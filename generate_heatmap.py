import pandas as pd
import numpy as np
import plotly.express as px
import urllib.request
import json

def generate_geographic_map():
    print("Start genereren geografische IZA-heatmap van Nederland...")
    
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
    
    # Koppel de regioscore aan elke gemeente via de crosswalk
    df_crosswalk['Risico_Score'] = df_crosswalk['ZK_Naam'].map(region_scores)

    # 3. Haal de betrouwbare GeoJSON van Nederland op (met 'name' als eigenschap voor gemeenten)
    geojson_url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/the-netherlands.geojson"
    
    print("Downloaden geografische kaartdata...")
    try:
        with urllib.request.urlopen(geojson_url, timeout=15) as response:
            geojson_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Fout bij ophalen GeoJSON: {e}")
        return

    # 4. Maak de interactieve landkaart met Plotly Choropleth
    fig = px.choropleth(
        df_crosswalk,
        geojson=geojson_data,
        locations='Gemeente',
        featureidkey="properties.name", # Gecorrigeerd naar de juiste property key in dit bestand
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
    generate_geographic_map()
