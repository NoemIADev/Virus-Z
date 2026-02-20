import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="Virus Z Map", layout="wide")
st.title("Carte des cas - Virus Z")

API_URL = "http://localhost:8000/cases/map"

# =======================
# Récupérer les données
# =======================
if "cases_data" not in st.session_state:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        st.session_state.cases_data = response.json()
    except Exception as e:
        st.error(f"Erreur API : {e}")
        st.stop()

data = st.session_state.cases_data

if not isinstance(data, list) or len(data) == 0:
    st.warning("Aucun cas trouvé ou erreur API")
    st.write(data)
    st.stop()

# =======================
# Créer la carte seulement si elle n'existe pas encore
# =======================
if "folium_map" not in st.session_state:
    # Centre initial sur le premier cas
    first_location = [data[0]["lat"], data[0]["lon"]]
    m = folium.Map(location=first_location, zoom_start=6)

    # Générer une couleur unique par virus
    virus_colors = {}
    for case in data:
        virus_colors.setdefault(case["virus"], "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)]))

    # Ajouter les cas sur la carte
    for idx, case in enumerate(data, start=1):
        folium.CircleMarker(
            location=[case["lat"], case["lon"]],
            radius=6,
            popup=f"ID: {idx} | Virus: {case['virus']}",
            color=virus_colors[case["virus"]],
            fill=True,
            fill_color=virus_colors[case["virus"]],
            fill_opacity=0.7,
        ).add_to(m)

    # Légende
    legend_html = """
    <div style="
        position: fixed; 
        bottom: 50px; left: 50px; 
        background:white; 
        padding:10px; 
        border-radius:8px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
        z-index:9999;
        font-size:14px;">
        <b>🦠 Légende Virus</b><br>
    """
    for virus, color in virus_colors.items():
        legend_html += f"""
        <div style='display:flex; align-items:center; margin-top:3px;'>
            <span style='width:12px; height:12px; background:{color}; display:inline-block; margin-right:6px;'></span>{virus}
        </div>
        """
    legend_html += "</div>"

    m.get_root().html.add_child(folium.Element(legend_html))

    # Stocker l'objet Folium Map dans session_state
    st.session_state.folium_map = m

# =======================
# Affichage final
# =======================
st_folium(st.session_state.folium_map, width=1200, height=700)

st.markdown("---")

# =======================
# Bouton pour afficher la liste complète des cas
# =======================
if st.button("Afficher la liste des cas"):
    try:
        resp_full = requests.get("http://localhost:8000/cases/full")
        resp_full.raise_for_status()
        full_data = resp_full.json()
    except Exception as e:
        st.error(f"Erreur API : {e}")
        st.stop()

    if not isinstance(full_data, list) or len(full_data) == 0:
        st.warning("Aucun cas trouvé")
    else:
        st.success(f"{len(full_data)} cas trouvés")
        # Affichage sous forme de tableau
        st.dataframe(full_data)