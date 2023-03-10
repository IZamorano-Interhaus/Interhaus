# -*- coding: utf-8 -*-
import psycopg2,json,os,sys
import xml.etree.ElementTree as ET
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError
from datetime import  date
class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module' 
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
        copy=False,
        index=True,
    )
    rut_tributario = fields.Char(
        string="Rut",
    )   
    tipo_documento=fields.Many2one(
        comodel_name="res.partner",
        string="Tipo de Documento",
        copy=False,
        index=True,
    )
    folio_documento = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Folio",
        copy=False,
        index=True,
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda l: l.env.company.id
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
    terminos_pagos = fields.Many2one(
        comodel_name="account.move",
        string="Términos de Pago",
        copy=False,
        index=True,
    )
    codigo_documento = fields.Char(
        string="Número del documento",
    )
    razon_social = fields.Char(
        string="nombre de la empresa que emite factura o la razon social",
    )
    acuseRecibo = fields.Selection(
        selection=[
            ('not_sent', 'Pendiente de ser enviado'),
            ('accepted','Aceptado'),
            ('ask_for_status', 'Consultar Estado Doc'),
            ('objected','Aceptado con reparos'),
            ('cancelled','Anulado'),
            ('rejected', 'Rechazado'),
            ('manual','Manual ( borrador)'),
        ],
        string='acusoRecibo',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='manual',
    )
    trackId = fields.Integer('Id de seguimiento')
    journal_id = fields.Many2one(
        'account.move', 'Diario',
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Cuenta Analitica'
    )
    date = fields.Date(
        'Starting Date', 
        required=True, 
        default=date.today()
    )
    state = fields.Selection(
        selection=[('draft', 'Draft'),
        ('running', 'Running')],
        default='draft', string='estado'
    )
    partner_id = fields.Many2one(
        'res.partner', 
        'Partner',
    )
    company_currency_id = fields.Many2one(
        string='Company Currency',
        related='company_id.currency_id', readonly=True,
    )
    montoNeto = fields.Monetary('monto neto sin iva',
        compute='_compute_amount', currency_field='company_currency_id',store=True, readonly=True,)
    montoIvaRecuperable = fields.Monetary('monto con iva incluido',
        compute='_compute_amount',currency_field='company_currency_id', store=True, readonly=True,)
    monto_Total = fields.Monetary('Monto',compute='_compute_amount',currency_field='company_currency_id', store=True, readonly=True,)

    def funcion(self):
        raise ValidationError("hola gente")
    
    def cargarDocumentos(self, *post):
        
        os.system('cls')
        listaRut=[]
        conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")
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
    def obtenerDatosVista(self, container):
        contenedor = container['records'].filtered(lambda move: move.line_ids)
        if not contenedor:
            return

        # /!\ As this method is called in create / write, we can't make the assumption the computed stored fields
        # are already done. Then, this query MUST NOT depend on computed stored fields.
        # It happens as the ORM calls create() with the 'no_recompute' statement.
        
        self._cr.execute('''
            select  tipodte codigo_documento,
                    tipodtestring tipo_documento,
                    rutCliente rut_tributario, 
                    folio folio_documento,
                    fechaemision date_start,
                    fecharecepcion fecha_factura,
                    razonsocial razon_social,
                    acuserecibo acuseRecibo,
                    montoNeto montoNeto,
                    montoivarecuperable Impuesto,
                    montototal total,
                    trackid
              FROM borradores 
              ;
        ''', [tuple(contenedor.ids)])

        return self._cr.fetchall()

            # return record
        # function to getting over dues
    def obtenerDataProveedor():
        import xml.etree.ElementTree as ET
        import psycopg2, os
        try:
            archivo_xml= open('C:/Users/Interhouse HP/Desktop/zonaTesting/testeos/zonaPython/xmlPruebas/prueba1.xml')
            
            datosProveedor = []
            conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")
            cur = conn.cursor()
            if archivo_xml.readable:
                dato_xml = ET.fromstring(archivo_xml.read())
                nodoSetDTE = dato_xml.find('{http://www.sii.cl/SiiDte}SetDTE')
                nodoDTE = nodoSetDTE.find('{http://www.sii.cl/SiiDte}DTE')
                nodoDocumento = nodoDTE.find('{http://www.sii.cl/SiiDte}Documento')
                nodoEncabezado = nodoDocumento.find('{http://www.sii.cl/SiiDte}Encabezado') 
                nodoEmisor = nodoEncabezado.find('{http://www.sii.cl/SiiDte}Emisor')
                datosProveedor=nodoEmisor.find('{http://www.sii.cl/SiiDte}RUTEmisor').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}DirOrigen').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}CmnaOrigen').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}RznSoc').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}GiroEmis').text
                print(datosProveedor)
                query = "select vat from res_partner;" 
                cur.execute(query)
                querySelect = cur.fetchall()
                largoQuery=len(querySelect)        
                existe=True
                for i in datosProveedor:
                    if largoQuery==0:
                        existe=False
                    else: 
                        existe=True
                        for j in range(largoQuery):
                            if str(datosProveedor[0])==str(querySelect[j][0]):
                                existe=True
                                cur.execute("update res_partner set vat='"+datosProveedor[0]+"', street='"+datosProveedor[1]+"', city='"+datosProveedor[2]+"',display_name ='"+datosProveedor[3]+"',name='"+datosProveedor[3]+"',l10n_cl_activity_description ='"+datosProveedor[4]+"' where vat='"+datosProveedor[0]+"';")
                                break
                            else:
                                existe=False
                    if existe==False:
                        cur.execute("insert into res_partner (id,vat, street, city,name,display_name ,l10n_cl_activity_description) values (1,'"+datosProveedor[0]+"','"+datosProveedor[1]+"','"+datosProveedor[2]+"','"+datosProveedor[3]+"','"+datosProveedor[3]+"','"+datosProveedor[4]+"');")
                        cur.execute(query)
                        querySelect = cur.fetchall()
                        largoQuery=len(querySelect)
                    conn.commit()
                conn.close()
            else:
                print(False)
        except Exception as err:
            print(err)
        finally:
            archivo_xml.close()