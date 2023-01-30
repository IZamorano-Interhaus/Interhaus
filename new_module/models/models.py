# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

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
    nombre = fields.Char(
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
    folio = fields.Many2one(
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
    date_factura = fields.Date(
        string="fecha de factura",
        default=fields.Date.context_today
    )
    fecha_vencimiento = fields.Date(
        string="fecha de vencimiento",
        default=fields.Date.context_today
    )
    documento_id = fields.Char(
        string = "Número de documento",
        required=True,
    )
    """ is_editable = fields.Boolean(compute="_compute_is_editable", readonly=True) """
class AccountJournalGroup(models.Model):
    _name = 'account.journal.group'
    _description = "Account Journal Group"
    _check_company_auto = True

    name = fields.Char("Journal Group", required=True, translate=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    excluded_journal_ids = fields.Many2many('account.journal', string="Excluded Journals", domain="[('company_id', '=', company_id)]",
        check_company=True)
    sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('uniq_name', 'unique(company_id, name)', 'A journal group name must be unique per company.'),
    ]