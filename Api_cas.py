from datetime import date
from decimal import Decimal
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from mysql.connector import Error as MySQLError
from pydantic import BaseModel

from DB import get_conn

app = FastAPI(title="Virus Z API")

BAN_URL = "https://data.geopf.fr/geocodage/search/"
BAN_TIMEOUT = 8
UNKNOWN_CP = "00000"
UNKNOWN_CITY = "Inconnue"


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
# HELPERS
# =====================
def geocode_one(adresse: str, code_postal: str, ville: str) -> dict:
    """
    Vérifie une adresse via la BAN (Géoplateforme).
    - Si aucune adresse trouvée: HTTP 422.
    - Si l'API ne répond pas (timeout/réseau): HTTP 503.
    """
    q = f"{adresse} {code_postal} {ville}".strip()

    params = {
        "q": q,
        "limit": 1,
        "autocomplete": 0,    #autocomplete 1 = mode “suggestions” (par défaut) → bien pour taper vite 
                              # 0 = recherche plus “stricte” (souvent mieux pour valider une adresse complète)
        "index": "address",
    }

    try:
        response = requests.get(BAN_URL, params=params, timeout=BAN_TIMEOUT)
        response.raise_for_status()
    except requests.Timeout as exc:
        raise HTTPException(status_code=503, detail="Service adresse indisponible") from exc
    except requests.RequestException as exc:
        raise HTTPException(status_code=503, detail="Service adresse indisponible") from exc

    data = response.json()
    features = data.get("features", [])
    if not features:
        raise HTTPException(status_code=422, detail="Adresse introuvable")

    first = features[0]
    properties = first.get("properties", {})
    geometry = first.get("geometry", {})
    coordinates = geometry.get("coordinates", [])

    if len(coordinates) < 2:
        raise HTTPException(status_code=422, detail="Adresse introuvable")

    return {
        "label": properties.get("label", q),
        "longitude": coordinates[0],
        "latitude": coordinates[1],
    }


def insert_adresse(cur, ligne1: str, code_postal: str, ville: str, latitude=None, longitude=None) -> int:
    """Insère une adresse dans la table adresse et retourne son id."""
    cur.execute(
        """
        INSERT INTO adresse (ligne1, code_postal, ville, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (ligne1, code_postal, ville, latitude, longitude),
    )
    return cur.lastrowid


def get_virus_id(cur, virus_contracte: str) -> int:
    """Récupère l'id du virus par son nom."""
    cur.execute("SELECT id FROM virus WHERE nom = %s LIMIT 1", (virus_contracte,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=422, detail="Virus introuvable")
    return row[0]


def validate_lieu_fields(lieu: Lieu, nom_lieu: str) -> None:
    """Vérifie qu'une adresse non inconnue a bien adresse + code postal + ville."""
    if lieu.inconnu:
        return

    if not lieu.adresse or not lieu.code_postal or not lieu.ville:
        raise HTTPException(status_code=422, detail=f"Adresse {nom_lieu} incomplète")


# =====================
# ROUTE
# =====================
@app.post("/cases")
def create_case(case: CaseCreate):
    # Vérification de la structure reçue du front
    if case.mise_en_quarantaine:
        if not case.quarantaine:
            raise HTTPException(status_code=422, detail="quarantaine est obligatoire si mise_en_quarantaine=true")
    else:
        if not case.lieux:
            raise HTTPException(status_code=422, detail="lieux est obligatoire si mise_en_quarantaine=false")

    conn = None
    cur = None

    try:
        conn = get_conn()
        cur = conn.cursor()

        virus_id = get_virus_id(cur, case.virus_contracte)

        lieu_quarantaine_id = None
        quarantaine_date_debut = None
        domicile_adresse_id = None
        travail_adresse_id = None

        if case.mise_en_quarantaine:
            # Branche quarantaine
            zone = case.quarantaine.zone.strip()
            quarantaine_date_debut = case.quarantaine.date_debut

            # La table lieu_quarantaine exige une FK adresse_id.
            zone_adresse_id = insert_adresse(
                cur,
                ligne1=f"Zone quarantaine: {zone}",
                code_postal=UNKNOWN_CP,
                ville=UNKNOWN_CITY,
            )

            cur.execute(
                """
                INSERT INTO lieu_quarantaine (nom, type, adresse_id)
                VALUES (%s, %s, %s)
                """,
                (zone, "ZONE", zone_adresse_id),
            )
            lieu_quarantaine_id = cur.lastrowid

            # La table cas impose domicile_adresse_id NOT NULL.
            domicile_adresse_id = insert_adresse(
                cur,
                ligne1="Domicile inconnu (quarantaine)",
                code_postal=UNKNOWN_CP,
                ville=UNKNOWN_CITY,
            )

        else:
            # Branche hors quarantaine
            domicile = case.lieux.domicile
            travail = case.lieux.travail

            validate_lieu_fields(domicile, "domicile")
            validate_lieu_fields(travail, "travail")

            # Domicile
            if domicile.inconnu:
                domicile_adresse_id = insert_adresse(
                    cur,
                    ligne1="Domicile inconnu",
                    code_postal=UNKNOWN_CP,
                    ville=UNKNOWN_CITY,
                )
            else:
                geo_domicile = geocode_one(domicile.adresse, domicile.code_postal, domicile.ville)
                domicile_adresse_id = insert_adresse(
                    cur,
                    ligne1=geo_domicile["label"],
                    code_postal=domicile.code_postal,
                    ville=domicile.ville,
                    latitude=Decimal(str(geo_domicile["latitude"])),
                    longitude=Decimal(str(geo_domicile["longitude"])),
                )

            # Travail (optionnel si inconnu)
            if not travail.inconnu:
                geo_travail = geocode_one(travail.adresse, travail.code_postal, travail.ville)
                travail_adresse_id = insert_adresse(
                    cur,
                    ligne1=geo_travail["label"],
                    code_postal=travail.code_postal,
                    ville=travail.ville,
                    latitude=Decimal(str(geo_travail["latitude"])),
                    longitude=Decimal(str(geo_travail["longitude"])),
                )

        # Insertion finale du cas
        cur.execute(
            """
            INSERT INTO cas (
                nom,
                prenom,
                age,
                sexe,
                date_infection_estimee,
                virus_id,
                mise_en_quarantaine,
                lieu_quarantaine_id,
                quarantaine_date_debut,
                domicile_adresse_id,
                travail_adresse_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                case.nom,
                case.prenom,
                case.age,
                case.sexe,
                case.date_infection_estimee,
                virus_id,
                case.mise_en_quarantaine,
                lieu_quarantaine_id,
                quarantaine_date_debut,
                domicile_adresse_id,
                travail_adresse_id,
            ),
        )

        new_id = cur.lastrowid
        conn.commit()

        return {"status": "ok", "id": new_id}

    except HTTPException:
        if conn:
            conn.rollback()
        raise
    except MySQLError as exc:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur base de données: {exc}") from exc
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
