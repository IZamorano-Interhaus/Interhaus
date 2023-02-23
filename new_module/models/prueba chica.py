# -*- coding: utf-8 -*-
import json, os ,psycopg2
os.system('cls')
auxlista2=[]
auxlista1=[]
listaFinal=[]
listaRut=[]
l=[]
conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")
cur = conn.cursor()
f = open("C:/tools/respaldoBaseDatos/SIIpruebas.json", "r")
archivoJSON = f.read()
datosJSON = json.loads(archivoJSON)
for ingreso in (datosJSON["ventas"]["detalleVentas"]):
    lax=[]
    # if ingreso["acuseRecibo"]==None:
    #     ingreso["acuseRecibo"]=0
    # elif ingreso["folioDocReferencia"]==False:
    #     ingreso["folioDocReferencia"]=0
    # elif ingreso["acuseRecibo"]==None and ingreso["folioDocReferencia"]==None:
    #     ingreso["acuseRecibo"]=0
    #     ingreso["folioDocReferencia"]=0
    lax= ingreso["tipoDTEString"],str(ingreso["tipoDTE"]),ingreso["tipoCompra"],ingreso["rutCliente"],ingreso["razonSocial"],str(ingreso["folio"]),ingreso["fechaEmision"],ingreso["fechaRecepcion"],str(ingreso["acuseRecibo"]),str(ingreso["montoExento"]),str(ingreso["montoNeto"]),str(ingreso["montoIvaRecuperable"]),str(ingreso["montoTotal"]),str(ingreso["ivaNoRetenido"]),str(ingreso["totalOtrosImpuestos"]),str(ingreso["valorOtroImpuesto"]),str(ingreso["tasaOtroImpuesto"]), str(ingreso["tipoDocReferencia"]),str(ingreso["trackId"]),ingreso["referencias"],ingreso["referenciado"],ingreso["reparos"],ingreso["otrosImpuestos"],ingreso["estado"]
    listaRut.append(lax)
print(listaRut)
cur.execute("drop table if exists borradores;")
cur.execute("create table borradores (id serial, tipoDTEstring VARCHAR(50),tipoDTE int,tipoCompra VARCHAR(50),rutCliente VARCHAR(50),razonSocial VARCHAR(50),folio int,fechaEmision date,fechaRecepcion date,acuseRecibo VARCHAR(50),montoExento int,montoNeto int,montoIvaRecuperable float,montoTotal float,ivaNoRetenido float,totalOtrosImpuestos float,valorOtroImpuesto varchar(50),tasaOtroImpuesto varchar(50),tipoDocReferencia int,folioDocReferencia int,trackId bigint,referencias VARCHAR(50),referenciado VARCHAR(50),reparos VARCHAR(50),otrosImpuestos VARCHAR(50),estado VARCHAR(50)); ")
query = "select * from borradores;" 
cur.execute(query)
querySelect = cur.fetchall()
for i in range(len(listaRut)):
    existe=False
    if range(len(querySelect))==0:
        cur.execute("insert into borradores (rutCliente,folio)values('61002000-3',5617);")
        cur.execute("select * from borradores;")
    elif range(len(querySelect))!=0: 
        
        for j in range(len(querySelect)):
            if listaRut[i]["rutCliente"]!=querySelect[j]["rut"] and listaRut[i]["folio"]!=querySelect[j]["folio"]:
                l.append(listaRut[3]["rutCliente"]+listaRut[5]["folio"])
        existe=True
    if existe:
        cur.execute("insert into borradores (tipoDTEstring,tipoDTE,tipoCompra,rutCliente,razonSocial,folio,fechaEmision,fechaRecepcion,montoExento,montoNeto,montoIvaRecuperable,montoTotal,ivaNoRetenido,totalOtrosImpuestos,valorOtroImpuesto,tasaOtroImpuesto,tipoDocReferencia,trackId,referencias,referenciado,reparos,otrosImpuestos,estado) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+",'"+str(listaRut[i][2])+"','"+str(listaRut[i][3])+"','"+str(listaRut[i][4])+"',"+str(listaRut[i][5])+",'"+str(listaRut[i][6])+"','"+str(listaRut[i][7])+"','"+str(listaRut[i][8])+"','"+str(listaRut[i][9])+"','"+str(listaRut[i][10])+"','"+str(listaRut[i][11])+"','"+str(listaRut[i][12])+"','"+str(listaRut[i][13])+"','"+str(listaRut[i][14])+"','"+str(listaRut[i][15])+"',"+str(listaRut[i][16])+",'"+str(listaRut[i][17])+"','"+str(listaRut[i][18])+"','"+str(listaRut[i][19])+"','"+str(listaRut[i][20])+"','"+str(listaRut[i][21])+"','"+str(listaRut[i][22])+"');")
print(l)
conn.commit()
print ("Records created successfully");
conn.close()