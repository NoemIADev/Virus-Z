from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date

import psycopg
from DB import get_conn


app = FastAPI(title="Virus Z API")

# =====================
# MODELS (schemas)
# =====================

class Quarantaine(BaseModel):
    zone: str
    date_debut: date


class Lieu(BaseModel):
    inconnu: bool
    adresse: Optional[str] = None
    code_postal: Optional[str] = None
    ville: Optional[str] = None


class Lieux(BaseModel):
    domicile: Lieu
    travail: Lieu


class CaseCreate(BaseModel):
    nom: str
    prenom: str
    age: int
    sexe: str
    date_infection_estimee: date
    virus_contracte: str
    mise_en_quarantaine: bool
    quarantaine: Optional[Quarantaine] = None
    lieux: Optional[Lieux] = None


# =====================
# ROUTES
# =====================

@app.post("/cases")
def create_case(case: CaseCreate):
    # 1) depliér les données de la requete en variables simples pour faciliter l'INSERT en DB
    quarantaine_zone = None
    quarantaine_date_debut = None

    domicile_inconnu = None
    domicile_adresse = None
    domicile_code_postal = None
    domicile_ville = None

    travail_inconnu = None
    travail_adresse = None
    travail_code_postal = None
    travail_ville = None

    if case.mise_en_quarantaine:
        if not case.quarantaine:
            raise HTTPException(status_code=422, detail="quarantaine est obligatoire si mise_en_quarantaine=true")
        quarantaine_zone = case.quarantaine.zone
        quarantaine_date_debut = case.quarantaine.date_debut
        # lieux restent NULL
    else:
        if not case.lieux:
            raise HTTPException(status_code=422, detail="lieux est obligatoire si mise_en_quarantaine=false")

        domicile_inconnu = case.lieux.domicile.inconnu
        domicile_adresse = case.lieux.domicile.adresse
        domicile_code_postal = case.lieux.domicile.code_postal
        domicile_ville = case.lieux.domicile.ville

        travail_inconnu = case.lieux.travail.inconnu
        travail_adresse = case.lieux.travail.adresse
        travail_code_postal = case.lieux.travail.code_postal
        travail_ville = case.lieux.travail.ville
        # quarantaine reste NULL

    # 2) INSERT en DB
    sql = """
        INSERT INTO public.cas (
          nom, prenom, age, sexe, date_infection_estimee, virus_contracte, mise_en_quarantaine,
          quarantaine_zone, quarantaine_date_debut,
          domicile_inconnu, domicile_adresse, domicile_code_postal, domicile_ville,
          travail_inconnu, travail_adresse, travail_code_postal, travail_ville
        )
        VALUES (
          %(nom)s, %(prenom)s, %(age)s, %(sexe)s, %(date_infection_estimee)s, %(virus_contracte)s, %(mise_en_quarantaine)s,
          %(quarantaine_zone)s, %(quarantaine_date_debut)s,
          %(domicile_inconnu)s, %(domicile_adresse)s, %(domicile_code_postal)s, %(domicile_ville)s,
          %(travail_inconnu)s, %(travail_adresse)s, %(travail_code_postal)s, %(travail_ville)s
        )
        RETURNING id;
    """
    print(sql)
    params = {
        "nom": case.nom,
        "prenom": case.prenom,
        "age": case.age,
        "sexe": case.sexe,
        "date_infection_estimee": case.date_infection_estimee,
        "virus_contracte": case.virus_contracte,
        "mise_en_quarantaine": case.mise_en_quarantaine,

        "quarantaine_zone": quarantaine_zone,
        "quarantaine_date_debut": quarantaine_date_debut,

        "domicile_inconnu": domicile_inconnu,
        "domicile_adresse": domicile_adresse,
        "domicile_code_postal": domicile_code_postal,
        "domicile_ville": domicile_ville,

        "travail_inconnu": travail_inconnu,
        "travail_adresse": travail_adresse,
        "travail_code_postal": travail_code_postal,
        "travail_ville": travail_ville,
    }

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                new_id = cur.fetchone()[0]
                conn.commit()

        return {"status": "ok", "id": new_id}

    except psycopg.Error as e:
        # détail DB utile pendant dev
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

