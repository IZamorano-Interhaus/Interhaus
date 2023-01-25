# -*- coding: utf-8 -*-

""" from odoo import api, fields, models, _
from odoo import tools """

class importData():
    """ _name = "import.data"
    _description="obtener datos por el rut presente en odoo"


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

    @api.model """

    def __init__(self, rutTrib,folio,doc,tipoDoc):
        self.__rutTributario = rutTrib
        self.__folioDocumento = folio
        self.__documento= doc
        self.__tipoDocumento=tipoDoc
    #getters

    def get_rut(self):
      return self.__rutTributario

    def get_folio(self):
      return self.__folioDocumento
      
    def get_tipoDocumento(self):
      return self.__tipoDocumento

    def get_documento(self):
      return self.__documento
    #setters

    def set_rut(self,rutTributario):
      self.__rutTributario=rutTributario
    
    #metodos
    def rellenoDocumentos(self):
      if(self.get_tipoDocumento==30):
          set.__doc__="facturaa"
      

      
auxList=[]
mensaje = importData(19669468-4,123541,"factura de ventas y servicios no afectos o exentos de IVA",32)

""" print(mensaje.get_rut()," | ",mensaje.get_folio()) """
        