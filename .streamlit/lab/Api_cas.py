from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date

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
    # pour l’instant on fait juste un echo
    return {
        "status": "ok",
        "case": case
    }

