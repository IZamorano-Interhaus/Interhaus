import os
import webbrowser
os.system('cls')
ruta=input("introduzca el archivo pdf\n")

os.system(ruta)

rutaUrl= input("introduzca url=>   ")
#url de prueba = https://drive.google.com/file/d/1aPCvSi49PqQmvKNSxuEx8MhL6mOU-6mR/view?usp=share_link
webbrowser.open_new(rutaUrl)