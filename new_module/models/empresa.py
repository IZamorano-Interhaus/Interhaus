from odoo import models, fields, api, _
from datetime import  date
from dateutil.relativedelta import *

class compañia(models.Model):
    _name="new_module.compañia"
    _description="modulo para linkear las compañias con los proveedores"
    partner_id = fields.Many2many(
        'new_module.proveedores',string = 'Contacto Proveedor'
    )
    name = fields.Char(
        'nombre compañia'
    )
    street = fields.Char(
        'direccion'
    )
