# -*- coding: utf-8 -*-
import psycopg2,json,os,sys
import xml.etree.ElementTree as ET
from odoo import models, fields, api, _
from datetime import  date
from dateutil.relativedelta import *
class pruebas(models.Model):
    _name = 'new_module.pruebas'
    _description = 'descripcion de las pruebas, un borrador' 
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
        copy=False,
        index=True,
    )
    rut_tributario = fields.Many2one(
        comodel_name='res.partner',
        string="Rut",
    )   
    tipo_documento=fields.Many2one(
        comodel_name="res.partner",
        string="Tipo de Documento",
        copy=False,
        index=True,
    )
    folio_documento = fields.Many2one(
        comodel_name="res.partner",
        string="Folio",
        copy=False,
        index=True,
    )    
    date_start = fields.Date(
        string="Fecha contable",
        help="Date when the user initiated the request.",
        default=fields.Date.context_today,
    )
    referencia_pago = fields.Char(
        string="Referencia de pago",
        help="La referencia de pago para establecer en apuntes de diario.",
    )
    fecha_factura = fields.Date(
        string="Fecha factura",
        default=fields.Date.context_today
    )
    codigo_documento = fields.Many2one(
        comodel_name="res.partner",
        string="Número del documento",
    )
    razon_social = fields.Many2one(
        comodel_name="res.partner",
        copy=False,
        index=True,
        string="Razón social",
    )
    l10n_cl_company_activities_id = fields.Many2one(
        comodel_name = 'res.partner',
        string="giro actividades"
    )
    acuseRecibo = fields.Selection(
        selection=[
            ('1','Pendiente de ser enviado'),
            ('2','Aceptado'),
            ('3','Consultar Estado Doc'),
            ('4','Aceptado con reparos'),
            ('5','Anulado'),
            ('6','Rechazado'),
            ('7','Manual'),
        ],
        string='acusoRecibo',
        required=True,
        readonly=False,
        copy=False,
        default='7',
    )
    trackId = fields.Integer('Id de seguimiento')
    date = fields.Date(
        'Starting Date', 
        required=True, 
        default=date.today()
    )
    state = fields.Selection(
        selection=[
        ('1', 'Draft'),
        ('2', 'Running')
        ],
        default='1',
        string='estado'
    )
    montoNeto = fields.Float(
        'monto neto sin iva',
        default=0
    )
    montoIvaRecuperable = fields.Float(
        'monto con iva incluido',
        default=0.19,
        readonly=True
    )
    monto_Total = fields.Float(
        'Monto Total',
        default=0
    )
    proveedor_id = fields.Many2one ( 
        comodel_name='new_module.proveedores',
        string = 'Proveedores'
    )
    @api.model
    def cargarDocumentos(self, *post):
        os.system('cls')
        listaRut=[]
        conn = psycopg2.connect(database="zonaTesting", user = "zonaTesting", password = "admin", host = "localhost", port = "5432")
        cur = conn.cursor()
        f = open("C:/tools/respaldoBaseDatos/doc_SII_202301", "r")
        archivoJSON = f.read()
        datosJSON = json.loads(archivoJSON)
        for ingreso in (datosJSON["ventas"]["detalleVentas"]):
            lax=[]
            try:
                if ingreso["acuseRecibo"]!=None:
                    acuse=ingreso["acuseRecibo"]
            except:
                acuse=""
            lax= ingreso["tipoDTEString"],str(ingreso["tipoDTE"]),ingreso["tipoCompra"],ingreso["rutCliente"],ingreso["razonSocial"],str(ingreso["folio"]),ingreso["fechaEmision"],ingreso["fechaRecepcion"],str(acuse),str(ingreso["montoExento"]),str(ingreso["montoNeto"]),str(ingreso["montoIvaRecuperable"]),str(ingreso["montoTotal"]),str(ingreso["ivaNoRetenido"]),str(ingreso["totalOtrosImpuestos"]),str(ingreso["valorOtroImpuesto"]),str(ingreso["tasaOtroImpuesto"]), str(ingreso["tipoDocReferencia"]),str(ingreso["trackId"]),ingreso["referencias"],ingreso["referenciado"],ingreso["reparos"],ingreso["otrosImpuestos"],ingreso["estado"]
            listaRut.append(lax)
        query = "select rutCliente,folio from borradores;" 
        cur.execute(query)
        querySelect = cur.fetchall()
        largoQuery=len(querySelect)
        for i in range(len(listaRut)): 
            existe=True
            if largoQuery==0:
                existe=False
            else: 
                existe=True
                for j in range(largoQuery):
                    if str(listaRut[i][3])==str(querySelect[j][0]) and str(listaRut[i][5])==str(querySelect[j][1]):
                        existe=True
                        break
                    else:
                        existe=False
            if existe==False:
                cur.execute("insert into borradores (tipoDTEstring,tipoDTE,tipoCompra,rutCliente,razonSocial,folio,fechaEmision,fechaRecepcion,acuseRecibo,montoExento,montoNeto,montoIvaRecuperable,montoTotal,ivaNoRetenido,totalOtrosImpuestos,valorOtroImpuesto,tasaOtroImpuesto,tipoDocReferencia,trackId,referencias,referenciado,reparos,otrosImpuestos,estado) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+",'"+str(listaRut[i][2])+"','"+str(listaRut[i][3])+"','"+str(listaRut[i][4])+"',"+str(listaRut[i][5])+",'"+str(listaRut[i][6])+"','"+str(listaRut[i][7])+"','"+str(listaRut[i][8])+"','"+str(listaRut[i][9])+"','"+str(listaRut[i][10])+"','"+str(listaRut[i][11])+"','"+str(listaRut[i][12])+"','"+str(listaRut[i][13])+"','"+str(listaRut[i][14])+"','"+str(listaRut[i][15])+"','"+str(listaRut[i][16])+"','"+str(listaRut[i][17])+"','"+str(listaRut[i][18])+"','"+str(listaRut[i][19])+"','"+str(listaRut[i][20])+"','"+str(listaRut[i][21])+"','"+str(listaRut[i][22])+"','"+str(listaRut[i][23])+"');")
                cur.execute(query)
                querySelect = cur.fetchall()
                largoQuery=len(querySelect)
                print("query despues del ciclo parte 2 => "+str(largoQuery))
        conn.commit()
        print("script completado")
        conn.close()
