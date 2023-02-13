# Copyright 2017 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def _purchase_request_confirm_done_message_content(self, message_data):
        title = _(
            "Receipt confirmation %(picking_name)s for your Request %(request_name)s"
        ) % {
            "picking_name": message_data["picking_name"],
            "request_name": message_data["request_name"],
        }
        message = "<h3>%s</h3>" % title
        message += _(
            "The following requested items from Purchase Request %(request_name)s "
            "have now been received in %(location_name)s using Picking %(picking_name)s:"
        ) % {
            "request_name": message_data["request_name"],
            "location_name": message_data["location_name"],
            "picking_name": message_data["picking_name"],
        }
        message += "<ul>"
        message += _(
            "<li><b>%(product_name)s</b>: "
            "Transferred quantity %(product_qty)s %(product_uom)s</li>"
        ) % {
            "product_name": message_data["product_name"],
            "product_qty": message_data["product_qty"],
            "product_uom": message_data["product_uom"],
        }
        message += "</ul>"
        return message

    @api.model
    def _picking_confirm_done_message_content(self, message_data):
        title = _("Receipt confirmation for Request %s") % (
            message_data["request_name"]
        )
        message = "<h3>%s</h3>" % title
        message += _(
            "The following requested items from Purchase Request %(request_name)s "
            "requested by %(requestor)s "
            "have now been received in %(location_name)s:"
        ) % {
            "request_name": message_data["request_name"],
            "requestor": message_data["requestor"],
            "location_name": message_data["location_name"],
        }
        message += "<ul>"
        message += _(
            "<li><b>%(product_name)s</b>: "
            "Transferred quantity %(product_qty)s %(product_uom)s</li>"
        ) % {
            "product_name": message_data["product_name"],
            "product_qty": message_data["product_qty"],
            "product_uom": message_data["product_uom"],
        }
        message += "</ul>"
        return message

   

    def _action_done(self):
        res = super(StockMoveLine, self)._action_done()
        self.allocate()
        return res
