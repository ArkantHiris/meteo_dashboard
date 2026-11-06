# 🌤️ Meteo Dashboard & ETL Pipeline

Un pipeline ETL météorologique robuste et une application de tableau de bord moderne, développés avec une architecture modulaire séparant le backend (**FastAPI**), la couche de données (**SQLite**), et le frontend interactif (**Streamlit**).



## 🏗️ Architecture du Projet

Le projet suit une architecture propre et découplée :
- **FastAPI (Backend / API)** : Expose les routes sécurisées et valide les flux de données grâce à **Pydantic**.
- **Streamlit (Frontend / Interface)** : Fournit un tableau de bord dynamique, des filtres interactifs et des visualisations graphiques avec **Plotly**.
- **SQLite (Base de Données)** : Stocke durablement les informations des villes et l'historique des relevés météo.
- **Pipeline ETL (Services)** : Interroge automatiquement l'API externe **Open-Meteo** pour récupérer les données en temps réel.



## 📂 Structure des Fichiers

meteo_dashboard/
│
├── main.py            # Point d'entrée de l'API FastAPI (Routes GET/POST)
├── app.py             # Interface utilisateur Streamlit (Dashboard)
├── database.py        # Connexion et initialisation de la base SQLite
├── crud.py            # Fonctions d'interaction avec la base de données (SQL)
├── services.py        # Logique du pipeline (Appel à Open-Meteo)
├── model.py           # Modèle basique dont vont hériter les class dans schemas
├── schemas.py         # Modèles de validation Pydantic 
├── meteo.db           # Base de donnée générée automatiquement par le script database.py
├── requirements.txt   # Liste des dépendances Python
├── seed.py            # Petit script pour peupler la db pendant le développement 
└── .gitignore         # Fichiers exclus de Git (base de données, caches)



## 🚀 Guide d'Installation et de Démarrage

1. Cloner le dépôt

```bash
git clone https://github.com/ArkantHiris/meteo_dashboard.git
```


2. Créer et activer un environnement virtuel

```bash
python -m venv .venv
# Sur Windows :
.venv\Scripts\activate
# Sur Linux / macOS :
source .venv/bin/activate
```


3. Installer les dépendances

```bash
pip install -r requirements.txt
```


## 🏃‍♂️ Exécution de l'Application

Le projet nécessite de lancer deux services en parallèle (dans deux terminaux distincts).


= >Terminal 1 : Lancer le Backend (FastAPI) : 

```bash
uvicorn main:app --reload
```

L'API sera accessible sur : http://127.0.0.1:8000
Documentation interactive (Swagger) : http://127.0.0.1:8000/docs


=> Terminal 2 : Lancer le Frontend (Streamlit) :

```bash
streamlit run app.py
```

Le tableau de bord s'ouvrira automatiquement sur : http://localhost:8501
(Normalement, streamlit ouvre automatiquement la page navigateur)


## 📊 Fonctionnalités du Dashboard

    - Gestion des Villes : Ajout et suivi de différentes localisations géographiques.
    - Pipeline : Récupération automatisée des températures et vitesses de vent.
    - Filtres Dynamiques : Filtrage par ville (multiselect) et par plage de dates.
    - Graphiques Interactifs : Courbes temporelles fluides propulsées par Plotly.


## 🛠️ Technologies Utilisées

    - Python 3.10+
    - FastAPI & Uvicorn
    - Streamlit & Plotly
    - Pydantic
    - SQLite
    - Pandas
    - Requests & Open-Meteo API