import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Virus Z Map", layout="wide")
st.title("Carte des cas - Virus Z")

API_URL = "http://localhost:8000/cases/map"

try:
    response = requests.get(API_URL)
    data = response.json()
except Exception as e:
    st.error(f"Erreur API : {e}")
    st.stop()

# Vérifier que data n'est pas vide
if response.status_code != 200 or not isinstance(data, list) or len(data) == 0:
    st.warning("Aucun cas trouvé ou erreur API")
    st.write(data)
    st.stop()

# ======================
# Couleur fixe par virus
# ======================
virus_colors = {}
color_palette = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", 
    "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe"
]

for i, case in enumerate(data):
    virus = case["virus"]
    if virus not in virus_colors:
        virus_colors[virus] = color_palette[len(virus_colors) % len(color_palette)]

# ======================
# Création carte
# ======================
first_location = [data[0]["lat"], data[0]["lon"]]
m = folium.Map(location=first_location, zoom_start=6)

for case in data:
    folium.CircleMarker(
        location=[case["lat"], case["lon"]],
        radius=8,
        popup=case["virus"],
        color=virus_colors[case["virus"]],
        fill=True,
        fill_color=virus_colors[case["virus"]],
        fill_opacity=0.7,
    ).add_to(m)

# ======================
# Légende
# ======================
legend_html = """
<div style="
position: fixed;
bottom: 50px;
left: 50px;
width: 200px;
background-color: white;
z-index:9999;
font-size:14px;
padding:10px;
border-radius:8px;
box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">
<b>🦠 Légende Virus</b><br>
"""
for virus, color in virus_colors.items():
    legend_html += f"""
    <div>
        <span style="
            display:inline-block;
            width:12px;
            height:12px;
            background:{color};
            margin-right:8px;
        "></span>
        {virus}
    </div>
    """
legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

# ======================
# Affichage dans Streamlit
# ======================
st_folium(m, width=1200, height=700)
