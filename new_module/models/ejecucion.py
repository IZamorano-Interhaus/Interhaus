import json, os 
os.system('cls')
f = open("C:/tools/respaldoBaseDatos/SIIpruebas.json", "r")
listaRut=[]
listaFolio=[]
listaConjunto=[]
archivoJSON = f.read()
datosJSON = json.loads(archivoJSON)
for ingreso in (datosJSON["ventas"]["detalleVentas"]):
    print("rut del cliente= "+ingreso["rutCliente"])
    print("folio: ")
    print(ingreso["folio"])
    listaRut.append(ingreso["rutCliente"])
    listaFolio.append(ingreso["folio"])
    listaConjunto.append(listaRut)
    listaConjunto.append(listaFolio)
print(listaRut)
print(listaRut[1])
print(listaRut[0][1])
print(listaFolio)
print(listaFolio[1])
print(str(listaFolio[0])[1])
print(listaConjunto)