import streamlit as st
from datetime import date
import requests

st.title("🧟 Ajouter un cas (Virus Z)")

# =====================
# CONFIG (à adapter)
# =====================
DRY_RUN = False # True = pas d'appel API, juste construction du payload et affichage
CAS_API = "http://localhost:8000"  # decomente/commente si besoin

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
        "variant": "",
        "mise_en_quarantaine": "Non",  # "Oui" ou "Non"

        # Etape 2 - quarantaine
        "zone_quarantaine": None,
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
    for k, v in defaults.items(): #key and value
        if k not in st.session_state:
            st.session_state.setdefault(k, v)

    # Normalise les anciennes valeurs possibles (bool/string) vers "Oui"/"Non"
    st.session_state.mise_en_quarantaine = "Oui" if is_quarantaine_enabled() else "Non"


def is_quarantaine_enabled() -> bool:
    """Retourne True si la quarantaine est activée, quel que soit le format stocké."""
    value = st.session_state.get("mise_en_quarantaine", "Non")
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"oui", "true", "1"}
    return False


def go(step: int):
    st.session_state.step = step
    st.rerun()


def on_change_quarantaine():
    """Quand on change Oui/Non, on reset l'autre branche pour éviter incohérences."""
    if is_quarantaine_enabled():
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
        st.session_state.zone_quarantaine = None
        st.session_state.date_debut_quarantaine = date.today()


def persist_step2_snapshot():
    """Snapshot non-widget de l'étape 2 pour survivre aux reruns de Streamlit."""
    st.session_state["step2_snapshot"] = {
        "zone_quarantaine": st.session_state.get("zone_quarantaine", ""),
        "date_debut_quarantaine": st.session_state.get("date_debut_quarantaine", date.today()),
        "domicile_inconnu": bool(st.session_state.get("domicile_inconnu", False)),
        "domicile_adresse": st.session_state.get("domicile_adresse", ""),
        "domicile_cp": st.session_state.get("domicile_cp", ""),
        "domicile_ville": st.session_state.get("domicile_ville", ""),
        "travail_inconnu": bool(st.session_state.get("travail_inconnu", False)),
        "travail_adresse": st.session_state.get("travail_adresse", ""),
        "travail_cp": st.session_state.get("travail_cp", ""),
        "travail_ville": st.session_state.get("travail_ville", ""),
    }


def validate_step1():
    errors = []
    if not st.session_state.virus_contracted.strip():
        errors.append("Le champ 'Virus contracté' est obligatoire.")
    if st.session_state.nom.strip() == "" or st.session_state.prenom.strip() == "":
        errors.append("Le nom et le prénom sont obligatoires.")
    return errors


def validate_step2():
    errors = []
    if is_quarantaine_enabled():
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
    quarantaine_active = is_quarantaine_enabled()
    step2 = st.session_state.get("step2_snapshot", {})

    def get_step2_value(key: str, default):
        return step2.get(key, st.session_state.get(key, default))

    def clean_text(value):
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    domicile_inconnu = bool(get_step2_value("domicile_inconnu", False))
    travail_inconnu = bool(get_step2_value("travail_inconnu", False))

    payload = {
        "nom": st.session_state.nom.strip(),
        "prenom": st.session_state.prenom.strip(),
        "age": int(st.session_state.age),
        "sexe": st.session_state.sexe,
        "date_infection_estimee": str(st.session_state.infection_date),
        "virus_contracte": st.session_state.virus_contracted.strip(),
        "variant": st.session_state.variant.strip() or None,
        "mise_en_quarantaine": quarantaine_active,
        "quarantaine": None,
        "lieux": None,
    }

    if quarantaine_active:
        payload["quarantaine"] = {
            "zone": clean_text(get_step2_value("zone_quarantaine", "")),
            "date_debut": str(get_step2_value("date_debut_quarantaine", date.today())),
        }
    else:
        payload["lieux"] = {
            "domicile": {
                "inconnu": domicile_inconnu,
                "adresse": None if domicile_inconnu else clean_text(get_step2_value("domicile_adresse", "")),
                "code_postal": None if domicile_inconnu else clean_text(get_step2_value("domicile_cp", "")),
                "ville": None if domicile_inconnu else clean_text(get_step2_value("domicile_ville", "")),
            },
            "travail": {
                "inconnu": travail_inconnu,
                "adresse": None if travail_inconnu else clean_text(get_step2_value("travail_adresse", "")),
                "code_postal": None if travail_inconnu else clean_text(get_step2_value("travail_cp", "")),
                "ville": None if travail_inconnu else clean_text(get_step2_value("travail_ville", "")),
            },
        }
    return payload


def post_cases(payload: dict):
    r = requests.post(f"{CAS_API}/cases", json=payload, timeout=10)
    if not r.ok:
        try:
            error_detail = r.json()
        except ValueError:
            error_detail = r.text
        raise RuntimeError(f"Erreur API ({r.status_code}) : {error_detail}")
    return r.json()


def get_quarantine_zones():
    """Récupère les zones de quarantaine depuis l'API."""
    try:
        r = requests.get(f"{CAS_API}/catalog/zones-quarantaine", timeout=10)
        r.raise_for_status()
        return r.json().get("zones", [])
    except Exception:
        return []


def get_virus_catalog():
    """Récupère les couples virus/variant depuis l'API."""
    try:
        r = requests.get(f"{CAS_API}/catalog/virus", timeout=10)
        r.raise_for_status()
        return r.json().get("virus", [])
    except Exception:
        return []


# =====================
# INIT
# =====================
init_state()

# Listes dynamiques depuis la base via API
zones_quarantaine = get_quarantine_zones()
virus_catalog = get_virus_catalog()
virus_labels = [item["label"] for item in virus_catalog]

st.progress({1: 0.33, 2: 0.66, 3: 1.0}[st.session_state.step])

# =====================
# ETAPE 1
# =====================
if st.session_state.step == 1:
    st.subheader("Étape 1/3 — Infos générales")

    with st.form("step1_form", clear_on_submit=False):
        nom = st.text_input("Nom *", value=st.session_state.nom)
        prenom = st.text_input("Prénom *", value=st.session_state.prenom)
        age = st.number_input("Age", min_value=0, value=int(st.session_state.age))

        sexe = st.selectbox("Sexe", ["Masculin", "Féminin", "Autre", "Inconnu"],
                            index=["Masculin", "Féminin", "Autre", "Inconnu"].index(st.session_state.sexe))
        infection_date = st.date_input("Date d'infection estimée", value=st.session_state.infection_date)

        selected_label = None
        if st.session_state.virus_contracted:
            for item in virus_catalog:
                if item["nom"] == st.session_state.virus_contracted and (item["variante"] or "") == st.session_state.variant:
                    selected_label = item["label"]
                    break

        if virus_labels:
            index_virus = virus_labels.index(selected_label) if selected_label in virus_labels else 0
            virus_choice = st.selectbox("Virus *", virus_labels, index=index_virus)
        else:
            st.warning("Aucun virus disponible pour le moment dans la base.")
            virus_choice = ""

        mise_en_quarantaine = st.radio(
            "Mise en quarantaine ?",
            ["Oui", "Non"],
            index=0 if st.session_state.mise_en_quarantaine == "Oui" else 1,
            horizontal=True
        )

        submit = st.form_submit_button("➡️ Suivant")

    # commit au submit
    if submit:
        st.session_state.nom = nom
        st.session_state.prenom = prenom
        st.session_state.age = age
        st.session_state.sexe = sexe
        st.session_state.infection_date = infection_date
        if virus_choice:
            for item in virus_catalog:
                if item["label"] == virus_choice:
                    st.session_state.virus_contracted = item["nom"]
                    st.session_state.variant = item["variante"] or ""
                    break
        else:
            st.session_state.virus_contracted = ""
            st.session_state.variant = ""

        # si changement quarantaine -> reset branche opposée
        if st.session_state.mise_en_quarantaine != mise_en_quarantaine:
            st.session_state.mise_en_quarantaine = mise_en_quarantaine
            on_change_quarantaine()
        else:
            st.session_state.mise_en_quarantaine = mise_en_quarantaine

        errors = validate_step1()
        if errors:
            for e in errors:
                st.error(e)
        else:
            go(2)

# =====================
# ETAPE 2
# =====================
elif st.session_state.step == 2:
    st.subheader("Étape 2/3 — Détails")

    quarantaine_display = "Oui" if is_quarantaine_enabled() else "Non"
    st.radio(
        "Mise en quarantaine ?",
        ["Oui", "Non"],
        index=0 if quarantaine_display == "Oui" else 1,
        key="mise_en_quarantaine_display",
        horizontal=True,
        disabled=True,
    )

    if is_quarantaine_enabled():
        st.markdown("### 🏥 Zone de quarantaine")
        if zones_quarantaine:
            index_zone = zones_quarantaine.index(st.session_state.zone_quarantaine) if st.session_state.zone_quarantaine in zones_quarantaine else 0
            selected_zone = st.selectbox("Zone de mise en quarantaine *", zones_quarantaine, index=index_zone)
            st.session_state.zone_quarantaine = selected_zone
        else:
            st.warning("Aucune zone de quarantaine disponible en base.")
            st.session_state.zone_quarantaine = ""
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
            # On fige l'état étape 2 ici pour que l'étape 3 survive aux reruns.
            persist_step2_snapshot()
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
                    created = post_cases(payload)
                    st.success("✅ Cas enregistré !")
                    st.json(created)
                except Exception as ex:
                    st.error(f"❌ Erreur API : {ex}")
