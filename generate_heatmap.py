import pandas as pd
import numpy as np
import plotly.express as px
import json
import os

def generate_local_geojson_map():
    print("Start genereren IZA-heatmap op basis van lokaal GeoJSON-bestand...")
    
    # 1. Laad de crosswalk (gemeenten naar IZA-regio's)
    try:
        df_crosswalk = pd.read_csv('table__86247NED.CSV', quotechar='"', header=None, skiprows=2)
        df_crosswalk.columns = ['Gemeente', 'ZK_Code', 'ZK_Naam']
        df_crosswalk = df_crosswalk.dropna(subset=['Gemeente', 'ZK_Code'])
    except Exception as e:
        print(f"Fout bij inlezen crosswalk: {e}")
        return

    # 2. Genereer realistische testdata per IZA-regio / gemeente
    np.random.seed(42)
    unique_regions = df_crosswalk['ZK_Naam'].unique()
    region_scores = {regio: np.random.uniform(25.0, 90.0) for regio in unique_regions}
    df_crosswalk['Risico_Score'] = df_crosswalk['ZK_Naam'].map(region_scores)

    # 3. Laad het lokale GeoJSON-bestand dat zojuist is geüpload
    geojson_filename = "the-netherlands.geojson"
    if not os.path.exists(geojson_filename):
        print(f"Fout: Kan '{geojson_filename}' niet vinden in de repository!")
        return
        
    print(f"Inlezen lokaal bestand '{geojson_filename}'...")
    with open(geojson_filename, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # 4. Maak de interactieve landkaart met Plotly Choropleth
    fig = px.choropleth(
        df_crosswalk,
        geojson=geojson_data,
        locations='Gemeente',
        featureidkey="properties.name", # Komt exact overeen met 'properties.name' in je GeoJSON
        color='Risico_Score',
        color_continuous_scale="Reds",
        range_color=(25, 90),
        scope="europe",
        center={"lat": 52.1326, "lon": 5.2913},
        hover_name='Gemeente',
        hover_data=['ZK_Naam', 'Risico_Score'],
        title="SRM Geografisch Stelselbeeld - Systeemdruk & Risico per IZA-regio"
    )

    # Optimaliseer de kaartweergave voor Nederland
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        template='plotly_white',
        height=800
    )

    # 5. Sla op als HTML-bestand
    output_file = "srm_heatmap_dashboard.html"
    fig.write_html(output_file)
    print(f"Geografische landkaart succesvol opgeslagen als '{output_file}'!")

if __name__ == "__main__":
    generate_local_geojson_map()
