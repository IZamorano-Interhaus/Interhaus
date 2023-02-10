import json,os
os.system('clear')
auxlista=list()
lista=[]
numero=0
with open("new 2.json") as archivo:
    # Cargar su contenido y crear un diccionario
    auxdiccionario = json.load(archivo)
# Abrir (o crear) un archivo ordenes_nuevo.json 
# y guardar la nueva versión de la información
with open("new 2.json", 'w') as archivo_nuevo:
    json.dump(auxdiccionario, archivo_nuevo)

print(auxdiccionario["ventas"]['resumenes'][0]["tipoDteString"])
print(auxdiccionario["ventas"]['resumenes'][-1]["tipoDteString"])
print(auxdiccionario["caratula"]['nombreMes'])
print(auxdiccionario["ventas"]['detalleVentas'][0]["rutCliente"],auxdiccionario["ventas"]['detalleVentas'][0]["folio"])
for x in range(len(auxdiccionario["ventas"]["detalleVentas"])):
    numero+=1
    
    auxlista.append(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["rutCliente"]+" | "+str(auxdiccionario["ventas"]['detalleVentas'][0+(numero-1)]["folio"]))
    



print(auxlista)
print("---------------------------------------------------------------------------------------------------------------")
diccionario = auxdiccionario.get("caratula")
print (diccionario)

    