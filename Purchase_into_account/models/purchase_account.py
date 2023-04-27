# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class reporte_detalle(models.Model):
    _inherit='purchase.order.line'

class OrdenCompra(models.Model):
    _inherit=['purchase.order']

    #name=fields.Char(compute="_get_name")
    x_studio_many2one_field_w1OXM=fields.Many2one('account.analytic.account', compute="_get_centro_negocio")
    x_studio_cuenta_contable=fields.Many2one('account.account',compute="_get_cuenta_contable")
    
    partner_id=fields.Many2one('res.partner',compute="partner_id")
    amount_total=fields.Monetary(compute="_get_amount_total")
    invoice_status=fields.Selection(selection=[
            ('no','Nada para facturar'),
            ('to invoice','Para Facturar'),
            ('invoiced','Totalmente facturado')],compute="_get_invoice_status")

    @api.depends('currency_id','company_id','partner_id')
    def _get_name(self):
        super(OrdenCompra,self)
        query="""
                select name
                from purchase_order;
                """
        self.env.cr.execute(query)
        res=self.env.cr.fetchone()
        
        for OC in self:
            id = OC.id
            result = {id: {'name': res}}
        return result
    
    @api.depends('currency_id','company_id','partner_id')
    def _get_cuenta_contable(self):
        query="""
                select x_studio_cuenta_contable
                from purchase_order;
                """
        self.env.cr.execute(query)
        res=self.env.cr.fetchone()
        return res
    
    @api.depends('currency_id','company_id','partner_id')
    def _get_centro_negocio(self):
        query="""
                    select x_studio_many2one_field_w1OXM
                    from purchase_order;
                """
        self.env.cr.execute(query)
        res=self.env.cr.fetchone()
        return res
    
    @api.depends('currency_id','company_id','partner_id')
    def _get_date_approve(self):
        query="""
                select date_approve
                from purchase_order;
                """
        self.env.cr.execute(query)
        res=self.env.cr.fetchone()
        return res
    @api.depends('currency_id','company_id','partner_id')
    def _get_partner_id(self):
        query="""
                select partner_id
                from purchase_order;
                """
        self.env.cr.execute(query)
        res=self.env.cr.fetchone()
        return res
    @api.depends('currency_id','company_id','partner_id')
    def _get_amount_total(self):
        query="""
                select amount_total
                from purchase_order;
                """
        self.env.cr.execute(query)
        res=self.env.cr.fetchone()
        return res
    @api.depends('currency_id','company_id','partner_id')
    def _get_invoice_status(self):
        query="""
                select invoice_status
                from purchase_order;
                """
        self.env.cr.execute(query)
        res=self.env.cr.fetchone()
        return res
    

