# -*- coding: utf-8 -*-
import json, os ,psycopg2,sys


if len(sys.argv) !=2:
    print("Error - Introduce los argumentos correctamente")
    print('Ejemplo: cargarDocumentos.py "nombreArchivoJSON"')
else:
    os.system('cls')
    listaRut=[]
    listajsonCorta=[]
    nombreArchivo=sys.argv[1]
    conn = psycopg2.connect(database="postgres", user = "postgres", password = "admin", host = "localhost", port = "5432")
    cur = conn.cursor()
    f = open(nombreArchivo, "r")
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
                if str(listaRut[i][3])==str(querySelect[j][0]):
                    existe=True
                    break
                else:
                    existe=False
        if existe==False:
            listajsonCorta.append(str(listaRut[i][0])+"',"+str(listaRut[i][1])+",'"+str(listaRut[i][2])+"','"+str(listaRut[i][3])+"','"+str(listaRut[i][4])+"',"+str(listaRut[i][5])+",'"+str(listaRut[i][6])+"','"+str(listaRut[i][7])+"','"+str(listaRut[i][8])+"','"+str(listaRut[i][9])+"','"+str(listaRut[i][10])+"','"+str(listaRut[i][11])+"','"+str(listaRut[i][12])+"','"+str(listaRut[i][13])+"','"+str(listaRut[i][14])+"','"+str(listaRut[i][15])+"','"+str(listaRut[i][16])+"','"+str(listaRut[i][17])+"','"+str(listaRut[i][18])+"','"+str(listaRut[i][19])+"','"+str(listaRut[i][20])+"','"+str(listaRut[i][21])+"','"+str(listaRut[i][22])+"','"+str(listaRut[i][23]))
            cur.execute("insert into borradores (tipoDTEstring,tipoDTE,tipoCompra,rutCliente,razonSocial,folio,fechaEmision,fechaRecepcion,acuseRecibo,montoExento,montoNeto,montoIvaRecuperable,montoTotal,ivaNoRetenido,totalOtrosImpuestos,valorOtroImpuesto,tasaOtroImpuesto,tipoDocReferencia,trackId,referencias,referenciado,reparos,otrosImpuestos,estado) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+",'"+str(listaRut[i][2])+"','"+str(listaRut[i][3])+"','"+str(listaRut[i][4])+"',"+str(listaRut[i][5])+",'"+str(listaRut[i][6])+"','"+str(listaRut[i][7])+"','"+str(listaRut[i][8])+"','"+str(listaRut[i][9])+"','"+str(listaRut[i][10])+"','"+str(listaRut[i][11])+"','"+str(listaRut[i][12])+"','"+str(listaRut[i][13])+"','"+str(listaRut[i][14])+"','"+str(listaRut[i][15])+"','"+str(listaRut[i][16])+"','"+str(listaRut[i][17])+"','"+str(listaRut[i][18])+"','"+str(listaRut[i][19])+"','"+str(listaRut[i][20])+"','"+str(listaRut[i][21])+"','"+str(listaRut[i][22])+"','"+str(listaRut[i][23])+"');")
            cur.execute(query)
            querySelect = cur.fetchall()
            largoQuery=len(querySelect)
            print("query despues del ciclo parte 2 => "+str(largoQuery))
    conn.commit()
    print("script completado 1")
    proveedores=cur.execute("select vat,name from res_partner;")

    listaPro=cur.fetchall()

    for i in range(len(listaPro)):
        cond = False
        for j in listajsonCorta:
            if listaPro[i]==j[3]:
                cond=True
                break
            else:
                cond=False
                conn.execute("insert into res_partner(vat,name,phone,mobile,email,website,category_id,l10n_cl_activity_description,l10n_cl_sii_taxpayer_type,l10n_latam_identification_type_id,l10n_cl_dte_email) ")
    conn.close()