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
conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")

cur = conn.cursor()

query = "select * from documentos;"


cur.execute(query)
rows = cur.fetchall()
for odoo in auxlista:
    for columnas in rows:
        if odoo[0]!=columnas[1]:
            print("ejecucion")
conn.commit()
print ("Records created successfully");
conn.close()

