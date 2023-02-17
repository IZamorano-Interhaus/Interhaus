
import psycopg2

conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")

cur = conn.cursor()

query = "select * from documentos;"
cur.execute("INSERT INTO documentos (rut,folio) \
      VALUES ('19669468-4',5617);");

cur.execute("INSERT INTO documentos (rut,folio) \
      VALUES ('72893782-2',5097);");

cur.execute("INSERT INTO documentos (rut,folio) \
      VALUES ('18679478-7',2533);");

cur.execute("INSERT INTO documentos (rut,folio) \
      VALUES ('10709562-4',2195);");

cur.execute(query)
rows = cur.fetchall()
for row in rows:
   print ("ID = ", row[0])
   print ("rut = ", row[1])
   print ("folio = ", row[2], "\n")
print(len(rows))
conn.commit()
print ("Records created successfully");
conn.close()

