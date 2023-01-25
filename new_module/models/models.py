# -*- coding: utf-8 -*-

from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module'
    name = fields.Char()
    value = fields.Integer()
    descuento = fields.Float(compute="_value_pc", store=True)
    
    rut = fields.Char()
    folio = fields.Integer()
    documento = fields.Char()
    tipo_documento = fields.Integer()

    name = fields.Char('Name', readonly=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id')
    amount = fields.Monetary(string="Amount", currency_field='currency_id')
    journal_id = fields.Many2one('account.journal', 'Journal',
                                 related='template_id.journal_id', readonly=False, required=True)
    payment_type = fields.Selection([
        ('outbound', 'Send Money'),
        ('inbound', 'Receive Money'),
    ], string='Payment Type', required=True, default='inbound')
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('done', 'Done')], default='draft', string='Status')
    date_begin = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)
    template_id = fields.Many2one('account.recurring.template', 'Recurring Template',
                                  domain=[('state', '=', 'done')],required=True)
    recurring_period = fields.Selection(related='template_id.recurring_period')
    recurring_interval = fields.Integer('Recurring Interval', required=True,
                                        related='template_id.recurring_interval', readonly=True)
    journal_state = fields.Selection(required=True, string='Generate Journal As',
                                     related='template_id.journal_state')

    description = fields.Text('Description')
    line_ids = fields.One2many('recurring.payment.line', 'recurring_payment_id', string='Recurring Lines')

    def compute_next_date(self, date):
        period = self.recurring_period
        interval = self.recurring_interval
        if period == 'days':
            date += relativedelta(days=interval)
        elif period == 'weeks':
            date += relativedelta(weeks=interval)
        elif period == 'months':
            date += relativedelta(months=interval)
        else:
            date += relativedelta(years=interval)
        return date

    def action_create_lines(self, date):
        ids = self.env['recurring.payment.line']
        vals = {
            'partner_id': self.partner_id.id,
            'amount': self.amount,
            'date': date,
            'recurring_payment_id': self.id,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'state': 'draft'
        }
        ids.create(vals)

    def action_done(self):
        date_begin = self.date_begin
        while date_begin < self.date_end:
            date = date_begin
            self.action_create_lines(date)
            date_begin = self.compute_next_date(date)
        self.state = 'done'

    def action_draft(self):
        if self.line_ids.filtered(lambda t: t.state == 'done'):
            raise ValidationError(_('You cannot Set to Draft as one of the line is already in done state'))
        else:
            for line in self.line_ids:
                line.unlink()
            self.state = 'draft'

    def action_generate_payment(self):
        line_ids = self.env['recurring.payment.line'].search([('date', '<=', date.today()),
                                                                       ('state', '!=', 'done')])
        for line in line_ids:
            line.action_create_payment()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'recurring.payment') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('recurring.payment') or _('New')
        return super(new_module, self).create(vals)

    @api.constrains('amount')
    def _check_amount(self):
        if self.amount <= 0:
            raise ValidationError(_('Amount Must Be Non-Zero Positive Number'))

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(_('Cannot delete done records !'))
        return super(new_module, self).unlink()


    

   
    @api.depends('value')

    
    def _value_pc(self):
        for record in self:
            record.descuento = float(record.value) * 0.10
        
  
    
