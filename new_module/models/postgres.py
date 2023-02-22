# -*- coding: utf-8 -*-
import psycopg2

conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")

cur = conn.cursor()

query = "select * from auxdoc;"


cur.execute("INSERT INTO auxdoc (rut,folio) \
      VALUES ('19669468-4',3421);");

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

