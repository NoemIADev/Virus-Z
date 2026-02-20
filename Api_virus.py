from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum, IntEnum
import mysql.connector
from mysql.connector import Error as MySQLError
from DB import get_conn
import json

app = FastAPI(title="Virus Z API")

class ModePropagation(str, Enum):
    morsure = "Morsure"
    sang = "Sang"
    mutation = "Mutation_secondaire"
    Griffure = "Griffure"
    Fluides = "Fluides"
    Aerein = "Aerien"

class MoyenDetection(str, Enum):
    symptome = "Symptômes"
    test_salivaire = "Test salivaire"
    PCR = "PCR"
    observation_comportementale = "Observation comportementale"
    Scan = "Scan"
    Test_adn = "test adn"

class ContagiositeLevel(IntEnum):
    Non_contagieux = 0
    faible = 1
    Fortement_contagieux = 2

class VirusCreate(BaseModel):
    nom: str
    variante: Optional[str] = ""  # ✅ table NOT NULL
    mode_propagation: ModePropagation
    incubation_min: int
    incubation_max: int
    contagiosite: ContagiositeLevel 
    moyens_detection: List[MoyenDetection]
    commentaire: Optional[str] = None

@app.post("/virus")
def create_virus(virus: VirusCreate):
    if virus.incubation_min > virus.incubation_max:
        raise HTTPException(
            status_code=422,
            detail="Incubation minimale doit être <= incubation maximale"
        )

    sql = """
        INSERT INTO virus (
            nom,
            variante,
            mode_propagation,
            incubation_min,
            incubation_max,
            contagiosite,
            moyens_detection,
            commentaire
        )
        VALUES (
            %(nom)s,
            %(variante)s,
            %(mode_propagation)s,
            %(incubation_min)s,
            %(incubation_max)s,
            %(contagiosite)s,
            %(moyens_detection)s,
            %(commentaire)s
        )
    """

    params = {
        "nom": virus.nom,
        "variante": virus.variante or "",  #pas None
        "mode_propagation": virus.mode_propagation.value,
        "incubation_min": virus.incubation_min,
        "incubation_max": virus.incubation_max,
        "contagiosite": virus.contagiosite.value,
        "moyens_detection": json.dumps([m.value for m in virus.moyens_detection]),
        "commentaire": virus.commentaire or ""
    }

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return {"status": "ok", "id": new_id}

    except MySQLError as e:
        try:
            cur.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass
        raise HTTPException(status_code=500, detail=f"DB error: {e}")