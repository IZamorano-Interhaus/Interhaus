import psycopg2,os
os.system('clear')

con = psycopg2.connect(database="nicolas", user="nicolas", password="", host="localhost", port="5432")

print("Database opened successfully")