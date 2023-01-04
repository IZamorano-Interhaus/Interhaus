from PIL import Image
import os
# aqui se crea el objeto que tendra la imagen
def mostrarImagen():
    im = Image.open(input("introduzca nombre del archivo: \n"))
    input("Imagen cargada, enter para continuar")
    im.show()
os.system('cls')

mostrarImagen()
respuesta= input("desea buscar otra imagen?")
while respuesta=="si":
    mostrarImagen()
    respuesta=input("otra mas: \n")

print("fin del programa")