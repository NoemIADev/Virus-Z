import streamlit as st
import requests

st.title("Ajouter une infection")

with st.form("add_infected"):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prenom")
    age = st.number_input("Age", min_value=0, value=30)
    sexe = st.selectbox(
        "Sexe",
        ["Masculin", "Féminin", "Autre", "Inconnu"]
    )
    infection_date = st.date_input("Date d'infection estimée")
    virus_contracted = st.text_input("Virus contracté")
    mise_en_quarantaine = st.checkbox("Mise en quarantaine")

    if mise_en_quarantaine:
        st.markdown("### 🏥 Zone de quarantaine")
        zone_quarantaine = st.text_input("Zone de mise en quarantaine *")
        date_debut_quarantaine = st.date_input("Début de la quarantaine")

        # valeurs par défaut pour l'autre branche
        domicile_inconnu = travail_inconnu = None
        domicile_adresse = domicile_cp = domicile_ville = None
        travail_adresse = travail_cp = travail_ville = None

    else:
        st.markdown("### 🏠 Lieux fréquentés")

        # ----- DOMICILE -----
        st.markdown("#### Domicile")
        domicile_inconnu = st.checkbox("Domicile inconnu", key="dom_inconnu")

        if not domicile_inconnu:
            domicile_adresse = st.text_input("Adresse domicile *", key="dom_adr")
            domicile_cp = st.text_input("Code postal *", key="dom_cp")
            domicile_ville = st.text_input("Ville *", key="dom_ville")
        else:
            domicile_adresse = domicile_cp = domicile_ville = None

        # ----- TRAVAIL -----
        st.markdown("#### Travail")
        travail_inconnu = st.checkbox("Lieu de travail inconnu", key="trav_inconnu")

        if not travail_inconnu:
            travail_adresse = st.text_input("Adresse travail *", key="trav_adr")
            travail_cp = st.text_input("Code postal *", key="trav_cp")
            travail_ville = st.text_input("Ville *", key="trav_ville")
        else:
            travail_adresse = travail_cp = travail_ville = None

        # valeurs par défaut pour l'autre branche
        zone_quarantaine = None
        date_debut_quarantaine = None

        
    submitted = st.form_submit_button("Enregistrer")
        