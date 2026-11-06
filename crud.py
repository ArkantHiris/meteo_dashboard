from schema import VilleModel

def inserer_ville(conn, ville: VilleModel) -> int:

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM villes WHERE nom = ?;", (ville.nom,))
    result = cursor.fetchone()
    
    if result:
        return result["id"]
    
    cursor.execute(
        "INSERT INTO villes (nom, latitude, longitude) VALUES (?, ?, ?);",
        (ville.nom, ville.latitude, ville.longitude)
    )
    conn.commit()
    return cursor.lastrowid


def inserer_releve(conn, ville_id: int, temperature: float, vitesse_vent: float, date_heure: str):
    
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO releves (ville_id, temperature, vitesse_vent, date_heure) 
        VALUES (?, ?, ?, ?);
        """,
        (ville_id, temperature, vitesse_vent, date_heure)
    )
    conn.commit()

def recuperer_toutes_les_villes(conn):

    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, latitude, longitude FROM villes;")
    return cursor.fetchall()

def recuperer_tous_les_releves(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, r.ville_id, v.nom as ville_nom, r.temperature, r.vitesse_vent, r.date_heure
        FROM releves r
        JOIN villes v ON r.ville_id = v.id
        ORDER BY r.date_heure ASC;
    """)
    return cursor.fetchall()