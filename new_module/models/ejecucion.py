import psycopg2,json

conexion1 = psycopg2.connect(database="postgres", user="postgres", password="admin")

cursor1 = conexion1.cursor()
query = "insert into documentos(id,rut, folio) values (%s,%s,%s)"
dato=(1,"19669468-4",123456)
cursor1.execute(query,dato)
conexion1.commit()
conexion1.close()