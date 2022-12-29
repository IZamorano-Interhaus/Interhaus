import requests,os,json
os.system('cls')
API_KEY='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMWI4NjE4N2U5OWQ3NTUzZmJmYTQ2NjgzNGE2MGRhNjM5ZjNhNTgxOGY2NzgzYTIxYTdmYzdiMzhmMDY4ZTY3NmRiOGQzZGFmNjRhYWFlNWIiLCJpYXQiOjE2NzE0NTY1MDIsIm5iZiI6MTY3MTQ1NjUwMiwiZXhwIjo0ODI3MTMwMTAyLCJzdWIiOiIxMjQ1Iiwic2NvcGVzIjpbXX0.rtgycOioDCHHRvM9pjdDNPl6Gn-rwe_deyBRcO-2b-3DYCrHGvAM3bND8b45wKAqymslsRAMBL8vwcFA7WTZkqwWeVTDMT5A_T6PEPq7108IzfKWaEff1IUUprqQifMbtqBZMTRr06APrn52gJMkM9Y9KZOutU_1PlOF5Vz13p5SM4iFJPHrwsiZL_77YN9PCCcsRx2fGmOZi3hY-nOM0U-d1vLlDYOQTPgJYqCkZdAo6hkg_KSHq_DYBSzICAvO1_TUcM-O98srOJ7sgORj5GIDfTW1n6l-8qF7oOcoWSZKXCx5EN5f5H-NP3wANgzCPbzoHPpAJNeKYjDuNDBWGezt_DrEJP1ciaRAiofLlwtb8UidhT2e3bmaP6cny3qtyeW1CD11ABBU1vd9-gebqLc4rKHt5NesBQGVNeY0ZJTwNPFXK3_N8i6RozRZI3YsBlVloOvtOJvQcvtTST914Fu3Tp0J_qJDwwcj8scBvpyRHooddW1ZH54f8OqUQ0FOnCp5vfel_scB9O7xxDxTLhTOFLc6kIGBHcKc9p0jtgcw2efDfgBP4ASNYfdz4Cv9I06d6qSE3yyww-Fptk2QrzXCj2Z87PJI0bwwGHeQ21S6QVi-PMg-IFOiERh816GVWaA7TmS1jYOv5ldVcRjJaapJUn_JSIs2Ynhfl0HwMWI'
parametros = dict(key=API_KEY, text='Hello', lang='en-es')
urlAPI='http://apigateway.cl/api/v1/sii/contribuyentes/situacion_tributaria/tercero/:rut?formato=json'
#llave_atenticacion=input("introduzca la llave o token correspondiente.\n")
respuesta = requests.get(urlAPI, params=parametros)

os.system('cls')
if respuesta:
    print("Se ha establecido conexion => "+str(respuesta))
else:
    print("error en la conexion con la api.")
respuesta.headers



#respuestaJson= json.loads(res.text)
#origin = respuestaJson['rut']
#print()
#debe traer Nombre, Giro, Dirección, Comuna, Región, Teléfono, Email al ingresar el rut
