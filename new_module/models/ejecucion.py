import json, os ,psycopg2
os.system('cls')
auxlistarut=[]
auxlistafolio=[]
listaJSON=[]
numero=0
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