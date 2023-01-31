# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import get_lang

class initial_data(models.TransientModel):
    _name='new_module.new_module'
    _description='new_module.new_module'

    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier",
        required=True,
        context={"res_partner_search_mode": "supplier"},
    )
    
    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Purchase Order",
        domain=[("state", "=", "draft")],
    )
    sync_data_planned = fields.Boolean(
        string="Match existing PO lines by Scheduled Date",
        help=(
            "When checked, PO lines on the selected purchase order are only reused "
            "if the scheduled date matches as well."
        ),
    )

    @api.model

    def preparar_objeto(self,linea):
        return {
            "line_id": linea.id,
            "request_id": linea.request_id.id,
            "product_id": linea.product_id.id,
            "name": linea.name or linea.product_id.name,
            "product_qty": linea.pending_qty_to_receive,
            "product_uom_id": linea.product_uom_id.id,
        }
    
    @api.model
    def _check_valid_request_line(self, request_line_ids):
        picking_type = False
        company_id = False

        for linaje in self.env["purchase.request.line"].browse(request_line_ids):
            if linaje.request_id.state == "done":
                raise UserError(_("The purchase has already been completed."))
            if linaje.request_id.state != "approved":
                raise UserError(
                    _("Purchase Request %s is not approved") % linaje.request_id.name
                )

            if linaje.purchase_state == "done":
                raise UserError(_("The purchase has already been completed."))

            line_company_id = linaje.company_id and linaje.company_id.id or False
            if company_id is not False and line_company_id != company_id:
                raise UserError(_("You have to select lines from the same company."))
            else:
                company_id = line_company_id

            line_picking_type = linaje.request_id.picking_type_id or False
            if not line_picking_type:
                raise UserError(_("You have to enter a Picking Type."))
            if picking_type is not False and line_picking_type != picking_type:
                raise UserError(
                    _("You have to select lines from the same Picking Type.")
                )
            else:
                picking_type = line_picking_type

