import xml.etree.ElementTree as ET
import os,psycopg2
try:
    os.system('cls')
    archivo_xml= open('C:/Users/Interhouse HP/Desktop/zonaTesting/testeos/zonaPython/xmlPruebas/prueba4.xml')
    datosProveedor = []
    if archivo_xml.readable:
        dato_xml = ET.fromstring(archivo_xml.read())
        nodoSetDTE = dato_xml.find('{http://www.sii.cl/SiiDte}SetDTE')
        nodoDTE = nodoSetDTE.find('{http://www.sii.cl/SiiDte}DTE')
        nodoDocumento = nodoDTE.find('{http://www.sii.cl/SiiDte}Documento')
        nodoEncabezado = nodoDocumento.find('{http://www.sii.cl/SiiDte}Encabezado') 
        nodoEmisor = nodoEncabezado.find('{http://www.sii.cl/SiiDte}Emisor')
        datosProveedor=nodoEmisor.find('{http://www.sii.cl/SiiDte}RUTEmisor').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}DirOrigen').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}CmnaOrigen').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}RznSoc').text,nodoEmisor.find('{http://www.sii.cl/SiiDte}GiroEmis').text
        print(datosProveedor)
        conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")
        cur = conn.cursor()
        query = "select vat,name, display_name,street,city,l10n_cl_activity_description from res_partner;" 
        cur.execute(query)
        querySelect = cur.fetchall()
        largoQuery=len(querySelect)
        for i in range(len(datosProveedor)): 
            existe=True
            if largoQuery==0:
                existe=False
            else: 
                existe=True
                for j in range(largoQuery):
                    if str(datosProveedor[i][0])==str(querySelect[j][0]) and str(datosProveedor[i][5])==str(querySelect[j][1]):
                        existe=True
                        break
                    else:
                        existe=False
            if existe==False:
                cur.execute("insert into res_partner(vat,name, display_name,street,city,l10n_cl_activity_description) values();")
                cur.execute(query)
                querySelect = cur.fetchall()
                largoQuery=len(querySelect)
                print("query despues del ciclo parte 2 => "+str(largoQuery))
        

        conn.commit()

        print("script completado")
        conn.close()
    else:
        print(False)
except Exception as err:
    print(err)
finally:
    archivo_xml.close()