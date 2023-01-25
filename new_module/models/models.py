# -*- coding: utf-8 -*-

""" from odoo import models, fields, api


class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module'
    name = fields.Char()
    value = fields.Integer()
    descuento = fields.Float(compute="_value_pc", store=True)
    
    rut = fields.Char()
    folio = fields.Integer()
    documento = fields.Char()
    tipo_documento = fields.Integer()

    

    

   
    @api.depends('value')

    
    def _value_pc(self):
        for record in self:
            record.descuento = float(record.value) * 0.10
        
  
    
