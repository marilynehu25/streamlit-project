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

        # bloc sur les infos du dataframe 
        st.subheader('Information sur les données :')
        with st.expander("📊 Aperçu"):
            st.markdown(f"**Dimensions :** {df.shape[0]} lignes × {df.shape[1]} colonnes")
            st.markdown("**Colonnes disponibles :**")
            st.write(list(df.columns))
            st.markdown("**Types de données :**")
            st.write(df.dtypes)

        st.subheader('Choix d\'option  :')
        nb_line = st.number_input(
            "Nombre de lignes à afficher",
            min_value=1,
            max_value=len(df),
            value=5,
            step=1,
            format="%d"  # ← force l'affichage et le retour d'un entier
        )

        # choix des colonnes à tracer
        columns = df.columns.tolist()

        float_cols = df.select_dtypes(include=['float', 'int']).columns

        if len(float_cols) > 0:
            default_index = columns.index(float_cols[0])
            col_x = st.selectbox("Choisir la colonne des valeurs (x)", columns, index=default_index)
        else:
            col_x = st.selectbox("Choisir la colonne des valeurs (x)", columns)

        col_y = st.selectbox('Choisir la colonne des catégories (y)', columns)
        
        title_choice = st.checkbox("Voulez-vous mettre un titre au graphique ?")
        if title_choice:
            title = st.text_input("Entrez le titre du graphique :", key="title_input")
        else:
            title = None

        # création du modèle de graphe et message si erreur pour la sélection des colonnes
        model_graph = utils_graph.plot_graph(df = df.loc[:nb_line-1, :], x = col_x, y = col_y, figsize=(13, nb_line*0.7))

        col_nombre, col_pourcentage = st.columns(2)

        with col_nombre : 
            x_choice = st.checkbox("Voulez-vous nommer l'axe des abscisses ?", key = "xlabel_choice")
            if x_choice:
                xlabel = st.text_input("Entrez le nom de l'axe des abscisses :", key="xlabel_input")
            else:
                xlabel = None

            nombre_choice = st.checkbox('Afficher la valeur absolue de chaque barre ?')
            if nombre_choice : 
                nombre = st.selectbox('Nom de la colonne des valeurs :', columns)
            else :
                nombre = None
        
        with col_pourcentage :
            y_choice = st.checkbox("Voulez-vous nommer l'axe des ordonnées ?", key = "ylabel_choice")
            if y_choice:
                ylabel = st.text_input("Entrez le nom de l'axe des ordonnées :", key="ylabel_input")
            else:
                ylabel = None

            pourcentage_choice = st.checkbox('Afficher le pourcentage de chaque barre ?')
            if pourcentage_choice :
                pourcentage = st.selectbox('Nom de la colonne des pourcentages :', columns)
            else : 
                pourcentage = None

        # partie encadrement 
        options = df[col_y]
        encadrement_choice = st.checkbox('Voulez-vous mettre en avant une barre ?')
        if encadrement_choice : 
            selection = st.multiselect("Choisissez les CFA à encadrer :", options)
        else :
            selection = None

        # partie pour la couleur des barres et de la légende

        legend_choice = st.checkbox('Voulez-vous mettre une légende de couleurs ?')

        if legend_choice:
            col_color = st.selectbox('Choisir la colonne des numéros de couleurs', columns)

            try : 
                # Premier tracé pour générer list_colors
                model_graph.barh_subplot(colors=col_color, show=False, title= title, xlabel= xlabel, ylabel=ylabel)

                colors_rgba = model_graph.list_colors

                custom_colors = {}
                legend_labels = []
                legend_indices = []

                st.markdown("Personnalisation des couleurs et des légendes :")

                for i, rgba in enumerate(colors_rgba):
                    hex_color = to_hex(rgba)
                    col1, col2 = st.columns(2)
                    with col1:
                        picked_color = st.color_picker(f"Couleur {i+1}", hex_color)
                    with col2:
                        label = st.text_input(f"Légende {i+1}", key=f"legend_{i}")

                    if label.strip():  # légende non vide
                        legend_labels.append(label)
                        legend_indices.append(i)
                        custom_colors[i] = {"color": picked_color, "label": label}

                # Retracer avec légendes non vides
                barh = model_graph.barh_subplot(
                    colors=col_color,
                    legend_list=legend_labels,
                    title_legend="Légende",
                    legend_indices=legend_indices, 
                    title= title, 
                    xlabel= xlabel,
                    ylabel= ylabel, 
                    show = False
                )

                model_graph.annotation(pourcentage= pourcentage, Nombre= nombre)
                model_graph.encadrer(selection=selection)

                st.pyplot(barh)
            
            except Exception as e:
                st.warning("⚠️ Cette colonne ne semble pas contenir des numéros de couleurs valides.")

        else:
            # Tracer sans légende
            barh = model_graph.barh_subplot(title= title, xlabel= xlabel, ylabel= ylabel, show=False)
            model_graph.annotation(pourcentage= pourcentage, Nombre= nombre)
            model_graph.encadrer(selection=selection)

            st.pyplot(barh)

        if 'barh' in locals():
            img_buffer = BytesIO()
            barh.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)

            st.download_button(
                label="📥 Télécharger le graphique",
                data=img_buffer,
                file_name="mon_graphique.png",
                mime="image/png")