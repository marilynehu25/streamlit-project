import pandas as pd
import numpy as np
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, to_hex
import matplotlib.patches as mpatches
from io import BytesIO

import utils.utils_graph as utils_graph
from utils.utils_graph import plot_graph

from onglets import onglet1

st.title('Logiciel cartographique')

option = st.sidebar.selectbox("Choisir le format du graphique :", ("Graphique en barre horizontale","Histogramme"))

if option == "Graphique en barre horizontale" : 
    onglet1.display()