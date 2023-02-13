import os
os.system('clear')

from psycopg2 import sql

conexion1 = sql.connect(database="interhuas_testing2", user="postgres", password="")
cursor1=conexion1.cursor()
createTable= "create table articulos(codigo serial, descripcion varchar(40),precio float,primary key (codigo));"
cursor1.execute(createTable)
insertar="insert into articulos(descripcion, precio) values (%s,%s)"
datos=("naranjas", 23.50)
cursor1.execute(insertar, datos)
datos=("peras", 34)
cursor1.execute(insertar, datos)
datos=("bananas", 25)
cursor1.execute(insertar, datos)
conexion1.commit()
conexion1.close() 