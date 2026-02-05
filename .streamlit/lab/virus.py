import streamlit as st
import requests

st.title("Ajouter une infection")

with st.form("add_infection"):
    nom = st.text_input("Nom du virus")
    variante = st.text_input("Variante")
    
    mode_propagation = st.selectbox(
        "Mode de propagation",
        ["Morsure", "Sang", "mutation genetique", "Inconnu"]
    )

    incubation_min = st.number_input(
        "Incubation minimale (heures)", min_value=0, value=1
    )
    incubation_max = st.number_input(
        "Incubation maximale (heures)", min_value=0, value=7
    )

    contagiosite = st.radio(
    "Contagiosité",
    options=[0, 1],
    format_func=lambda x: "Faible / non contagieux" if x == 0 else "Fortement contagieux"
    )

    moyens_detection = st.multiselect(
        "Moyens de détection",
        ["Symptômes", "Test salivaire", "Scan", "Observation comportementale"]
    )

    commentaire = st.text_area("Commentaire")

    submitted = st.form_submit_button("Enregistrer")

if submitted:
    errors = []

    if not nom:
        errors.append("Le nom du virus est obligatoire")

    if not mode_propagation:
        errors.append("Le mode de propagation est obligatoire")

    if incubation_min > incubation_max:
        errors.append("L'incubation minimale doit être ≤ incubation maximale")

    if not moyens_detection:
        errors.append("Au moins un moyen de détection est obligatoire")

    if errors:
        for e in errors:
            st.error(e)
    else:
        payload = {
            "nom": nom,
            "variante": variante or None,
            "mode_propagation": mode_propagation,
            "incubation_min": incubation_min,
            "incubation_max": incubation_max,
            "contagiosite": contagiosite,
            "moyens_detection": moyens_detection,
            "commentaire": commentaire or None
        }

        # appel API ici
        st.success("Infection enregistrée avec succès 🧟‍♂️")
