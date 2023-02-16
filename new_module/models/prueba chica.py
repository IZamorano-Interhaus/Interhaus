import json
import psycopg2
auxlista=[]
numero=0
with open("C:/tools/respaldoBaseDatos/SIIpruebas.json") as archivo:
    auxdiccionario = json.load(archivo)
with open("C:/tools/respaldoBaseDatos/SIIpruebas.json", 'w') as archivo_nuevo:
    json.dump(auxdiccionario, archivo_nuevo)
for x in range(len(auxdiccionario["ventas"]["detalleVentas"])):
    numero+=1
    auxlista.append(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["rutCliente"]+str(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["folio"]))
print (auxlista)
conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")

cur = conn.cursor()

query = "select * from documentos;"
cur.execute("INSERT INTO documentos (ID,rut,folio) \
      VALUES (1, '196694684', 32 );");

cur.execute("INSERT INTO documentos (ID,rut,folio) \
      VALUES (2, '72893782-2', 25);");

cur.execute("INSERT INTO documentos (ID,rut,folio) \
      VALUES (3, '18679478-7', 23);");

cur.execute("INSERT INTO documentos (ID,rut,folio) \
      VALUES (4, '10709562-4', 25);");

cur.execute(query)
rows = cur.fetchall()
for row in rows:
   print ("ID = ", row[0])
   print ("rut = ", row[1])
   print ("folio = ", row[2], "\n")

conn.commit()
print ("Records created successfully");
conn.close()

