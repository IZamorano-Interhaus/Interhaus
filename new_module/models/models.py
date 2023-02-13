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
auxlista=list()
numero=0
class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module' 
    partner_id = fields.Many2one(
        comodel_name="account.move",
        string="Proveedor",
        copy=False,
        index=True,
    )
    rut_tributario = fields.Char(
        string="Rut",
        required=True,
    )   
    tipo_documento=fields.Many2one(
        comodel_name="procurement.group",
        string="Tipo de Documento",
        copy=False,
        index=True,
    )
    folio_documento = fields.Many2one(
        comodel_name="procurement.group",
        string="Folio",
        copy=False,
        index=True,
    )
    company_id = fields.Many2one('res.company',
                                 default=lambda l: l.env.company.id)
    date_start = fields.Date(
        string="Fecha contable",
        help="Date when the user initiated the request.",
        default=fields.Date.context_today,
    )
    referencia_pago = fields.Char(
        string="Referencia de pago",
        help="La referencia de pago para establecer en apuntes de diario.",
    )
    fecha_factura = fields.Date(
        string="Fecha factura",
        default=fields.Date.context_today
    )
    terminos_pagos = fields.Many2one(
        comodel_name="procurement.group",
        string="Términos de Pago",
        copy=False,
        index=True,
    )
    documento_id = fields.Char(
        string = "Número de documento",
        required=True,
    )
    journal_id = fields.Many2one('procurement.group', 'Diario', required=True)
    date = fields.Date('Starting Date', required=True, default=date.today())
    amount = fields.Float('Monto')
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('running', 'Running')],
                             default='draft', string='estado')
    @api.model
    def getDocument(self, *post):
        """ with open("new 2.json") as archivo:
            auxdiccionario = json.load(archivo)
        with open("new 2.json", 'w') as archivo_nuevo:
            json.dump(auxdiccionario, archivo_nuevo) """
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
    @api.model
    def get_latebillss(self, *post):
        company_id = self.get_current_company_value()
        partners = self.env['res.partner'].search([('active', '=', True)])
        states_arg = ""
        if post[0] != 'posted':
            states_arg = """ account_move.state in ('posted', 'draft')"""
        else:
            states_arg = """ account_move.state = 'posted'"""
        if post[1] == 'this_month':
            self._cr.execute((''' 
                                select to_char(account_move.date, 'Month') as month, res_partner.name as bill_partner, account_move.partner_id as parent,
                                sum(account_move.amount_total) as amount from account_move, res_partner where account_move.partner_id = res_partner.id
                                AND account_move.move_type = 'in_invoice'
                                AND payment_state = 'not_paid'
                                AND %s 
                                AND Extract(month FROM account_move.invoice_date_due) = Extract(month FROM DATE(NOW()))
                                AND Extract(YEAR FROM account_move.invoice_date_due) = Extract(YEAR FROM DATE(NOW()))
                                AND account_move.company_id in ''' + str(tuple(company_id)) + '''
                                AND account_move.partner_id = res_partner.commercial_partner_id
                                group by parent, bill_partner, month
                                order by amount desc ''') % (states_arg))
        else:
            self._cr.execute((''' select res_partner.name as bill_partner, account_move.partner_id as parent,
                                            sum(account_move.amount_total) as amount from account_move, res_partner where account_move.partner_id = res_partner.id
                                            AND account_move.move_type = 'in_invoice'
                                            AND payment_state = 'not_paid'
                                            AND %s
                                            AND Extract(YEAR FROM account_move.invoice_date_due) = Extract(YEAR FROM DATE(NOW()))
                                            AND account_move.partner_id = res_partner.commercial_partner_id
                                            AND account_move.company_id in ''' + str(tuple(company_id)) + '''
                                            group by parent, bill_partner
                                            order by amount desc ''') % (states_arg))
        result = self._cr.dictfetchall()
        bill_partner = [item['bill_partner'] for item in result]
        bill_amount = [item['amount'] for item in result]
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
        """ for x in range(len(auxdiccionario["ventas"]["detalleVentas"])):
            if x.folio_documento=="":
                numero+=1
                auxlista.append(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["rutCliente"]+" | "+str(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["folio"]))
                self._cr.execute(

                ) """