from odoo import models,fields
from datetime import datetime, date

class TestModel(models.Model):
    _name="test.model"
    _description="una pequeña descripcion"

    name= fields.Char()
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
        copy=False,
        index=True,
    )
    rut_tributario = fields.Char(
        string="Rut",
    )   
    tipo_documento=fields.Many2one(
        comodel_name="res.partner",
        string="Tipo de Documento",
        copy=False,
        index=True,
    )
    folio_documento = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Folio",
        copy=False,
        index=True,
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda l: l.env.company.id
    )
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
        comodel_name="account.move",
        string="Términos de Pago",
        copy=False,
        index=True,
    )
    codigo_documento = fields.Char(
        string="Número del documento",
    )
    razon_social = fields.Char(
        string="nombre de la empresa que emite factura o la razon social",
    )
    acuseRecibo = fields.Selection(
        selection=[
            ('not_sent', 'Pendiente de ser enviado'),
            ('accepted','Aceptado'),
            ('ask_for_status', 'Consultar Estado Doc'),
            ('objected','Aceptado con reparos'),
            ('cancelled','Anulado'),
            ('rejected', 'Rechazado'),
            ('manual','Manual ( borrador)'),
        ],
        string='acusoRecibo',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='manual',
    )
    trackId = fields.Integer('Id de seguimiento')
    journal_id = fields.Many2one(
        'account.move', 'Diario',
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Cuenta Analitica'
    )
    date = fields.Date(
        'Starting Date', 
        required=True, 
        default=date.today()
    )
    state = fields.Selection(
        selection=[('draft', 'Draft'),
        ('running', 'Running')],
        default='draft', string='estado'
    )