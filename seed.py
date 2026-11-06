# seed.py
from datetime import datetime, timedelta
import sqlite3

DB_NAME = "meteo.db"

def peupler_base():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    print("🌱 Début du peuplement de la base de données...")

    # 1. Insertion des villes de test
    villes = [
        ("Saint-Quentin", 49.8472, 3.2873),
        ("Toulouse", 43.6047, 1.4442),
        ("Paris", 48.8566, 2.3522)
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO villes (nom, latitude, longitude) 
    VALUES (?, ?, ?);
    """, villes)
    conn.commit()

    # Récupérer les ID des villes insérées
    cursor.execute("SELECT id, nom FROM villes;")
    villes_db = cursor.fetchall()
    ville_map = {nom: id_ for id_, nom in villes_db}

    # 2. Insertion de plusieurs relevés historiques pour chaque ville
    maintenant = datetime.now()
    releves_generes = []

    for nom_ville, ville_id in ville_map.items():
        # Générer 5 relevés espacés de quelques heures
        for i in range(5):
            date_releve = maintenant - timedelta(hours=i * 6)
            date_str = date_releve.strftime('%Y-%m-%d %H:%M:%S')
            
            # Température et vent fictifs mais cohérents
            temperature = 15.5 + (i * 1.2)
            vitesse_vent = 10.0 + (i * 2.5)

            releves_generes.append((ville_id, temperature, vitesse_vent, date_str))

    cursor.executemany("""
    INSERT INTO releves (ville_id, temperature, vitesse_vent, date_heure) 
    VALUES (?, ?, ?, ?);
    """, releves_generes)

    conn.commit()
    conn.close()
    print("✅ Base de données peuplée avec succès !")

if __name__ == "__main__":
    peupler_base()