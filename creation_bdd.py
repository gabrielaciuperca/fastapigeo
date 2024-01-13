import csv
import requests
import time
import sqlite3
from database import get_db_connection

DATABASE_PATH = 'communes.db'
CSV_PATH = 'communes-departement-region.csv'

# Définition de la fonction de géocodage, de l'extraction des données, etc.
# ... (comme dans ton code actuel)

# Fonction de géocodage
def geocode_commune(nom_commune):
    # Remplacer l'URL par l'URL de ton instance Pelias
    pelias_url = "http://pelias:4000/v1/search"
    params = {'text': nom_commune}
    try:
        response = requests.get(pelias_url, params=params)
        if response.status_code == 200 and response.json():
            data = response.json()['features'][0]['geometry']['coordinates']
            # Pelias renvoie les coordonnées sous la forme [longitude, latitude]
            return data[1], data[0]  # Inverser pour obtenir latitude, longitude
    except requests.RequestException as e:
        print(f"Erreur de géocodage pour {nom_commune}: {e}")
    return None, None


# Extraction des données
def extract_data_from_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

# Transformation des données
def transform_data(communes_data):
    transformed_data = []
    for commune_info in communes_data:
        # Limitation du taux de requêtes pour Nominatim
        latitude, longitude = geocode_commune(commune_info['nom_commune_complet'])
        print(commune_info['nom_commune_complet'], latitude, longitude)  # Pour le débogage
        transformed_data.append({
            'code_postal': commune_info['code_postal'],
            'nom_commune': commune_info['nom_commune_complet'].upper(),
            'departement': commune_info['code_postal'][:2],
            'latitude': latitude,
            'longitude': longitude,
        })
    return transformed_data

# Chargement des données
def load_data_to_db(transformed_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS communes (
            code_postal TEXT,
            nom_commune_complet TEXT,
            departement TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    for commune in transformed_data:
        cursor.execute('''
            INSERT INTO communes (code_postal, nom_commune_complet, departement, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        ''', (commune['code_postal'], commune['nom_commune'], commune['departement'], commune['latitude'], commune['longitude']))
    conn.commit()
    conn.close()

def run_etl_process():
    data = extract_data_from_csv(CSV_PATH)
    transformed_data = transform_data(data)
    load_data_to_db(transformed_data)

if __name__ == "__main__":
    run_etl_process()
