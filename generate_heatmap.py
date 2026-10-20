import pandas as pd
import numpy as np
import plotly.express as px
import urllib.request
import json

def generate_geographic_heatmap():
    print("Genereren van geografische IZA-heatmap van Nederland...")
    
    # 1. Laad de gemeente-naar-regio crosswalk
    try:
        df_crosswalk = pd.read_csv('table__86247NED.CSV', quotechar='"', header=None, skiprows=2)
        df_crosswalk.columns = ['Gemeente', 'ZK_Code', 'ZK_Naam']
        df_crosswalk = df_crosswalk.dropna(subset=['Gemeente', 'ZK_Code'])
    except Exception as e:
        print(f"Fout bij inlezen crosswalk: {e}")
        return

    # 2. Genereer realistische testdata per gemeente (of direct per IZA-regio)
    np.random.seed(42)
    df_crosswalk['Systeemdruk_Score'] = np.random.uniform(25.0, 90.0, size=len(df_crosswalk))
    
    # Aggregeer naar IZA-regio niveau voor de tabel/statistieken
    df_iza = df_crosswalk.groupby(['ZK_Code', 'ZK_Naam']).agg(
        Systeemdruk_Score=('Systeemdruk_Score', 'mean'),
        Aantal_Gemeenten=('Gemeente', 'count')
    ).reset_index()

    # 3. Download openbaar GeoJSON-bestand van Nederlandse gemeenten
    geojson_url = "https://raw.githubusercontent.com/opengeodata/agiv-vlaanderen-en-nederland/master/nederland_gemeenten.geojson"
    print("Downloaden van geografische kaartdata (GeoJSON)...")
    
    with urllib.request.urlopen(geojson_url) as url:
        geojson_data = json.loads(url.read().decode())

    # 4. Bouw een interactieve Choropleth kaart van Nederland op gemeenteniveau (gekleurd op IZA-regio / score)
    # We mappen de gemeenten uit de GeoJSON aan onze crosswalk data
    fig = px.choropleth(
        df_crosswalk,
        geojson=geojson_data,
        locations='Gemeente',
        featureidkey="properties.gemeentenaam", # Afhankelijk van de eigenschap in de GeoJSON, of we gebruiken een alternative mapping
        color='Systeemdruk_Score',
        color_continuous_scale="Reds",
        range_color=(25, 90),
        scope="europe",
        center={"lat": 52.1326, "lon": 5.2913},
        title="SRM Geografisch Stelselbeeld - Systeemdruk per Regio"
    )

    # Optimaliseer de kaartweergave voor Nederland
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        template='plotly_white',
        height=800
    )

    # 5. Sla op als HTML-bestand
    output_file = "srm_heatmap_dashboard.html"
    fig.write_html(output_file)
    print(f"Geografische kaart succesvol opgeslagen als '{output_file}'!")

if __name__ == "__main__":
    generate_geographic_heatmap()
