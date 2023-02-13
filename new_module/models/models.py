# -*- coding: utf-8 -*-
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from odoo import tools
from odoo.http import request
from odoo import models, fields, api, _
from odoo.exceptions import UserError
_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To be approved"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("done", "Done"),
]
auxlista=list()
numero=0


class FollowupStatByPartner(models.Model):
    _name = "followup.stat.by.partner"
    _description = "Follow-up Statistics by Partner"
    _rec_name = 'partner_id'
    _auto = False

    def _get_invoice_partner_id(self):
        for rec in self:
            rec.invoice_partner_id = rec.partner_id.address_get(
                adr_pref=['invoice']).get('invoice', rec.partner_id.id)

    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    date_move = fields.Date('First move', readonly=True)
    date_move_last = fields.Date('Last move', readonly=True)
    date_followup = fields.Date('Latest follow-up', readonly=True)
    max_followup_id = fields.Many2one('followup.line', 'Max Follow Up Level', readonly=True, ondelete="cascade")
    balance = fields.Float('Balance', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    invoice_partner_id = fields.Many2one('res.partner', compute='_get_invoice_partner_id', string='Invoice Address')

    @api.model
    
    def get_latebills(self, *post):

        company_id = self.get_current_company_value()

        states_arg = ""
        if post != ('posted',):
            states_arg = """ account_move.state in ('posted', 'draft')"""
        else:
            states_arg = """ account_move.state = 'posted'"""

        self._cr.execute(('''  select res_partner.name as partner, res_partner.commercial_partner_id as res  ,
                            account_move.commercial_partner_id as parent, sum(account_move.amount_total) as amount
                            from account_move,res_partner where 
                            account_move.partner_id=res_partner.id AND account_move.move_type = 'in_invoice' AND
                            payment_state = 'not_paid' AND 
                              account_move.company_id in ''' + str(tuple(company_id)) + ''' AND
                            %s 
                            AND  account_move.commercial_partner_id=res_partner.commercial_partner_id 
                            group by parent,partner,res
                            order by amount desc ''') % (states_arg))

        record = self._cr.dictfetchall()

        bill_partner = [item['partner'] for item in record]

        bill_amount = [item['amount'] for item in record]

        amounts = sum(bill_amount[9:])
        name = bill_partner[9:]
        results = []
        pre_partner = []

        bill_amount = bill_amount[:9]
        bill_amount.append(amounts)
        bill_partner = bill_partner[:9]
        bill_partner.append("Others")
        records = {
            'bill_partner': bill_partner,
            'bill_amount': bill_amount,
            'result': results,

        }
        return records

        # return record

    # function to getting over dues



class RecurringPayments(models.Model):
    _name = 'account.recurring.payments'
    _description = 'Accounting Recurring Payment'

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

    

class GetAllRecurringEntries(models.TransientModel):
    _name = 'account.recurring.entries.line'
    _description = 'Account Recurring Entries Line'

    date = fields.Date('Date')
    template_name = fields.Char('Name')
    amount = fields.Float('Amount')
    tmpl_id = fields.Many2one('account.recurring.payments', string='id')





    """ @api.model
    def getDocument(self):
        with open("new 2.json") as archivo:
            auxdiccionario = json.load(archivo)
        with open("new 2.json", 'w') as archivo_nuevo:
            json.dump(auxdiccionario, archivo_nuevo)
        for x in range(len(auxdiccionario["ventas"]["detalleVentas"])):
            if x.folio_documento=="":
                numero+=1
                auxlista.append(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["rutCliente"]+" | "+str(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["folio"]))
                self._cr.execute(

                ) """
