import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import matplotlib.patches as mpatches

# partie sur les légendes à revoir

c_map = ['#000091', '#AB0345']
cmap = LinearSegmentedColormap.from_list("custom_cmap", c_map)

class plot_graph() : 
    def __init__(self,df, x, y, figsize = (10,6), ax = None, fig = None):
        self.df = df
        self.x = self.df[x]
        self.y = self.df[y]
        self.figsize = figsize
        self.ax = ax
        self.fig = fig

    