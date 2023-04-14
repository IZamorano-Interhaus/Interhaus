from odoo import fields,models,api,_
from datetime import  date

class informe(models.Model):
    _inherit = "account.move"
    _name="new_module.informe"
    _description="modulo para descargar archivos en pdf y vista preliminar de libros contables"
    