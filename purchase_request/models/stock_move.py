# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class StockMove(models.Model):
    _inherit = "stock.move"

    created_purchase_request_line_id = fields.Many2one(
        comodel_name="purchase.request.line",
        string="Created Purchase Request Line",
        ondelete="set null",
        readonly=True,
        copy=False,
        index=True,
    )

    purchase_request_allocation_ids = fields.One2many(
        comodel_name="purchase.request.allocation",
        inverse_name="stock_move_id",
        copy=False,
        string="Purchase Request Allocation",
    )

    purchase_request_ids = fields.One2many(
        comodel_name="purchase.request",
        string="Purchase Requests",
        compute="_compute_purchase_request_ids",
    )

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        distinct_fields = super(StockMove, self)._prepare_merge_moves_distinct_fields()
        distinct_fields += ["created_purchase_request_line_id"]
        return distinct_fields

    

    

    def _merge_moves_fields(self):
        res = super(StockMove, self)._merge_moves_fields()
        res["purchase_request_allocation_ids"] = [
            (4, m.id) for m in self.mapped("purchase_request_allocation_ids")
        ]
        return res

    @api.constrains("company_id")
    def _check_company_purchase_request(self):
        if not self.ids:
            return
        self.env.cr.execute(
            """
            SELECT 1
            FROM purchase_request_allocation pra
            INNER JOIN stock_move sm
               ON sm.id=pra.stock_move_id
            WHERE pra.company_id != sm.company_id
                AND sm.id IN %s
            LIMIT 1
        """,
            (tuple(self.ids),),
        )
        if self.env.cr.fetchone():
            raise ValidationError(
                _(
                    "The company of the purchase request must match with "
                    "that of the location."
                )
            )

    def copy_data(self, default=None):
        """Propagate request allocation on copy.

        If this move is being split, or if this move is processed and there is
        a remaining allocation, move the appropriate quantity over to the new move.
        """
        if default is None:
            default = {}
        if not default.get("purchase_request_allocation_ids") and (
            default.get("product_uom_qty") or self.state in ("done", "cancel")
        ):
            default["purchase_request_allocation_ids"] = []
            new_move_qty = default.get("product_uom_qty") or self.product_uom_qty
            rounding = self.product_id.uom_id.rounding
            for alloc in self.purchase_request_allocation_ids.filtered(
                "open_product_qty"
            ):
                if (
                    float_compare(
                        new_move_qty,
                        0,
                        precision_rounding=self.product_id.uom_id.rounding,
                    )
                    <= 0
                    or float_compare(
                        alloc.open_product_qty, 0, precision_rounding=rounding
                    )
                    <= 0
                ):
                    break
                open_qty = min(new_move_qty, alloc.open_product_qty)
                new_move_qty -= open_qty
                default["purchase_request_allocation_ids"].append(
                    (
                        0,
                        0,
                        {
                            "purchase_request_line_id": alloc.purchase_request_line_id.id,
                            "requested_product_uom_qty": open_qty,
                        },
                    )
                )
                alloc.requested_product_uom_qty -= open_qty
        return super(StockMove, self).copy_data(default)
