# duplicacion de los ruts con razones sociales distintas
import xml.etree.ElementTree as ET
import psycopg2, os
try:
    archivo_xml= open('C:/Users/Interhouse HP/Desktop/zonaTesting/testeos/zonaPython/xmlPruebas/prueba3.xml')
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
        query = "select id, vat,name from res_partner;" 
        cur.execute(query)
        querySelect = cur.fetchall()
        largoQuery=len(querySelect)        
        existe=True
        for i in range(largoQuery):
            if largoQuery==0:
                existe=False
                break
            else: 
                existe=True
                for j in range(len(datosProveedor)):
                    if datosProveedor[0]==str(querySelect[j][1]) and datosProveedor[3]==str(querySelect[2]):
                        existe=True
                        print("existe un dato")
                        break
                    else:
                        existe=False
                        print('no existe dato')
                        continue
                break
        if existe==False:
            if str(datosProveedor[3])!=str(querySelect[0][2]) and str(datosProveedor[0])!=str(querySelect[0][1]):
                cur.execute("insert into res_partner (vat, street, city,name,display_name ,l10n_cl_activity_description,l10n_cl_sii_taxpayer_type) values ('"+datosProveedor[0]+"','"+datosProveedor[1]+"','"+datosProveedor[2]+"','"+datosProveedor[3]+"','"+datosProveedor[3]+"','"+datosProveedor[4]+"',1);")
                cur.execute(query)
                querySelect = cur.fetchall()
                print("se agrega nuevo proveedor")
                largoQuery=len(querySelect)
            elif str(datosProveedor[3])==str(querySelect[0][2]) and str(datosProveedor[0])!=str(querySelect[0][1]):
                cur.execute("update res_partner set vat='"+datosProveedor[0]+"', street='"+datosProveedor[1]+"', city='"+datosProveedor[2]+"',display_name ='"+datosProveedor[3]+"',name='"+datosProveedor[3]+"',l10n_cl_activity_description ='"+datosProveedor[4]+"',l10n_cl_sii_taxpayer_type=1 where  name= '"+datosProveedor[3]+"' and vat = '"+datosProveedor[0]+"';")
                cur.execute(query)
                querySelect = cur.fetchall()
                print("se actualiza por rut distinto")
                largoQuery=len(querySelect)              
        conn.commit()
        conn.close()
    else:
        print(False)
except Exception as err:
    print(err)
finally:
    archivo_xml.close()