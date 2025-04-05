# Onglet pour tracer les histogrammes en barre horizontable

import streamlit as st
import pandas as pd
from matplotlib.colors import to_hex
from io import BytesIO
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

import utils.utils_graph as utils_graph

def display() : 
    upload_file = st.file_uploader('Charger vos données en format .csv ou .xlsx.')

    if upload_file is not None : 

        # chargement des données
        filename = upload_file.name 

        # vérifie la forme des données
        if filename.endswith('.csv'):
            df = pd.read_csv(upload_file)
            st.success("Fichier CSV chargé avec succès.")

        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(upload_file)
            st.success("Fichier Excel chargé avec succès.")

        else:
            st.error("Format de fichier non supporté. Veuillez charger un .csv ou un .xlsx.")

        # visualisation des données
        st.header('Visualisation des données :')
        st.dataframe(df, use_container_width=True)