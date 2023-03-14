# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, modules


class Users(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']

    @api.model
    def systray_get_activities(self):
        """ Update the systray icon of res.partner activities to use the
        contact application one instead of base icon. """
        activities = super(Users, self).systray_get_activities()
        for activity in activities:
            if activity['model'] != 'res.partner':
                continue
            activity['icon'] = modules.module.get_module_icon('contacts')
        return activities
    
   
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
                        cur.execute("insert into res_partner (vat, street, city,name,display_name ,l10n_cl_activity_description) values ('"+datosProveedor[0]+"','"+datosProveedor[1]+"','"+datosProveedor[2]+"','"+datosProveedor[3]+"','"+datosProveedor[3]+"','"+datosProveedor[4]+"');")
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
