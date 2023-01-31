# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import get_lang

class initial_data(models.TransientModel):
    _name='new_module.new_module'
    _description='new_module.new_module'

    cliente = fields.Char(
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
    folio_documento = fields.Many2one(
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
    fecha_factura = fields.Date(
        string="fecha de factura",
        default=fields.Date.context_today
    )
    fecha_vencimiento = fields.Date(
        string="fecha de vencimiento",
        default=fields.Date.context_today
    )
    plazo_pago = fields.Date(
                default=fields.Date.context_today

    )
    documento_id = fields.Char(
        string = "Número de documento",
        required=True,
    )
    diario = fields.Many2one(
        comodel_name="procurement.group",
        string="Diario",
        copy=False,
        index=True,
    )
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

