import json, os ,psycopg2
os.system('cls')
auxlista=[]
numero=0
numero2=0
with open("C:/tools/respaldoBaseDatos/SIIpruebas.json") as archivo:
    auxdiccionario = json.load(archivo)
with open("C:/tools/respaldoBaseDatos/SIIpruebas.json", 'w') as archivo_nuevo:
    json.dump(auxdiccionario, archivo_nuevo)
for x in range(len(auxdiccionario["ventas"]["detalleVentas"])):
    numero+=1
    auxlista.append(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["rutCliente"]+str(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["folio"]))
print(auxlista)
conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")
cur = conn.cursor()
query = "select * from documentos;"
insert = "insert into documentos (rut,folio) values(%s,%s);"
cur.execute(query)
rows = cur.fetchall()
for odoo in auxlista:
    numero2 +=1
    for columnas in rows:
        numero2+=1  
        print(numero2)
        if odoo[0]!=columnas[1]:
            
            numero2 +=1
            cur.execute(insert)
print(numero2)
for row in rows:
   print ("ID = ", row[0])
   print ("rut = ", row[1])
   print ("folio = ", row[2], "\n")
conn.commit()
print ("Records created successfully");
conn.close()

