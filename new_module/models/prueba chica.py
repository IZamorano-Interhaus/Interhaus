import json, os ,psycopg2
os.system('cls')
auxlista2=[]
auxlista1=[]
listaFinal=[]
listaRut=[]
conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")
cur = conn.cursor()
f = open("C:/tools/respaldoBaseDatos/SIIpruebas.json", "r")
archivoJSON = f.read()
datosJSON = json.loads(archivoJSON)
for ingreso in (datosJSON["ventas"]["detalleVentas"]):
    lax=[]
    lax=ingreso["rutCliente"],str(ingreso["folio"])
    listaRut.append(lax)
query = "select * from documentos;"
cur.execute(query)
querysql = cur.fetchall()
print(querysql)
for i in range(len(listaRut)):
    for j in range(len(querysql)):
        if listaRut[i][0]!=querysql[j][1]:
            insert = "insert into documentos (rut,folio) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+");"           
            cur.execute(insert)
            cur.execute("insert into auxdoc (rut,folio) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+");")
        else:
            cur.execute(insert)
            cur.execute("insert into auxdoc (rut,folio) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+");")
print("tiempo de espera")
print("------------------------------------------------------------------------")
print("inicio segundo ciclo")
for i in range(len(listaRut)):
    print(i)
    for j in range(len(querysql)):
        print(j)
        if listaRut[i][0]!=querysql[j][1]:
            cur.execute("insert into auxdoc (rut,folio) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+");")
        else:
            listaRut=listaFinal


for columna in querysql:
    print("id=",columna[0])
    print("rut=",columna[1])
    print("folio=",columna[2])
conn.commit()
print ("Records created successfully");
conn.close()