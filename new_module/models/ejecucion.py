import json, os ,psycopg2
os.system('cls')
auxlista=[]
numero=0
with open("C:/tools/respaldoBaseDatos/SIIpruebas.json") as archivo:
    auxdiccionario = json.load(archivo)
with open("C:/tools/respaldoBaseDatos/SIIpruebas.json", 'w') as archivo_nuevo:
    json.dump(auxdiccionario, archivo_nuevo)
for x in range(len(auxdiccionario["ventas"]["detalleVentas"])):
    numero+=1
    auxlista.append(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["rutCliente"]+str(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["folio"]))
print(numero)
print(auxlista)