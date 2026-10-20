import pandas as pd
import numpy as np
import plotly.express as px

def generate_robust_heatmap():
    print("Start genereren SRM IZA-regio stelselbeeld...")
    
    # 1. Laad de crosswalk (gemeenten naar IZA-regio's)
    try:
        df_crosswalk = pd.read_csv('table__86247NED.CSV', quotechar='"', header=None, skiprows=2)
        df_crosswalk.columns = ['Gemeente', 'ZK_Code', 'ZK_Naam']
        df_crosswalk = df_crosswalk.dropna(subset=['Gemeente', 'ZK_Code'])
    except Exception as e:
        print(f"Fout bij inlezen crosswalk: {e}")
        return

    # 2. Genereer realistische testdata per gemeente voor indicator 'Systeemdruk'
    np.random.seed(42)
    df_crosswalk['Systeemdruk_Score'] = np.random.uniform(25.0, 90.0, size=len(df_crosswalk))
    
    # Aggregeer naar IZA-regio niveau voor een helder overzicht per zorgkantoorregio
    df_iza = df_crosswalk.groupby(['ZK_Code', 'ZK_Naam']).agg(
        Systeemdruk_Score=('Systeemdruk_Score', 'mean'),
        Aantal_Gemeenten=('Gemeente', 'count')
    ).reset_index()

    print(f"Aggregatie voltooid voor {len(df_iza)} IZA-regio's.")

    # 3. Maak een helder, interactief choropleth-achtig staafdiagram / regio-heatmap met Plotly
    # Dit garandeert 100% stabiele werking in elke GitHub Actions omgeving zonder netwerkfouten.
    fig = px.bar(
        df_iza.sort_values(by='Systeemdruk_Score', ascending=True),
        x='Systeemdruk_Score',
        y='ZK_Naam',
        orientation='h',
        title='SRM Stelselbeeld - Systeemdruk & Risico per IZA-regio',
        labels={'Systeemdruk_Score': 'Gemiddelde Risicoscore (0-100)', 'ZK_Naam': 'IZA-regio'},
        color='Systeemdruk_Score',
        color_continuous_scale='Reds',
        text_auto='.1f'
    )
    
    fig.update_layout(
        template='plotly_white',
        xaxis_title="Risico-index",
        yaxis_title="Regio",
        height=900,
        margin={"r":20,"t":50,"l":150,"b":50}
    )

    # 4. Sla altijd op als HTML-bestand
    output_file = "srm_heatmap_dashboard.html"
    fig.write_html(output_file)
    print(f"Dashboard succesvol gegenereerd en opgeslagen als '{output_file}'!")

if __name__ == "__main__":
    generate_robust_heatmap()
