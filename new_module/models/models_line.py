# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class lineaNuevoModulo(models.Model):
    _name="linea.nuevo.modulo"
    _description="linea nuevo modulo"
    product_id= fields.Many2one(
        comodel_name="account.move.line",
        string="Producto",
        copy=False,
        index=True
    )
    account_id= fields.Many2one(
        comodel_name="account.move.line",
        string="Cuenta",
        copy=False,
        index=True
    )