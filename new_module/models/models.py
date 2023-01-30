# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To be approved"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("done", "Done"),
]

class new_module(models.Model):

    
    _name = 'new_module.new_module'
    _description = 'new_module.new_module'
    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)
    @api.model
    def _company_get(self):
        return self.env["res.company"].browse(self.env.company.id)

    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)

    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("purchase.request")
    name = fields.Char(
        string="Referencia comprador",
        required=True,
        default=lambda self: _("Ejemplo: Nicolas"),
        tracking=True,
    )
    @api.model
    def _default_picking_type(self):
        type_obj = self.env["stock.picking.type"]
        company_id = self.env.context.get("company_id") or self.env.company.id
        types = type_obj.search(
            [("code", "=", "incoming"), ("warehouse_id.company_id", "=", company_id)]
        )
        if not types:
            types = type_obj.search(
                [("code", "=", "incoming"), ("warehouse_id", "=", False)]
            )
        return types[:1]

    value = fields.Integer()
    descuento = fields.Float(compute="_value_pc", store=True)
    rut = fields.Char(
        string="Rut",
        required=True,
        default=lambda self: _("Sin puntos y con guión"),
        tracking=True,
    )
    
    documento=fields.Many2one(
        comodel_name="product.product",
        string="documento",
        copy=False,
        index=True,
    )

    folio = fields.Many2one(
        comodel_name="procurement.group",
        string="Folio",
        copy=False,
        index=True,
    )

    date_start = fields.Date(
        string="Fecha Inicio",
        help="Date when the user initiated the request.",
        default=fields.Date.context_today,
        tracking=True,
    )
    is_name_editable = fields.Boolean(
        default=lambda self: self.env.user.has_group("base.group_no_one"),
    )
    origin = fields.Char(string="Source Document")
    
    requested_by = fields.Many2one(
        comodel_name="res.users",
        required=True,
        copy=False,
        tracking=True,
        default=_get_default_requested_by,
        index=True,
    )
    assigned_to = fields.Many2one(
        comodel_name="res.users",
        string="Approver",
        tracking=True,
        domain=lambda self: [
            (
                "groups_id",
                "in",
                self.env.ref("purchase_request.group_purchase_request_manager").id,
            )
        ],
        index=True,
    )
    description = fields.Text()
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=False,
        default=_company_get,
        tracking=True,
    )
    
    state = fields.Selection(
        selection=_STATES,
        string="Status",
        index=True,
        tracking=True,
        required=True,
        copy=False,
        default="draft",
    )
    is_editable = fields.Boolean(compute="_compute_is_editable", readonly=True)
    to_approve_allowed = fields.Boolean(compute="_compute_to_approve_allowed")
    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Picking Type",
        required=True,
        default=_default_picking_type,
    )
    group_id = fields.Many2one(
        comodel_name="procurement.group",
        string="Procurement Group",
        copy=False,
        index=True,
    )
    line_count = fields.Integer(
        string="Purchase Request Line count",
        compute="_compute_line_count",
        readonly=True,
    )
    move_count = fields.Integer(
        string="Stock Move count", compute="_compute_move_count", readonly=True
    )
    purchase_count = fields.Integer(
        string="Purchases count", compute="_compute_purchase_count", readonly=True
    )
    currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)
    estimated_cost = fields.Monetary(
        compute="_compute_estimated_cost",
        string="Total Estimated Cost",
        store=True,
    )

    
    is_editable = fields.Boolean(compute="_compute_is_editable", readonly=True)

    
    @api.depends('value')

    
    def _value_pc(self):
        for record in self:
            record.descuento = float(record.value) * 0.10