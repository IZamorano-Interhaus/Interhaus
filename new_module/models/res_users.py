from odoo import fields, models

class res_users(models.Model):
    _name = "res.users"
    _inherit="res.users"
    _description="usuario"

    new_field = fields.Char(string="New Field")