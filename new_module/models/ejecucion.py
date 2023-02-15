
from odoo import api, models,_

@api.model
def obtenerDatos(self): 
    
    query = "select simpleapi.sequence_number folio, odoo.vat rut from account_move simpleapi join res_partner odoo on simpleapi.commercial_partner_id = odoo.commercial_partner_id;"
    

    self._cr.execute(query)
    record = self._cr.dictfechall()
    