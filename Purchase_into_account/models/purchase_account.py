# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class reporte_detalle(models.Model):
    _inherit='purchase.order.line'
    x_studio_cuenta_contable = fields.Many2one(
        comodel_name='account.account',
        string='Cuenta contable',
        readonly=True,
        required=True,
    )
class OrdenCompra(models.Model):
    _inherit=['purchase.order','studio_customization.default_list_view_fo_03669b9d-d385-4147-ba8e-f3405fb19c44']

    

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

