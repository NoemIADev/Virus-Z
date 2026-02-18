import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

print("DB_HOST =", os.getenv("DB_HOST"))
print("DB_PORT =", os.getenv("DB_PORT"))
print("DB_USER =", os.getenv("DB_USER"))
print("DB_NAME =", os.getenv("DB_NAME"))

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),  # <-- ✅ PAS dbname
)

cur = conn.cursor()

cur.execute("SELECT DATABASE();")
print("Connecté à :", cur.fetchone()[0])

cur.execute("SHOW TABLES LIKE 'cas';")
print("Table 'cas' :", cur.fetchall())

cur.execute("SHOW TABLES LIKE 'virus';")
print("Table 'virus' :", cur.fetchall())

cur.close()
conn.close()
print("✅ Connexion OK")
