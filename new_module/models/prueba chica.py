import json,os
os.system('clear')
auxlista=list()
numero=0
with open("new 2.json") as archivo:
    auxdiccionario = json.load(archivo)
with open("new 2.json", 'w') as archivo_nuevo:
    json.dump(auxdiccionario, archivo_nuevo)
for x in range(len(auxdiccionario["ventas"]["detalleVentas"])):
    numero+=1
    auxlista.append(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["rutCliente"]+" | "+str(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["folio"]))

