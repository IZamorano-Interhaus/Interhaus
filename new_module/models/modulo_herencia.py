from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "res.partner"

    new_field = fields.Char(string="New Field")
    