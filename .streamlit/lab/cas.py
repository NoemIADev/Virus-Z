import streamlit as st
from datetime import date
import requests

st.title("🧟 Ajouter un cas (Virus Z)")

# =====================
# CONFIG (à adapter)
# =====================
DRY_RUN = True
# CASE_API = "http://localhost:8000"  # décommente si besoin

# =====================
# STATE
# =====================
def init_state():
    defaults = {
        "step": 1,

        # Etape 1
        "nom": "",
        "prenom": "",
        "age": 30,
        "sexe": "Masculin",
        "infection_date": date.today(),
        "virus_contracted": "",
        "mise_en_quarantaine": "Non",  # "Oui" ou "Non"

        # Etape 2 - quarantaine
        "zone_quarantaine": "",
        "date_debut_quarantaine": date.today(),

        # Etape 2 - lieux
        "domicile_inconnu": False,
        "domicile_adresse": "",
        "domicile_cp": "",
        "domicile_ville": "",

        "travail_inconnu": False,
        "travail_adresse": "",
        "travail_cp": "",
        "travail_ville": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def go(step: int):
    st.session_state.step = step
    st.rerun()


def on_change_quarantaine():
    """Quand on change Oui/Non, on reset l'autre branche pour éviter incohérences."""
    if st.session_state.mise_en_quarantaine == "Oui":
        # reset lieux
        st.session_state.domicile_inconnu = False
        st.session_state.domicile_adresse = ""
        st.session_state.domicile_cp = ""
        st.session_state.domicile_ville = ""

        st.session_state.travail_inconnu = False
        st.session_state.travail_adresse = ""
        st.session_state.travail_cp = ""
        st.session_state.travail_ville = ""
    else:
        # reset quarantaine
        st.session_state.zone_quarantaine = ""
        st.session_state.date_debut_quarantaine = date.today()


def validate_step1():
    errors = []
    if not st.session_state.virus_contracted.strip():
        errors.append("Le champ 'Virus contracté' est obligatoire.")
    if st.session_state.nom.strip() == "" or st.session_state.prenom.strip() == "":
        errors.append("Le nom et le prénom sont obligatoires.")
    return errors


def validate_step2():
    errors = []
    if st.session_state.mise_en_quarantaine == "Oui":
        if not st.session_state.zone_quarantaine.strip():
            errors.append("La zone de quarantaine est obligatoire.")
    else:
        # domicile
        if not st.session_state.domicile_inconnu:
            if not st.session_state.domicile_adresse.strip():
                errors.append("Adresse domicile obligatoire (ou coche 'Domicile inconnu').")
            if not st.session_state.domicile_cp.strip():
                errors.append("Code postal domicile obligatoire (ou coche 'Domicile inconnu').")
            if not st.session_state.domicile_ville.strip():
                errors.append("Ville domicile obligatoire (ou coche 'Domicile inconnu').")

        # travail
        if not st.session_state.travail_inconnu:
            if not st.session_state.travail_adresse.strip():
                errors.append("Adresse travail obligatoire (ou coche 'Lieu de travail inconnu').")
            if not st.session_state.travail_cp.strip():
                errors.append("Code postal travail obligatoire (ou coche 'Lieu de travail inconnu').")
            if not st.session_state.travail_ville.strip():
                errors.append("Ville travail obligatoire (ou coche 'Lieu de travail inconnu').")
    return errors


def build_payload():
    payload = {
        "nom": st.session_state.nom.strip(),
        "prenom": st.session_state.prenom.strip(),
        "age": int(st.session_state.age),
        "sexe": st.session_state.sexe,
        "date_infection_estimee": str(st.session_state.infection_date),
        "virus_contracte": st.session_state.virus_contracted.strip(),
        "mise_en_quarantaine": (st.session_state.mise_en_quarantaine == "Oui"),
        "quarantaine": None,
        "lieux": None,
    }

    if st.session_state.mise_en_quarantaine == "Oui":
        payload["quarantaine"] = {
            "zone": st.session_state.zone_quarantaine.strip(),
            "date_debut": str(st.session_state.date_debut_quarantaine),
        }
    else:
        payload["lieux"] = {
            "domicile": {
                "inconnu": bool(st.session_state.domicile_inconnu),
                "adresse": None if st.session_state.domicile_inconnu else st.session_state.domicile_adresse.strip(),
                "code_postal": None if st.session_state.domicile_inconnu else st.session_state.domicile_cp.strip(),
                "ville": None if st.session_state.domicile_inconnu else st.session_state.domicile_ville.strip(),
            },
            "travail": {
                "inconnu": bool(st.session_state.travail_inconnu),
                "adresse": None if st.session_state.travail_inconnu else st.session_state.travail_adresse.strip(),
                "code_postal": None if st.session_state.travail_inconnu else st.session_state.travail_cp.strip(),
                "ville": None if st.session_state.travail_inconnu else st.session_state.travail_ville.strip(),
            },
        }
    return payload


# def post_case(payload: dict):
#     r = requests.post(f"{CASE_API}/cases", json=payload, timeout=10)
#     r.raise_for_status()
#     return r.json()


# =====================
# INIT
# =====================
init_state()
st.progress({1: 0.33, 2: 0.66, 3: 1.0}[st.session_state.step])

# =====================
# ETAPE 1
# =====================
if st.session_state.step == 1:
    st.subheader("Étape 1/3 — Infos générales")

    st.text_input("Nom *", key="nom")
    st.text_input("Prénom *", key="prenom")
    st.number_input("Age", min_value=0, key="age")

    st.selectbox("Sexe", ["Masculin", "Féminin", "Autre", "Inconnu"], key="sexe")
    st.date_input("Date d'infection estimée", key="infection_date")
    st.text_input("Virus contracté *", key="virus_contracted")

    st.radio(
        "Mise en quarantaine ?",
        ["Oui", "Non"],
        key="mise_en_quarantaine",
        horizontal=True,
        on_change=on_change_quarantaine
    )

    errors = validate_step1()
    for e in errors:
        st.error(e)

    if st.button("➡️ Suivant", disabled=bool(errors)):
        go(2)

# =====================
# ETAPE 2
# =====================
elif st.session_state.step == 2:
    st.subheader("Étape 2/3 — Détails")
#regle le bug de la quarantaine qui reset quand on remplie la zone de quarantaine
    st.radio(
    "Mise en quarantaine ?",
    ["Oui", "Non"],
    key="mise_en_quarantaine",
    horizontal=True,
    disabled=True
)


    if st.session_state.mise_en_quarantaine == "Oui":
        st.markdown("### 🏥 Zone de quarantaine")
        st.text_input("Zone de mise en quarantaine *", key="zone_quarantaine")
        st.date_input("Début de la quarantaine", key="date_debut_quarantaine")
    else:
        st.markdown("### 🏠 Lieux fréquentés")

        st.markdown("#### Domicile")
        st.checkbox("Domicile inconnu", key="domicile_inconnu")
        if not st.session_state.domicile_inconnu:
            st.text_input("Adresse domicile *", key="domicile_adresse")
            st.text_input("Code postal *", key="domicile_cp")
            st.text_input("Ville *", key="domicile_ville")
        else:
            # reset uniquement si case cochée (et donc widget non affiché)
            st.session_state.domicile_adresse = ""
            st.session_state.domicile_cp = ""
            st.session_state.domicile_ville = ""

        st.markdown("#### Travail")
        st.checkbox("Lieu de travail inconnu", key="travail_inconnu")
        if not st.session_state.travail_inconnu:
            st.text_input("Adresse travail *", key="travail_adresse")
            st.text_input("Code postal *", key="travail_cp")
            st.text_input("Ville *", key="travail_ville")
        else:
            st.session_state.travail_adresse = ""
            st.session_state.travail_cp = ""
            st.session_state.travail_ville = ""

    errors = validate_step2()
    for e in errors:
        st.error(e)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Précédent"):
            go(1)
    with col2:
        if st.button("➡️ Suivant", disabled=bool(errors)):
            go(3)

# =====================
# ETAPE 3
# =====================
else:
    st.subheader("Étape 3/3 — Récap & Enregistrer")

    payload = build_payload()
    st.markdown("### 📦 Payload")
    st.json(payload)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Modifier"):
            go(2)
    with col2:
        if st.button("🚨 Enregistrer"):
            if DRY_RUN:
                st.success("✅ DRY RUN : prêt (pas d'appel API).")
            else:
                try:
                    created = post_case(payload)
                    st.success("✅ Cas enregistré !")
                    st.json(created)
                except Exception as ex:
                    st.error(f"❌ Erreur API : {ex}")
