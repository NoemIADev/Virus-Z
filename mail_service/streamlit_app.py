import streamlit as st
from app.alertedb import add_subscriber, init_db

init_db()

st.title("📩 Abonnement aux alertes Virus-Z")

st.write("Inscrivez-vous pour recevoir les alertes par email.")

nom = st.text_input("Nom")
prenom = st.text_input("Prénom")
email = st.text_input("Adresse email")

if st.button("S’abonner"):
    if nom and prenom and email:
        success = add_subscriber(nom, prenom, email)
        
        if success:
            st.success("✅ Vous êtes bien abonné !")
        else:
            st.warning("⚠️ Cet email est déjà enregistré.")
    else:
        st.error("❌ Merci de remplir tous les champs.")