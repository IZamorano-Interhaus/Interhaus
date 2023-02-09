import json,os
os.system('clear')
cliente = {
    "nombre": "Nora",
    "edad": 56,
    "id": "45355",
    "color_ojos": "verdes",
    "usa_lentes": False
}
datos_pruebas = """
{
	"ordenes": [ 
		{
			"tamano": "mediana",
			"precio": 15.67,
			"toppings": ["champinones", "pepperoni", "albahaca"],
			"queso_extra": false,
			"delivery": true,
			"cliente": {
				"nombre": "Jane Doe",
				"telefono": null,
				"correo": "janedoe@email.com"
			}
		},
		{
			"tamano": "pequena",
			"precio": 6.54,
			"toppings": null,
			"queso_extra": true,
			"delivery": false,
			"cliente": {
				"nombre": "Foo Jones",
				"telefono": "556-342-452",
				"correo": null
			}
		}
	]
}
        
"""
datos_pruebas_JSON = json.dumps(datos_pruebas)
print("------------------------------------------------------------------------------------------------------------------")
print(datos_pruebas_JSON)
datos_jaison = json.loads(datos_pruebas)
print("------------------------------------------------------------------------------------------------------------------")
print(datos_jaison)
cliente_JSON = json.dumps(cliente, indent=4)
print("------------------------------------------------------------------------------------------------------------------")
print(cliente_JSON)
cliente_JSON= json.dumps(cliente,sort_keys=True)
print("------------------------------------------------------------------------------------------------------------------")
print(cliente_JSON)
cliente_JSON=json.dumps(cliente,indent=4,sort_keys=True)
print("------------------------------------------------------------------------------------------------------------------")
print(cliente_JSON)



# Abrir el archivo ordenes.json
with open("/home/nicolas/Documentos/ordenes.json") as archivo:
    # Cargar su contenido y crear un diccionario
    datos = json.load(archivo) 
# Abir (o crear) un archivo ordenes_nuevo.json 
# y guardar la nueva versión de la información
with open("ordenes_nuevo.json", 'w') as archivo_nuevo:
    json.dump(datos, archivo_nuevo)
print("------------------------------------------------------------------------------------------------------------------")
print("-------------------------------llamar un dato dentro de un archivo -----------------------------------------------")
print("------------------------------------------------------------------------------------------------------------------")
print(datos["ordenes"][0]["toppings"])
print(datos["ordenes"][0]["cliente"]["nombre"])
with open("/home/nicolas/Documentos/new 2.json") as archivo:
    # Cargar su contenido y crear un diccionario
    datos = json.load(archivo)
# Abrir (o crear) un archivo ordenes_nuevo.json 
# y guardar la nueva versión de la información
with open("new 2.json", 'w') as archivo_nuevo:
    json.dump(datos, archivo_nuevo)
print("------------------------------------------------------------------------------------------------------------------")
print("-------------------------------llamar un dato dentro de un archivo -----------------------------------------------")
print("------------------------------------------------------------------------------------------------------------------")

print(datos["caratula"])


    

    
        
    