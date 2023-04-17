from odoo import fields,models,api,_
from datetime import  date

class borradoresFactura(models.Model):
    
    _name="new_module.borrador.factura"
    _description="modulo para crear tabla borrador para alojar los datos que se obtienen en facturas"

    tipoDTEString= fields.Char(),
    tipoDTE= fields.Integer(),
    tipoCompra= fields.Char(),
    rutCliente= fields.Char(),
    razonSocial= fields.Char(),
    folio= fields.Integer(),
    fechaEmision= fields.Date(),
    fechaRecepcion = fields.Date(),
    acuseRecibo= fields.Selection(),
    montoExento = fields.Float(),
    montoNeto= fields.Float(),
    montoIvaRecuperable =  fields.Float(),
    montoTotal= fields.Float() ,
    ivaNoRetenido= fields.Float(),
    totalOtrosImpuestos=  fields.Float(),
    valorOtroImpuesto= fields.Char(),
    tasaOtroImpuesto = fields.Char(),
    tipoDocReferencia = fields.Integer(),
    trackId= fields.Integer(),
    referencias= fields.Char(),
    referenciado=fields.Char() ,
    reparos=fields.Char() ,
    otrosImpuestos=fields.Char() ,
    estado=fields.Selection() 
    



class borradorDetalle(models.Model):
    _name="new_module.borrador.detalle"
    _description="Muestra la cantidad de documentos emitidos segun el tipo de documento"

    tipoDte= fields.Integer(),
    tipoDteString= fields.Char(),
    totalDocumentos=fields.Integer(),
    montoExento=fields.Integer(),
    montoNeto=fields.Integer(),
    ivaRecuperable=fields.Float(), 
    ivaUsoComun= fields.Float(),
    ivaNoRecuperable=fields.Float(),
    montoTotal=fields.Float(),
    estado=fields.Selection()
