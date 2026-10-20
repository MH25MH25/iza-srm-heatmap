import pandas as pd
import numpy as np

def run_srm_regional_aggregation():
    print("Stap 3: Start aggregatie van open data naar de 38 IZA-regio's...")
    
    # 1. Laad de gemeente-naar-regio crosswalk
    # Zorg dat je bestand in GitHub 'table__86247NED.csv' heet (.csv extensie)
    try:
        df_crosswalk = pd.read_csv('table__86247NED.csv', quotechar='"', header=None, skiprows=2)
        df_crosswalk.columns = ['Gemeente', 'ZK_Code', 'ZK_Naam']
        df_crosswalk = df_crosswalk.dropna(subset=['Gemeente', 'ZK_Code'])
    except Exception as e:
        print(f"Fout bij inlezen crosswalk: {e}")
        return
    
    print(f"-> Gekoppelde gemeenten geladen: {len(df_crosswalk)}")

    # 2. Simuleer / Laad open data per gemeente (bijv. Indicator 1: Systeemdruk / Zorgvraagcomplexiteit)
    # In een latere versie trek je dit rechtstreeks van de CBS StatLine API per gemeente.
    np.random.seed(42) # Voor reproduceerbare testdata
    df_open_data = pd.DataFrame({
        'Gemeente': df_crosswalk['Gemeente'],
        'Systeemdruk_Score': np.random.uniform(20.0, 95.0, size=len(df_crosswalk))
    })

    # 3. Voeg de open data samen met de crosswalk op basis van Gemeentenaam
    df_merged = pd.merge(df_crosswalk, df_open_data, on='Gemeente', how='inner')

    # 4. Aggregeer van gemeenten naar IZA-regio's (groeperen op ZK_Code en ZK_Naam)
    df_iza_regios = df_merged.groupby(['ZK_Code', 'ZK_Naam']).agg(
        Gemiddelde_Systeemdruk=('Systeemdruk_Score', 'mean'),
        Aantal_Gemeenten=('Gemeente', 'count')
    ).reset_index()

    # Sorteer van hoog naar laag risico
    df_iza_regios = df_iza_regios.sort_values(by='Gemiddelde_Systeemdruk', ascending=False)

    print("\nResultaat: Top 5 IZA-regio's met de hoogste berekende stelseldruk:")
    print(df_iza_regios.head(5).to_string(index=False))

    # 5. Sla het resultaat op als een tussentijds CSV-bestand
    output_filename = "srm_iza_regio_scores.csv"
    df_iza_regios.to_csv(output_filename, index=False)
    print(f"\nRegionale scores succesvol opgeslagen als '{output_filename}'!")

if __name__ == "__main__":
    run_srm_regional_aggregation()
