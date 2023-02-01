# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module' 

    cliente = fields.Char(
        string="Referencia comprador",
        required=True,
        default=lambda self: _("Ejemplo: Nicolas"),
    )
    rut_tributario = fields.Char(
        string="Rut",
        required=True,
        default=lambda self: _("Sin puntos y con guión"),
    )   
    documento=fields.Many2one(
        comodel_name="product.product",
        string="documento",
        copy=False,
        index=True,
    )
    tipo_documento=fields.Many2one(
        comodel_name="product.product",
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
    fecha_vencimiento = fields.Date(
        string="fecha de vencimiento",
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
    supplier_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Supplier",
        required=True,
        context={"res_partner_search_mode": "supplier"},
    )
    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Purchase Order",
        domain=[("state", "=", "draft")],
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
    debit_account = fields.Many2one('account.account', 'Debit Account',
                                    required=True,
                                    domain="['|', ('company_id', '=', False), "
                                           "('company_id', '=', company_id)]")
    credit_account = fields.Many2one('account.account', 'Credit Account',
                                     required=True,
                                     domain="['|', ('company_id', '=', False), "
                                            "('company_id', '=', company_id)]")
    journal_id = fields.Many2one('account.journal', 'Journal', required=True)
    analytic_account_id = fields.Many2one('account.analytic.account',
                                          'Analytic Account')
    date = fields.Date('Starting Date', required=True, default=date.today())
    next_date = fields.Date('Next Schedule', compute=_get_next_schedule,
                            readonly=True, copy=False)
    recurring_period = fields.Selection(selection=[('days', 'Days'),
                                                   ('weeks', 'Weeks'),
                                                   ('months', 'Months'),
                                                   ('years', 'Years')],
                                        store=True, required=True)
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
    partner_id = fields.Many2one('res.partner', 'Partner')
    pay_time = fields.Selection(selection=[('pay_now', 'Pay Directly'),
                                           ('pay_later', 'Pay Later')],
                                store=True, required=True)
    company_id = fields.Many2one('res.company',
                                 default=lambda l: l.env.company.id)
    recurring_lines = fields.One2many('account.recurring.entries.line', 'tmpl_id')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id.property_account_receivable_id:
            self.credit_account = self.partner_id.property_account_payable_id

    @api.model
    def _cron_generate_entries(self):
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
                move_id.post()
class GetAllRecurringEntries(models.TransientModel):
    _name = 'account.recurring.entries.line'
    _description = 'Account Recurring Entries Line'

    date = fields.Date('Date')
    template_name = fields.Char('Name')
    amount = fields.Float('Amount')
    tmpl_id = fields.Many2one('account.recurring.payments', string='id')