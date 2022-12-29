import os
def leerArchivo():
    os.system('cls')
    contador=0
    for linea in archivo:
        contador +=1
        print(str(contador)+"."+linea)
        linea=archivo.readline()
    archivo.close()
    input("instrucciones ejecutadas")
def escribirArchivo():
    os.system('cls')
    nombre.write(input("escriba lo que quieras por aqui.\n"))
    nombre.close()
    input("Presione Entre para Finalizar. . . ")
os.system('cls')
try:
    print("introduccion al programa")
    archivo =open(input("archivo de texto por favor\n"))
    leerArchivo()
    condicion=input("desea escribir archivo? si/no")
    if condicion=="si":
        nombre = open(input("escribe el texto\n"), "w")
        escribirArchivo()
        print("fin programa")
    elif condicion=="no":
        print("fin programa")
except:
    print("error fatal, aplicacion caida")