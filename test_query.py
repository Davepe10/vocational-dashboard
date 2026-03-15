import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    connect_timeout=10,
    ssl={"ssl": {}},
    cursorclass=pymysql.cursors.DictCursor,
)

with conn.cursor() as cursor:
    cursor.execute("SELECT 1 AS ok;")
    result = cursor.fetchone()
    print(result)

conn.close()
