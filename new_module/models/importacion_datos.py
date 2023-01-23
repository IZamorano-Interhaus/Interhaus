from odoo import models, fields, api

class importar(models.Model):

    
    rut = fields.Text()
    folio = fields.Text()
    asset_depreciation_ids = fields.One2many('account.asset.depreciation.registro', 'move_id',
                                             string='Assets Depreciation Lines')
    @api.depends('rut')
    def Boton_desplegar_datos(self):
        for move in self:
            for registro in move.asset_depreciation_ids:
                registro.move_posted_click = False
        return super(importar, self).Boton_desplegar_datos()
    
