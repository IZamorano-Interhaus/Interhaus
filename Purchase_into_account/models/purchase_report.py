# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class reporte_detalle():
    _inherit="purchase.order.line"

class OrdenCompra():
    _inherit=['purcharse.order',]

    @api.depends('journal_id','company_id','partner_id')
    def _migracionDatos(self):
        query="""
                select Po.id,Po.name,Po.x_studio_cuenta_contable, Pol.analytic_distribution, Pol.price_total
                from purchase_order  Po
                join purchase_order_line Pol on Po.id=Pol.order_id;
                """
        self.env.cr.execute(query)
        res=self.env.cr.fetchone()
        return res

