import sqlite3

DB_NAME = "meteo.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS villes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS releves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ville_id INTEGER NOT NULL,
        temperature REAL NOT NULL,
        vitesse_vent REAL NOT NULL,
        date_heure TEXT NOT NULL,
        FOREIGN KEY (ville_id) REFERENCES villes (id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()