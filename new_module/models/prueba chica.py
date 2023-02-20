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
    lax=ingreso["rutCliente"],str(ingreso["folio"])
    listaRut.append(lax)
cur.execute("drop table if exists auxdoc;")
cur.execute("create table auxdoc (id serial, rut varchar(15),folio int);")
query = "select * from auxdoc;"
cur.execute(query)
querySelect = cur.fetchall()
print(len(querySelect))
for i in range(len(listaRut)):
    existe=False
    if (len(querySelect))==0:
        cur.execute("insert into auxdoc (rut,folio)values('61002000-3',5617);")
    elif len(querySelect)!=0: 
        for j in range(len(querySelect)):
            if listaRut[i][0]!=querySelect[j][1] and listaRut[i][1]!=querySelect[j][2]:
                l.append(listaRut[0][0]+listaRut[0][1])
        print(i)
    existe=True
    
    if existe==True:
        cur.execute("insert into auxdoc (rut,folio) values('"+str(l[i][0])+"',"+str(l[i][1])+");")
    
        # if listaRut[i][0]!=querysql[j][1] and listaRut[i][1]!=querysql[j][2]:
        #     # insert = "insert into documentos (rut,folio) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+");"           
        #     # cur.execute(insert)
        #     l.append(str(listaRut[i-1][0])+"',"+str(listaRut[i-1][1]))
        #     cur.execute("insert into auxdoc (rut,folio) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+");")
        # elif listaRut[i][1]!=querysql[j][2]:
        #     # cur.execute(insert)
        #     l.append(str(listaRut[i-1][0])+"',"+str(listaRut[i-1][1]))
        #     cur.execute("insert into auxdoc (rut,folio) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+");")
        # elif listaRut[i][0]!=querysql[j][1] and listaRut[i][1]!=querysql[j][2]:
        #     l.append(str(listaRut[i-1][0])+"',"+str(listaRut[i-1][1]))
        #     cur.execute("insert into auxdoc (rut,folio) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+");")
print(l)
print(len(l))
print("tiempo de espera")
print("------------------------------------------------------------------------")
print("inicio segundo ciclo")
for columna in l:
    if l.count(columna)>1:
        l.remove(columna)
print(l)
print(len(l))
conn.commit()
print ("Records created successfully");
conn.close()