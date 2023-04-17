# -*- coding: utf-8 -*-
import psycopg2,json,os,sys
import xml.etree.ElementTree as ET
from odoo import models, fields, api, _
from datetime import  date
from dateutil.relativedelta import *
class proveedores(models.Model):
    _name="new_module.proveedores"
    _description="borrador para los proveedores"
    name=fields.Many2one(
        comodel_name='res.partner',
        string = "Nombre proveedor",
        required=True
    )
    street=fields.Many2one(
        comodel_name='partner_id.street',
        string="Dirección",
        required=True
    )
    company_id=fields.Many2one(
        string="Compañia",
        comodel_name="res.company",
        required=True, 
        default=lambda self: self.env.company,
        store=True,
        index=True,
    )
    l10n_cl_sii_taxpayer_type_id = fields.Selection(
        selection=[
        ('1','IVA afecto 1° categoria'),
        ('2','Emisor de boleta 2da Categoria'),
        ('3','Consumidor final'),
        ('4','Extranjero')
        ],
        default='1', string = 'Tipo de contribuyente'
    )
    l10n_cl_sii_activity_description_id= fields.Many2one(
        comodel_name='res.partner',
        string="Giro",
        required=True
    )
    pruebas_id= fields.One2many(
        comodel_name='new_module.pruebas',
        inverse_name='proveedor_id',
        string='Borradores'
    )
    
            # return record
        # function to getting over dues
    @api.model
    def obtenerDataProveedor(self):
        try:
            archivo_xml= open('C:/Users/Interhouse HP/Desktop/zonaTesting/testeos/zonaPython/xmlPruebas/prueba4.xml')
            datosProveedor = []
            conn = psycopg2.connect(database="zonaTesting", user = "zonaTesting", password = "admin", host = "localhost", port = "5432")
            cur = conn.cursor()
            if archivo_xml.readable:
                dato_xml = ET.fromstring(archivo_xml.read())
                nodoSetDTE = dato_xml.find('{http://www.sii.cl/SiiDte}SetDTE')
                nodoDTE = nodoSetDTE.find('{http://www.sii.cl/SiiDte}DTE')
                nodoDocumento = nodoDTE.find('{http://www.sii.cl/SiiDte}Documento')
                nodoEncabezado = nodoDocumento.find('{http://www.sii.cl/SiiDte}Encabezado') 
                nodoEmisor = nodoEncabezado.find('{http://www.sii.cl/SiiDte}Emisor')
                datosProveedor=nodoEmisor.find('{http://www.sii.cl/SiiDte}RUTEmisor').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}DirOrigen').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}CmnaOrigen').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}RznSoc').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}GiroEmis').text
                query=self.env.cr.execute("""
                    SELECT vat,name,street FROM RES_PARTNER;
                """, {
                    'journal_ids': self.ids,
                })
                
                querySelect = cur.fetchall()
                largoQuery=len(querySelect)        
                existe=True
                for i in range(len(datosProveedor)):
                    if largoQuery==0:
                        existe=False
                    else: 
                        existe=True
                        for j in range(largoQuery):
                            if str(datosProveedor[0])==str(querySelect[j][1]) and str(datosProveedor[3])==str(querySelect[j][2]):
                                existe=True
                                print("existe un dato")
                                break
                            else:
                                existe=False
                                print("no existe el dato en la base")
                                continue
                    if existe==False:
                        if str(datosProveedor[0])==str(querySelect[i][1]) and str(datosProveedor[3])!=str(querySelect[i][2]):
                            cur.execute("update res_partner set vat='"+datosProveedor[0]+"', street='"+datosProveedor[1]+"', city='"+datosProveedor[2]+"',display_name ='"+datosProveedor[3]+"',name='"+datosProveedor[3]+"',l10n_cl_activity_description ='"+datosProveedor[4]+"',l10n_cl_sii_taxpayer_type_id=1 where  name= '"+datosProveedor[3]+"' and vat = '"+datosProveedor[0]+"';")
                            cur.execute(query)
                            querySelect = cur.fetchall()
                            print("se actualiza proveedor por el nombre distinto")
                            largoQuery=len(querySelect)
                        elif str(datosProveedor[0])!=str(querySelect[i][1]) and str(datosProveedor[3])==str(querySelect[i][2]):
                            cur.execute("update res_partner set vat='"+datosProveedor[0]+"', street='"+datosProveedor[1]+"', city='"+datosProveedor[2]+"',display_name ='"+datosProveedor[3]+"',name='"+datosProveedor[3]+"',l10n_cl_activity_description ='"+datosProveedor[4]+"',l10n_cl_sii_taxpayer_type_id=1 where  name= '"+datosProveedor[3]+"' and vat = '"+datosProveedor[0]+"';")
                            cur.execute(query)
                            querySelect = cur.fetchall()
                            print("se actualiza por rut distinto")
                            largoQuery=len(querySelect)
                        else:
                            cur.execute("insert into res_partner (vat, street, city,name,display_name ,l10n_cl_activity_description,l10n_cl_sii_taxpayer_type_id) values ('"+datosProveedor[0]+"','"+datosProveedor[1]+"','"+datosProveedor[2]+"','"+datosProveedor[3]+"','"+datosProveedor[3]+"','"+datosProveedor[4]+"',1);")
                            cur.execute(query)
                            querySelect = cur.fetchall()
                            print("se agrega nuevo proveedor")
                            largoQuery=len(querySelect)
                conn.commit()
                conn.close()
            else:
                print(False)
        except Exception as err:
            print(err)
        finally:
            archivo_xml.close()
