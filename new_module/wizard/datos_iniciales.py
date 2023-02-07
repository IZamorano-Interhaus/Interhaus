# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from datetime import datetime, date
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import get_lang
from dateutil.relativedelta import relativedelta

_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To be approved"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("done", "Done"),
]
class initial_data(models.TransientModel):
    _name='new_module.new_module'
    _description='new_module.new_module'

    cliente = fields.Many2one('res.partner', 'tributante')
    
    rut_tributario = fields.Char(
        string="Rut",
        required=True,
        default=lambda self: _("Sin puntos y con guión"),
    )   
    documento=fields.Many2one(
        comodel_name="account.account",
        string="documento",
        copy=False,
        index=True,
    )
    tipo_documento=fields.Many2one(
        comodel_name="ir_act_client",
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
        default=fields.Date.context_today,
        string = "plazo de pago"
    )
    documento_id = fields.Char(
        string = "Número de documento",
        required=True,
    )
    diario = fields.Many2one(
        comodel_name="account.account",
        string="Diario",
        copy=False,
        index=True,
    )
    supplier_id = fields.Many2one(
        comodel_name="account.journal",
        string="Supplier",
        required=True,
        context={"res_partner_search_mode": "supplier"},
    )
    purchase_order_id = fields.Many2one(
        comodel_name="ir.act.client",
        string="Purchase Order",
        domain=[("state", "=", "draft")],
    )
    def _get_next_schedule(self):
        if self.date:
            recurr_dates = []
            today = datetime.today()
            start_date = datetime.strptime(str(self.date), '%Y-%m-%d')
            while start_date <= today:
                recurr_dates.append(str(start_date.date()))
                if self.recurring_period == 'days':
                    start_date += relativedelta(days=self.recurring_interval)
                elif self.recurring_period == 'weeks':
                    start_date += relativedelta(weeks=self.recurring_interval)
                elif self.recurring_period == 'months':
                    start_date += relativedelta(months=self.recurring_interval)
                else:
                    start_date += relativedelta(years=self.recurring_interval)
            self.next_date = start_date.date()   
    
    
    @api.model
    def get_items(self, request_line_ids):
        request_line_obj = self.env["purchase.request.line"]
        items = []
        request_lines = request_line_obj.browse(request_line_ids)
        self._check_valid_request_line(request_line_ids)
        self.check_group(request_lines)
        for line in request_lines:
            items.append([0, 0, self._prepare_item(line)])
        return items
    
    
    @api.model
    def _prepare_purchase_order_line(self, po, item):
        if not item.product_id:
            raise UserError(_("Please select a product for all lines"))
        product = item.product_id
        # Keep the standard product UOM for purchase order so we should
        # convert the product quantity to this UOM
        qty = item.product_uom_id._compute_quantity(
            item.product_qty, product.uom_po_id or product.uom_id
        )
        # Suggest the supplier min qty as it's done in Odoo core
        min_qty = item.line_id._get_supplier_min_qty(product, po.partner_id)
        qty = max(qty, min_qty)
        date_required = item.line_id.date_required
        return {
            "order_id": po.id,
            "product_id": product.id,
            "product_uom": product.uom_po_id.id or product.uom_id.id,
            "price_unit": 0.0,
            "product_qty": qty,
            "analytic_distribution": item.line_id.analytic_distribution,
            "purchase_request_lines": [(4, item.line_id.id)],
            "date_planned": datetime(
                date_required.year, date_required.month, date_required.day
            ),
            "move_dest_ids": [(4, x.id) for x in item.line_id.move_dest_ids],
        }
    """ @api.model
    def _get_purchase_line_name(self, order, line):
        
        product_lang = line.product_id.with_context(
            lang=get_lang(self.env, self.supplier_id.lang).code,
            partner_id=self.supplier_id.id,
            company_id=order.company_id.id,
        )
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += "\n" + product_lang.description_purchase
        return name """
    @api.model
    def _get_order_line_search_domain(self, order, item):
        vals = self._prepare_purchase_order_line(order, item)
        name = self._get_purchase_line_name(order, item)
        order_line_data = [
            ("order_id", "=", order.id),
            ("name", "=", name),
            ("product_id", "=", item.product_id.id),
            ("product_uom", "=", vals["product_uom"]),
            ("analytic_distribution", "=?", item.line_id.analytic_distribution),
        ]
        if self.sync_data_planned:
            date_required = item.line_id.date_required
            order_line_data += [
                (
                    "date_planned",
                    "=",
                    datetime(
                        date_required.year, date_required.month, date_required.day
                    ),
                )
            ]
        if not item.product_id:
            order_line_data.append(("name", "=", item.name))
        return order_line_data
    