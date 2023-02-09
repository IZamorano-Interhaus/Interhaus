# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, tools
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
        comodel_name="account.move",
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
    invoice_payment_term_id = fields.Many2one(
        comodel_name="account.move",
        string="Términos de Pago",
        copy=False,
        index=True,
    )
    documento_id = fields.Char(
        string = "Número de documento",
        required=True,
    )
    journal_id = fields.Many2one('account.move', 'Diario', required=True)
    analytic_account_id = fields.Many2one('account.analytic.account',
                                          'Analytic Account')
    date = fields.Date('Starting Date', required=True, default=date.today())
    amount = fields.Float('Amount')
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('running', 'Running')],
                             default='draft', string='Status')
    partner_id = fields.Many2one('res.partner', 'Partner')

    @api.model
    def init(self):
        tools.drop_view_if_exists(self._cr, 'followup_stat_by_partner')
        self._cr.execute("""
            create view followup_stat_by_partner as (
                SELECT
                    l.partner_id * 10000::bigint + l.company_id as id,
                    l.partner_id AS partner_id,
                    min(l.date) AS date_move,
                    max(l.date) AS date_move_last,
                    max(l.followup_date) AS date_followup,
                    max(l.followup_line_id) AS max_followup_id,
                    sum(l.debit - l.credit) AS balance,
                    l.company_id as company_id
                FROM
                    account_move_line l
                    LEFT JOIN account_account a ON (l.account_id = a.id)
                WHERE
                    a.account_type = 'asset_receivable' AND
                    l.full_reconcile_id is NULL AND
                    l.partner_id IS NOT NULL
                    GROUP BY
                    l.partner_id, l.company_id
            )""")