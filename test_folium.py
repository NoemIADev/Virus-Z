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

if not data:
    st.warning("Aucun cas trouvé.")
    st.stop()

first_location = [data[0]["lat"], data[0]["lon"]]

m = folium.Map(location=first_location, zoom_start=6)

virus_set = set()

for case in data:
    virus = case["virus"]
    virus_set.add(virus)

    folium.CircleMarker(
        location=[case["lat"], case["lon"]],
        radius=8,
        popup=virus,
        color=case["color"],
        fill=True,
        fill_color=case["color"],
        fill_opacity=0.7,
    ).add_to(m)

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

for case in data:
    legend_html += f"""
    <div>
        <span style="
            display:inline-block;
            width:12px;
            height:12px;
            background:{case['color']};
            margin-right:8px;
        "></span>
        {case['virus']}
    </div>
    """

legend_html += "</div>"

m.get_root().html.add_child(folium.Element(legend_html))

st_folium(m, width=1200, height=700)