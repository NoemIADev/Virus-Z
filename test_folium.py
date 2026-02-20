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

# Vérifier que data n'est pas vide et que c'est une liste
if response.status_code != 200 or not isinstance(data, list) or len(data) == 0:
    st.warning("Aucun cas trouvé ou erreur API")
    st.write(data)
    st.stop()

first_location = [data[0]["lat"], data[0]["lon"]]

m = folium.Map(location=first_location, zoom_start=6)

for case in data:
    folium.CircleMarker(
        location=[case["lat"], case["lon"]],
        radius=8,
        popup=case["virus"],
        color=case["color"],
        fill=True,
        fill_color=case["color"],
        fill_opacity=0.7,
    ).add_to(m)

# Légende simple
legend_html = "<div style='position: fixed; bottom: 50px; left: 50px; background:white; padding:10px; border-radius:8px;'>"
legend_html += "<b>🦠 Légende Virus</b><br>"
for case in data:
    legend_html += f"<div style='display:flex; align-items:center;'><span style='width:12px; height:12px; background:{case['color']}; display:inline-block; margin-right:8px;'></span>{case['virus']}</div>"
legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

st_folium(m, width=1200, height=700)
