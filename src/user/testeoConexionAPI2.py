from urllib.request import urlopen
from pprint import pprint
import json, os
os.system('cls')
#fechaBuscada=input("ingresar fecha por año sin separadores, formato yyyymmdd\n")
#url=('https://api.covidtracking.com/v1/us/'+fechaBuscada+'.json')
urlPrueba='http://apigateway.cl/api/v1/sii/contribuyentes/situacion_tributaria/tercero/:rut?formato=json'
solicitud = urlopen(urlPrueba).read().decode('utf-8')

respuesta = json.loads(solicitud)

pprint(solicitud)

#print('cantidad de posts =>',len(solicitud))