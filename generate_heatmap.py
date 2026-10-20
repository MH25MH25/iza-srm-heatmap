import pandas as pd
import numpy as np
import plotly.express as px
import json
import requests

def generate_srm_heatmap():
    print("Stap 4: Genereren van de IZA-regio heatmap...")
    
    # 1. Laad de berekende regionale scores (of bereken ze direct uit de crosswalk)
    try:
        df_crosswalk = pd.read_csv('table__86247NED.CSV', quotechar='"', header=None, skiprows=2)
        df_crosswalk.columns = ['Gemeente', 'ZK_Code', 'ZK_Naam']
        df_crosswalk = df_crosswalk.dropna(subset=['Gemeente', 'ZK_Code'])
    except Exception as e:
        print(f"Fout bij inlezen crosswalk: {e}")
        return

    # Genereer testdata voor de 38 IZA-regio's
    np.random.seed(42)
    df_open_data = pd.DataFrame({
        'Gemeente': df_crosswalk['Gemeente'],
        'Systeemdruk_Score': np.random.uniform(25.0, 90.0, size=len(df_crosswalk))
    })

    df_merged = pd.merge(df_crosswalk, df_open_data, on='Gemeente', how='inner')
    df_iza = df_merged.groupby(['ZK_Code', 'ZK_Naam']).agg(
        Systeemdruk_Score=('Systeemdruk_Score', 'mean'),
        Aantal_Gemeenten=('Gemeente', 'count')
    ).reset_index()

    # 2. Haal een openbaar GeoJSON-bestand op voor de Nederlandse gemeenten/regio's
    # (We gebruiken hier een openbare CBS/gemeente grenzen bron voor de visualisatie)
    geojson_url = "https://raw.githubusercontent.com/opengeodata/agiv-vlaanderen-en-nederland/master/nederland_gemeenten.geojson"
    
    print("Bezig met aanmaken van de Plotly choropleth kaart...")
    
    # Voor nu bouwen we een duidelijke staafdiagram/heatmap weergave of kaartstructuur
    fig = px.bar(
        df_iza.sort_values(by='Systeemdruk_Score', ascending=True),
        x='Systeemdruk_Score',
        y='ZK_Naam',
        orientation='h',
        title='SRM Stelselbeeld - Systeemdruk per IZA-regio',
        labels={'Systeemdruk_Score': 'Gemiddelde Systeemdruk Index (0-100)', 'ZK_Naam': 'IZA-regio'},
        color='Systeemdruk_Score',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        template='plotly_white',
        xaxis_title="Risicoscore",
        yaxis_title="Regio",
        height=900
    )

    # 3. Sla op als interactief HTML-bestand
    output_file = "srm_heatmap_dashboard.html"
    fig.write_html(output_file)
    print(f"Dashboard succesvol opgeslagen als '{output_file}'!")

if __name__ == "__main__":
    generate_srm_heatmap()
