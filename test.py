import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

print("DB_NAME =", os.getenv("DB_NAME"))

conn = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)

with conn.cursor() as cur:
    cur.execute("SELECT current_database();")
    print("Connecté à :", cur.fetchone()[0])

    cur.execute("SELECT tablename FROM pg_tables WHERE tablename='cas';")
    print("Table cas :", cur.fetchall())

conn.close()
print("✅ Connexion OK")
