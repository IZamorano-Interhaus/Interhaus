# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, exceptions, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _purchase_request_confirm_message_content(self, request, request_dict=None):
        self.ensure_one()
        if not request_dict:
            request_dict = {}
        title = _("Order confirmation %(po_name)s for your Request %(pr_name)s") % {
            "po_name": self.name,
            "pr_name": request.name,
        }
        message = "<h3>%s</h3><ul>" % title
        message += _(
            "The following requested items from Purchase Request %(pr_name)s "
            "have now been confirmed in Purchase Order %(po_name)s:"
        ) % {
            "po_name": self.name,
            "pr_name": request.name,
        }

        for line in request_dict.values():
            message += _(
                "<li><b>%(prl_name)s</b>: Ordered quantity %(prl_qty)s %(prl_uom)s, "
                "Planned date %(prl_date_planned)s</li>"
            ) % {
                "prl_name": line["name"],
                "prl_qty": line["product_qty"],
                "prl_uom": line["product_uom"],
                "prl_date_planned": line["date_planned"],
            }
        message += "</ul>"
        return message

    

    

    def button_confirm(self):
        self._purchase_request_line_check()
        res = super(PurchaseOrder, self).button_confirm()
        self._purchase_request_confirm_message()
        return res

    def unlink(self):
        alloc_to_unlink = self.env["purchase.request.allocation"]
        for rec in self:
            for alloc in (
                rec.order_line.mapped("purchase_request_lines")
                .mapped("purchase_request_allocation_ids")
                .filtered(
                    lambda alloc, rec=rec: alloc.purchase_line_id.order_id.id == rec.id
                )
            ):
                alloc_to_unlink += alloc
        res = super().unlink()
        alloc_to_unlink.unlink()
        return res


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    purchase_request_lines = fields.Many2many(
        comodel_name="purchase.request.line",
        relation="purchase_request_purchase_order_line_rel",
        column1="purchase_order_line_id",
        column2="purchase_request_line_id",
        readonly=True,
        copy=False,
    )

    purchase_request_allocation_ids = fields.One2many(
        comodel_name="purchase.request.allocation",
        inverse_name="purchase_line_id",
        string="Purchase Request Allocation",
        copy=False,
    )

    def action_open_request_line_tree_view(self):
        """
        :return dict: dictionary value for created view
        """
        request_line_ids = []
        for line in self:
            request_line_ids += line.purchase_request_lines.ids

        domain = [("id", "in", request_line_ids)]

        return {
            "name": _("Purchase Request Lines"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.request.line",
            "view_mode": "tree,form",
            "domain": domain,
        }

    def _prepare_stock_moves(self, picking):
        self.ensure_one()
        val = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        all_list = []
        for v in val:
            all_ids = self.env["purchase.request.allocation"].search(
                [("purchase_line_id", "=", v["purchase_line_id"])]
            )
            for all_id in all_ids:
                all_list.append((4, all_id.id))
            v["purchase_request_allocation_ids"] = all_list
        return val

    

    @api.model
    def _purchase_request_confirm_done_message_content(self, message_data):
        title = _("Service confirmation for Request %s") % (
            message_data["request_name"]
        )
        message = "<h3>%s</h3>" % title
        message += _(
            "The following requested services from Purchase"
            " Request %(request_name)s requested by %(requestor)s "
            "have now been received:"
        ) % {
            "request_name": message_data["request_name"],
            "requestor": message_data["requestor"],
        }
        message += "<ul>"
        message += _(
            "<li><b>%(product_name)s</b>: "
            "Received quantity %(product_qty)s %(product_uom)s</li>"
        ) % {
            "product_name": message_data["product_name"],
            "product_qty": message_data["product_qty"],
            "product_uom": message_data["product_uom"],
        }
        message += "</ul>"
        return message

    

    def write(self, vals):
        #  As services do not generate stock move this tweak is required
        #  to allocate them.
        prev_qty_received = {}
        if vals.get("qty_received", False):
            service_lines = self.filtered(lambda l: l.product_id.type == "service")
            for line in service_lines:
                prev_qty_received[line.id] = line.qty_received
        res = super(PurchaseOrderLine, self).write(vals)
        if prev_qty_received:
            for line in service_lines:
                line.update_service_allocations(prev_qty_received[line.id])
        return res
