
import psycopg2

conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")

cur = conn.cursor()

query = "select * from documentos;"
cur.execute("INSERT INTO documentos (ID,rut,folio) \
      VALUES (1, '196694684', 32 );");

cur.execute("INSERT INTO documentos (ID,rut,folio) \
      VALUES (2, '72893782-2', 25);");

cur.execute("INSERT INTO documentos (ID,rut,folio) \
      VALUES (3, '18679478-7', 23);");

cur.execute("INSERT INTO documentos (ID,rut,folio) \
      VALUES (4, '10709562-4', 25);");

cur.execute(query)
rows = cur.fetchall()
for row in rows:
   print ("ID = ", row[0])
   print ("rut = ", row[1])
   print ("folio = ", row[2], "\n")

conn.commit()
print ("Records created successfully");
conn.close()

