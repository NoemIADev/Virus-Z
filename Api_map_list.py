from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error as MySQLError
from DB import get_conn
import random
app = FastAPI(title="Virus Z API")

def fetch_cases(sql: str, params: dict = None):
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        cur.execute(sql, params or {})
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows

    except MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cases/map")
def list_cases_for_map():

    sql = """
        SELECT 
            v.id AS virus_id,
            v.nom AS virus_nom,
            v.contagiosite,
            da.latitude,
            da.longitude
        FROM cas c
        JOIN virus v ON c.virus_id = v.id
        JOIN adresse da ON c.domicile_adresse_id = da.id
        WHERE da.latitude IS NOT NULL AND da.longitude IS NOT NULL
    """

    rows = fetch_cases(sql)
    if not rows:
        return []
    # Générer une couleur unique par virus
    virus_colors = {}
    def random_color():
        return "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)])

    for row in rows:
        virus_colors.setdefault(row["virus_nom"], random_color())

    map_data = []
    for row in rows:
        map_data.append({
            "virus": row["virus_nom"],
            "contagiosite": row["contagiosite"],
            "lat": float(row["latitude"]),
            "lon": float(row["longitude"]),
            "color": virus_colors[row["virus_nom"]]
        })

    return map_data

@app.get("/cases/full")
def list_cases_full():

    sql = """
        SELECT 
            c.id,
            c.nom,
            c.prenom,
            c.age,
            c.sexe,
            c.date_infection_estimee,
            v.nom AS virus_nom,
            v.variante AS virus_variante,
            v.contagiosite,
            v.mode_propagation,
            v.incubation_min,
            v.incubation_max,
            v.moyens_detection,
            v.commentaire AS virus_commentaire,
            c.mise_en_quarantaine,
            c.quarantaine_date_debut,
            lq.nom AS lieu_quarantaine_nom,
            lq.type AS lieu_quarantaine_type,
            da.ligne1 AS domicile_ligne1,
            da.code_postal AS domicile_cp,
            da.ville AS domicile_ville,
            da.latitude AS domicile_latitude,
            da.longitude AS domicile_longitude,
            ta.ligne1 AS travail_ligne1,
            ta.code_postal AS travail_cp,
            ta.ville AS travail_ville,
            ta.latitude AS travail_latitude,
            ta.longitude AS travail_longitude
        FROM cas c
        JOIN virus v ON c.virus_id = v.id
        LEFT JOIN lieu_quarantaine lq ON c.lieu_quarantaine_id = lq.id
        LEFT JOIN adresse da ON c.domicile_adresse_id = da.id
        LEFT JOIN adresse ta ON c.travail_adresse_id = ta.id
    """

    return fetch_cases(sql)

