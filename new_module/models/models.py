# -*- coding: utf-8 -*-

from odoo import models, fields, api


class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module'
    name = fields.Char()
    value = fields.Integer()
    descuento = fields.Float(compute="_value_pc", store=True)
    
    rut = fields.Char()
    folio = fields.Integer()
    """ asset_depreciation_ids = fields.One2many('account.asset.depreciation.registro', 'move_id',
                                             string='Assets Depreciation Lines') """

   
    @api.depends('value')

    
    def _value_pc(self):
        for record in self:
            record.descuento = float(record.value) * 0.10
        
    """ def _call_data(self):
        for move in self:
            for registro in move.asset_deprecation_ids:
                registro.move_posted_click = True
        return super(new_module, self)._call_data() """
    