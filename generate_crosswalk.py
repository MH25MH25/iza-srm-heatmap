import pandas as pd

def load_and_verify_crosswalk():
    print("Stap 2: Inlezen en verifiëren van de gemeente-regio crosswalk...")
    
    # Lees het CSV-bestand in (let op de komma/puntkomma scheiding en headers)
    df_crosswalk = pd.read_csv('table__86247NED.csv', quotechar='"', header=None, skiprows=2)
    df_crosswalk.columns = ['Gemeente', 'ZK_Code', 'ZK_Naam']
    
    # Verwijder eventuele lege rijen
    df_crosswalk = df_crosswalk.dropna(subset=['Gemeente', 'ZK_Code'])
    
    print(f"Totaal aantal gekoppelde gemeenten ingeladen: {len(df_crosswalk)}")
    print(f"Aantal unieke IZA/Zorgkantoorregio's in de dataset: {df_crosswalk['ZK_Code'].nunique()}")
    
    # Toon de eerste 5 rijen ter controle
    print("\nVoorbeeld van de koppeling:")
    print(df_crosswalk.head())
    
    return df_crosswalk

if __name__ == "__main__":
    crosswalk_df = load_and_verify_crosswalk()
