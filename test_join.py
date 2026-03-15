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

sql = """
SELECT
    u.idUsuario AS id_usuario,
    it.idIntento AS id_intento,
    it.numeroIntento AS num_intento,
    c.nombre AS carrera,
    i.nombre AS institucion,
    oc.modalidad,
    oc.costoPension AS costo_pension,
    rc.afinidad
FROM usuario u
INNER JOIN intentotest it
    ON it.id_usuario = u.idUsuario
INNER JOIN recomendacion r
    ON r.id_intento = it.idIntento
INNER JOIN recomendacioncarrera rc
    ON rc.id_recomendacion = r.idRecomendacion
INNER JOIN carrera c
    ON c.idCarrera = rc.id_carrera
INNER JOIN ofertacarrera oc
    ON oc.id_carrera = c.idCarrera
INNER JOIN institucion i
    ON i.idInstitucion = oc.id_institucion
LIMIT 5;
"""

with conn.cursor() as cursor:
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)

conn.close()
