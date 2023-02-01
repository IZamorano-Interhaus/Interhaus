# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module' 

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
        comodel_name="purchase.order",
        string="Supplier",
        required=True,
        context={"res_partner_search_mode": "supplier"},
    )
    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
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