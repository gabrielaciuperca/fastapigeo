from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db_connection

# Définition de la configuration et des constantes

app = FastAPI()


# Modèles Pydantic pour la validation des données
class Commune(BaseModel):
    code_postal: str
    nom_commune: str
    departement: str
    latitude: float = None
    longitude: float = None

# FastAPI Endpoints
@app.get("/communes/{nom_commune}")
async def lire_commune(nom_commune: str):
    conn = get_db_connection()
    commune = conn.execute('SELECT * FROM communes WHERE nom_commune_complet = ?', (nom_commune,)).fetchone()
    conn.close()
    if commune is None:
        return {"erreur": "Commune non trouvée"}
    return dict(commune)

@app.post("/communes")
async def ajouter_commune(commune: Commune):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO communes (code_postal, nom_commune_complet, departement, latitude, longitude) 
        VALUES (?, ?, ?, ?, ?)
    ''', (commune.code_postal, commune.nom_commune, commune.departement, commune.latitude, commune.longitude))
    conn.commit()
    conn.close()
    return {"message": "Commune ajoutée avec succès"}

@app.get("/departements/{departement}/communes")
async def lister_communes_departement(departement: str):
    conn = get_db_connection()
    departement_int = int(departement) if departement.isdigit() else departement
    communes = conn.execute('SELECT * FROM communes WHERE departement = ?', (departement_int,)).fetchall()
    conn.close()
    if not communes:
        raise HTTPException(status_code=404, detail="Aucune commune trouvée pour ce département")
    return [dict(commune) for commune in communes]


@app.get("/communes/{nom_commune}/coordinates")
async def get_commune_coordinates(nom_commune: str):
    conn = get_db_connection()
    commune = conn.execute(
        'SELECT nom_commune_complet, latitude, longitude FROM communes WHERE nom_commune_complet = ?', 
        (nom_commune,)
    ).fetchone()
    conn.close()
    if commune is None:
        return {"erreur": "Commune non trouvée"}
    return dict(commune)


