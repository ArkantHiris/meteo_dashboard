import requests
from database import get_db_connection
from schema import VilleModel
from crud import inserer_ville, inserer_releve, recuperer_toutes_les_villes

def executer_pipeline_meteo():
    """
    Fonction récupérant les données météorologiques des villes sélectionnées
    Puis les enregistre en db
    """
    
    conn = get_db_connection()
    resultats = []

    villes_cibles = recuperer_toutes_les_villes(conn)

    for v_data in villes_cibles:
        try:
            # 1. Validation Pydantic
            ville_obj = VilleModel(**v_data)
            
            # 2. Gestion de la ville en base
            ville_id = inserer_ville(conn, ville_obj)

            # 3. Requête API Open-Meteo
            url = f"https://api.open-meteo.com/v1/forecast?latitude={ville_obj.latitude}&longitude={ville_obj.longitude}&current=temperature_2m,wind_speed_10m"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            current = response.json().get("current", {})
            temp = current.get("temperature_2m")
            vent = current.get("wind_speed_10m")
            date_str = current.get("time").replace("T", " ") + ":00"

            # 4. Enregistrement du relevé
            inserer_releve(conn, ville_id, temp, vent, date_str)
            resultats.append({"ville": ville_obj.nom, "statut": "Succès", "temperature": temp, "vent": vent})

        except Exception as e:
            resultats.append({"ville": v_data["nom"], "statut": "Erreur", "details": str(e)})

    conn.close()
    return resultats