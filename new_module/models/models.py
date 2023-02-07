# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To be approved"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("done", "Done"),
]
class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module' 
    cliente = fields.Many2one('res.partner', 'Tributario')
    creating_user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    date_from = fields.Date('Start Date', required=True, states={'done': [('readonly', True)]})
    date_to = fields.Date('End Date', required=True, states={'done': [('readonly', True)]})
    
    
    partner_id = fields.Many2one(
        comodel_name="account.move",
        string="Proveedor",
        required=True,
    )   
    documento=fields.Many2one(
        comodel_name="product.product",
        string="documento",
        copy=False,
        index=True,
    )
    l10n_latam_document_type=fields.Many2one(
        comodel_name="account.move",
        string="tipo de documento",
        copy=False,
        index=True,
    )
    folio_documento = fields.Many2one(
        comodel_name="procurement.group",
        string="Folio",
        copy=False,
        index=True,
    )
    date_start = fields.Date(
        string="Fecha Inicio",
        help="Date when the user initiated the request.",
        default=fields.Date.context_today,
    )
    referencia_pago = fields.Char(
        string="Referencia de pago",
        help="La referencia de pago para establecer en apuntes de diario.",
    )
    fecha_factura = fields.Date(
        string="fecha de factura",
        default=fields.Date.context_today
    )
    plazo_pago = fields.Date(
                default=fields.Date.context_today
    )
    documento_id = fields.Char(
        string = "Número de documento",
        required=True,
    )
    diario = fields.Many2one(
        comodel_name="procurement.group",
        string="Diario",
        copy=False,
        index=True,
    )
    def _get_next_schedule(self):
        if self.date:
            recurr_dates = []
            today = datetime.today()
            start_date = datetime.strptime(str(self.date), '%Y-%m-%d')
            while start_date <= today:
                recurr_dates.append(str(start_date.date()))
                if self.recurring_period == 'days':
                    start_date += relativedelta(days=self.recurring_interval)
                elif self.recurring_period == 'weeks':
                    start_date += relativedelta(weeks=self.recurring_interval)
                elif self.recurring_period == 'months':
                    start_date += relativedelta(months=self.recurring_interval)
                else:
                    start_date += relativedelta(years=self.recurring_interval)
            self.next_date = start_date.date()
    name = fields.Char('Name')
   
    analytic_account_id = fields.Many2one('account.analytic.account',
                                          'Analytic Account')
    date = fields.Date('Starting Date', required=True, default=date.today())
    next_date = fields.Date('Next Schedule', compute=_get_next_schedule,
                            readonly=True, copy=False)
    
    amount = fields.Float('Amount')
    description = fields.Text('Description')
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('running', 'Running')],
                             default='draft', string='Status')
    journal_state = fields.Selection(selection=[('draft', 'Unposted'),
                                                ('posted', 'Posted')],
                                     required=True, default='draft',
                                     string='Generate Journal As')
    recurring_interval = fields.Integer('Recurring Interval', default=1)
    pay_time = fields.Selection(selection=[('pay_now', 'Pay Directly'),
                                           ('pay_later', 'Pay Later')],
                                store=True, required=True)
   
    @api.model
    def _company_get(self):
        return self.env["res.company"].browse(self.env.company.id)

    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)

    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("purchase.request")

    @api.model
    def _default_picking_type(self):
        type_obj = self.env["stock.picking.type"]
        company_id = self.env.context.get("company_id") or self.env.company.id
        types = type_obj.search(
            [("code", "=", "incoming"), ("warehouse_id.company_id", "=", company_id)]
        )
        if not types:
            types = type_obj.search(
                [("code", "=", "incoming"), ("warehouse_id", "=", False)]
            )
        return types[:1]

    @api.depends("state")
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ("to_approve", "approved", "rejected", "done"):
                rec.is_editable = False
            else:
                rec.is_editable = True
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self._get_default_name()
        requests = super(new_module, self).create(vals_list)
        for vals, request in zip(vals_list, requests):
            if vals.get("assigned_to"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
        return requests
    def write(self, vals):
        res = super(new_module, self).write(vals)
        for request in self:
            if vals.get("assigned_to"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
        return res
    def _can_be_deleted(self):
        self.ensure_one()
        return self.state == "draft"
    def unlink(self):
        for request in self:
            if not request._can_be_deleted():
                raise UserError(
                    _("You cannot delete a purchase request which is not draft.")
                )
        return super(new_module, self).unlink()
    def button_draft(self):
        self.mapped("line_ids").do_uncancel()
        return self.write({"state": "draft"})
    def button_to_approve(self):
        self.to_approve_allowed_check()
        return self.write({"state": "to_approve"})
    def button_approved(self):
        return self.write({"state": "approved"})
    def button_rejected(self):
        self.mapped("line_ids").do_cancel()
        return self.write({"state": "rejected"})
    def button_done(self):
        return self.write({"state": "done"})
    def check_auto_reject(self):
        """When all lines are cancelled the purchase request should be
        auto-rejected."""
        for pr in self:
            if not pr.line_ids.filtered(lambda l: l.cancelled is False):
                pr.write({"state": "rejected"})
    def to_approve_allowed_check(self):
        for rec in self:
            if not rec.to_approve_allowed:
                raise UserError(
                    _(
                        "You can't request an approval for a purchase request "
                        "which is empty. (%s)"
                    )
                    % rec.name
                )
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id.property_account_receivable_id:
            self.credit_account = self.partner_id.property_account_payable_id
    """ def _cron_generate_entries(self):
        data = self.env['account.recurring.payments'].search(
            [('state', '=', 'running')])
        entries = self.env['account.move'].search(
            [('recurring_ref', '!=', False)])
        journal_dates = []
        journal_codes = []
        remaining_dates = []
        for entry in entries:
            journal_dates.append(str(entry.date))
            if entry.recurring_ref:
                journal_codes.append(str(entry.recurring_ref))
        today = datetime.today()
        for line in data:
            if line.date:
                recurr_dates = []
                start_date = datetime.strptime(str(line.date), '%Y-%m-%d')
                while start_date <= today:
                    recurr_dates.append(str(start_date.date()))
                    if line.recurring_period == 'days':
                        start_date += relativedelta(
                            days=line.recurring_interval)
                    elif line.recurring_period == 'weeks':
                        start_date += relativedelta(
                            weeks=line.recurring_interval)
                    elif line.recurring_period == 'months':
                        start_date += relativedelta(
                            months=line.recurring_interval)
                    else:
                        start_date += relativedelta(
                            years=line.recurring_interval)
                for rec in recurr_dates:
                    recurr_code = str(line.id) + '/' + str(rec)
                    if recurr_code not in journal_codes:
                        remaining_dates.append({
                            'date': rec,
                            'template_name': line.name,
                            'amount': line.amount,
                            'tmpl_id': line.id,
                        })
        child_ids = self.recurring_lines.create(remaining_dates)
        for line in child_ids:
            tmpl_id = line.tmpl_id
            recurr_code = str(tmpl_id.id) + '/' + str(line.date)
            line_ids = [(0, 0, {
                'account_id': tmpl_id.credit_account.id,
                'partner_id': tmpl_id.partner_id.id,
                'credit': line.amount,
                # 'analytic_account_id': tmpl_id.analytic_account_id.id,
            }), (0, 0, {
                'account_id': tmpl_id.debit_account.id,
                'partner_id': tmpl_id.partner_id.id,
                'debit': line.amount,
                # 'analytic_account_id': tmpl_id.analytic_account_id.id,
            })]
            vals = {
                'date': line.date,
                'recurring_ref': recurr_code,
                'company_id': self.env.company.id,
                'journal_id': tmpl_id.journal_id.id,
                'ref': line.template_name,
                'narration': 'Recurring entry',
                'line_ids': line_ids
            }
            move_id = self.env['account.move'].create(vals)
            if tmpl_id.journal_state == 'posted':
                move_id.post() """