# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import tools

class importData(models.Model):
    _name = "import.data"


    def _get_data_by_folio(self):
        for x in self:
            x.folio = x.partner_id.address_get(
                adr_pref=['invoice']).get('invoice', x.partner_id.id)
    
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    primera_fecha = fields.Date('First move', readonly=True)
    ultima_fecha = fields.Date('Last move', readonly=True)
    fecha_seguimiento = fields.Date('Latest follow-up', readonly=True)
    max_followup_id = fields.Many2one('followup.line', 'Max Follow Up Level', readonly=True, ondelete="cascade")
    balance = fields.Float('Balance', readonly=True)
    rutTributario = fields.Many2one('res.company', 'Company', readonly=True)
    folio = fields.Many2one('res.partner', compute='_get_data_by_folio', string='Invoice Address')

    @api.model

    def inicio(self):
        tools.drop_viw_if_exists(self._cr,'import_data')
        self._cr.execute(
            "aqui ira la sintaxis sql para traer los datos"
            "select * from "
        )