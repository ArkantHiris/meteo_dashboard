from fastapi import FastAPI, status, HTTPException
from typing import List

from database import init_db, get_db_connection
from schema import VilleRead, VilleCreate, ReleveRead
from services import executer_pipeline_meteo

from crud import inserer_ville, recuperer_tous_les_releves

app = FastAPI(
    title="Service Météo API",
    description="Architecture professionnelle séparant Schémas, Services, CRUD et Routes.",
    version="3.0.0"
)

@app.on_event("startup")
def startup_event():
    init_db()  # Crée les tables au démarrage de l'API

@app.post("/pipeline/run", status_code=status.HTTP_200_OK, summary="Lancer la collecte ETL Open-Meteo")
def run_pipeline():
    resultats = executer_pipeline_meteo()
    return {"message": "Pipeline exécuté avec succès", "details": resultats}

@app.get("/villes", response_model=List[VilleRead], summary="Lister les villes enregistrées")
def get_villes():
    conn = get_db_connection()
    villes = conn.execute("SELECT * FROM villes;").fetchall()
    conn.close()
    return [dict(v) for v in villes]


@app.get("/releves", response_model=List[ReleveRead], summary="Récupérer l'historique de tous les relevés météo")
def obtenir_releves():
    conn = get_db_connection()
    releves = recuperer_tous_les_releves(conn)
    conn.close()
    
    return [dict(r) for r in releves]


@app.post("/villes", response_model=VilleRead, status_code=status.HTTP_201_CREATED, summary="Ajouter une nouvelle ville")
def ajouter_ville(ville: VilleCreate): 

    conn = get_db_connection()

    try:
        # L'insertion en base ne se soucie pas de l'id, SQLite le génère
        ville_id = inserer_ville(conn, ville)
        
        # On retourne l'objet complet avec son nouvel ID
        return {
            "id": ville_id,
            "nom": ville.nom,
            "latitude": ville.latitude,
            "longitude": ville.longitude
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        conn.close()
