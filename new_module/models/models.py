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
    name = fields.Char()
    value = fields.Integer()
    descuento = fields.Float(compute="_value_pc", store=True)
    rut = fields.Char()
    
    documento=fields.Char()
    folio = fields.Char()
    date_start = fields.Date(
        string="Fecha Inicio",
        help="Date when the user initiated the request.",
        default=fields.Date.context_today,
        tracking=True,
    )
    tipo_documento=fields.Char()
    
    
    """ is_editable = fields.Boolean(compute="_compute_is_editable", readonly=True) """

    
    @api.depends('value')

    
    def _value_pc(self):
        for record in self:
            record.descuento = float(record.value) * 0.10