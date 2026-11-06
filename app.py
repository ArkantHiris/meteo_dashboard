import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Météo ETL Dashboard", page_icon="🌤️", layout="wide")

st.title("🌤️ Dashboard Météo - Clean Architecture & Analytics")

# menu
menu = st.sidebar.selectbox("Navigation", ["Tableau de bord", "Gestion des Villes", "Lancer le pipeline ETL"])

# Tableau de bord 
if menu == "Tableau de bord":
    st.header("📊 Vue d'ensemble et Analyses Météo")

    # Bouton de rafraîchissement manuel des données
    col_btn_ref, _ = st.columns([1, 4])
    with col_btn_ref:
        if st.button("🔄 Rafraîchir les données"):
            st.rerun()

    # Gestion du chargement et des erreurs d'API
    try:
        with st.spinner("Chargement des données depuis l'API..."):
            resp_villes = requests.get(f"{API_URL}/villes", timeout=15)
            resp_releves = requests.get(f"{API_URL}/releves", timeout=15)
            
            resp_villes.raise_for_status()
            resp_releves.raise_for_status()
            
            villes = resp_villes.json()
            releves = resp_releves.json()

    except requests.exceptions.ConnectionError:
        st.error("⚠️ **Erreur de connexion** : Impossible de joindre l'API FastAPI. Vérifiez qu'elle tourne bien sur `http://127.0.0.1:8000`.")
        st.stop()
    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ **Erreur HTTP** : {e}")
        st.stop()

    if not releves:
        st.info("ℹAucun relevé météo disponible. Allez dans l'onglet **'Lancer le pipeline ETL'** pour récupérer des données.")
    else:
        # Conversion en DataFrames Pandas
        df_releves = pd.DataFrame(releves)
        df_villes = pd.DataFrame(villes)
        
        # S'assurer que la date est au bon format datetime
        df_releves["date_heure"] = pd.to_datetime(df_releves["date_heure"])

        # Filtres 
        st.sidebar.markdown("---")
        st.sidebar.subheader("Filtres du Dashboard")

        # 1. Filtre par Ville (Multiselect)
        villes_disponibles = df_releves["ville_nom"].unique().tolist()
        villes_selectionnees = st.sidebar.multiselect(
            "Filtrer par ville",
            options=villes_disponibles,
            default=villes_disponibles
        )

        # 2. Filtre par Plage de Dates
        min_date = df_releves["date_heure"].min().date()
        max_date = df_releves["date_heure"].max().date()
        
        date_range = st.sidebar.date_input(
            "Plage de dates",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # Application des filtres sur le DataFrame
        if villes_selectionnees:
            df_releves = df_releves[df_releves["ville_nom"].isin(villes_selectionnees)]

        if len(date_range) == 2:
            start_date, end_date = date_range
            df_releves = df_releves[
                (df_releves["date_heure"].dt.date >= start_date) & 
                (df_releves["date_heure"].dt.date <= end_date)
            ]

        if df_releves.empty:
            st.warning("⚠️ Aucun relevé ne correspond aux filtres sélectionnés.")
        else:

            # Carte 
            st.subheader("🗺️ Localisation des Villes Observées")
            if not df_villes.empty:
                # Filtrer aussi les villes sur la carte si l'utilisateur filtre dans le multiselect
                df_villes_filtered = df_villes[df_villes["nom"].isin(villes_selectionnees)] if villes_selectionnees else df_villes
                st.map(df_villes_filtered, latitude="latitude", longitude="longitude", zoom=5, use_container_width=True)

            st.markdown("---")

            # Courbes
            st.subheader("📈 Évolution temporelle")
            
            st.markdown("### 🌡️ Température (°C)")
            fig_temp = px.line(
                df_releves, 
                x="date_heure", 
                y="temperature", 
                color="ville_nom", 
                markers=True,
                labels={"date_heure": "Date et Heure", "temperature": "Température (°C)", "ville_nom": "Ville"}
            )
            st.plotly_chart(fig_temp, use_container_width=True)

            st.markdown("---")

            st.markdown("### 💨 Vitesse du Vent (km/h)")
            fig_vent = px.line(
                df_releves, 
                x="date_heure", 
                y="vitesse_vent", 
                color="ville_nom", 
                markers=True,
                labels={"date_heure": "Date et Heure", "vitesse_vent": "Vent (km/h)", "ville_nom": "Ville"}
            )
            st.plotly_chart(fig_vent, use_container_width=True)

# gestion des villes
elif menu == "Gestion des Villes":
    st.header("📍 Villes enregistrées et Ajout")
    
    # Formulaire d'ajout
    with st.form("form_ajout_ville"):
        st.subheader("Ajouter une nouvelle ville")
        nom = st.text_input("Nom de la ville")
        latitude = st.number_input("Latitude",  format="%.4f", min_value=-90.0, max_value=90.0)
        longitude = st.number_input("Longitude",  format="%.4f", min_value=-180.0, max_value=180.0)
        
        if st.form_submit_button(label="Enregistrer la ville"):
            if nom.strip():
                try:
                    res = requests.post(f"{API_URL}/villes", json={"nom": nom, "latitude": latitude, "longitude": longitude})
                    if res.status_code == 201:
                        st.success(f"Ville '{nom}' ajoutée avec succès ! 🎉")
                    else:
                        st.error(f"Erreur : {res.json().get('detail')}")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ API injoignable.")
            else:
                st.warning("Le nom ne peut pas être vide.")

    st.markdown("---")
    # Affichage du tableau des villes
    try:
        resp = requests.get(f"{API_URL}/villes")
        if resp.status_code == 200:
            villes = resp.json()
            if villes:
                st.dataframe(pd.DataFrame(villes), use_container_width=True)
    except:
        pass

# Lancer la pipeline
elif menu == "Lancer le pipeline":
    st.header("⚡ Exécution du pipeline Météo")
    st.markdown("Déclenchez la récupération des données en direct via Open-Meteo pour l'ensemble de vos villes.")
    
    if st.button("🚀 Lancer la mise à jour météo"):
        with st.spinner("Récupération des données en cours..."):
            try:
                response = requests.post(f"{API_URL}/pipeline/run") 
                if response.status_code == 200:
                    data = response.json()
                    st.success(data.get("message", "Pipeline exécuté avec succès !"))
                    st.json(data.get("details"))
                else:
                    st.error(f"Erreur : {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Impossible de contacter l'API FastAPI.")