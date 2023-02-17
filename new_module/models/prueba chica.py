import json, os ,psycopg2
os.system('cls')
auxlistarut=[]
auxlistafolio=[]
listaJSON=[]
numero=0
numero2=0
with open("C:/tools/respaldoBaseDatos/SIIpruebas.json") as archivo:
    auxdiccionario = json.load(archivo)
with open("C:/tools/respaldoBaseDatos/SIIpruebas.json", 'w') as archivo_nuevo:
    json.dump(auxdiccionario, archivo_nuevo)
for x in range(len(auxdiccionario["ventas"]["detalleVentas"])):
    numero+=1
    auxlistarut.append(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["rutCliente"])
    auxlistafolio.append(str(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["folio"]))
    listaJSON.append(auxlistarut[0+(numero-1)]+" | "+str(auxlistafolio[0+(numero-1)]))
print(listaJSON)
conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")
cur = conn.cursor()
query = "select * from documentos;"
# insert = "insert into documentos (rut,folio) values("+auxlista+"",");"
cur.execute(query)
querysql = cur.fetchall()
for row in querysql:
   print ("ID = ", row[0])
   print ("rut = ", row[1])
   print ("folio = ", row[2], "\n")
numero=0
numero3=0
for i in range(len(listaJSON)):
    numero+=1
    for j in range(len(querysql)):
        if i==j:
            numero2+=1
            # cur.execute(insert)
    numero3+=numero2+1
print(numero)
print(numero2)
print(numero3)

conn.commit()
print ("Records created successfully");
conn.close()

