from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "inherited.model"

    new_field = fields.Char(string="New Field")
    