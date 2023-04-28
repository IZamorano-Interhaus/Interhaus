# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class reporte_detalle(models.Model):
    _inherit='purchase.order.line'

class OrdenCompra(models.Model):
    _inherit=['purchase.order']
    
    x_studio_cuenta_contable=fields.Many2one('account.account',compute="_get_cuenta_contable")
    
    name=fields.Text(string='N°OC', required=True, compute='_get_name', store=True, readonly=True)

    x_studio_many2one_field_w1OXM=fields.Many2one('account.analytic.account', compute="_get_centro_negocio")
    
    partner_id=fields.Many2one('res.partner',compute="partner_id")
    amount_total=fields.Monetary(compute="_get_amount_total")
    invoice_status=fields.Selection(selection=[
            ('no','Nada para facturar'),
            ('to invoice','Para Facturar'),
            ('invoiced','Totalmente facturado')],compute="_get_invoice_status")

    """ @api.depends('currency_id','company_id','partner_id')
    def _get_name(self):
        super(OrdenCompra,self)
        query=
                #select name
                #from purchase_order;
                
        self.env.cr.execute(query)
        res=self.env.cr.fetchone()
        
        for OC in self:
            id = OC.id
            result = {id: {'name': res}}
        return result
        """
    
    
    

