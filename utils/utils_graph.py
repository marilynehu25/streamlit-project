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
        
    def barh_subplot(self, title = None, xlabel = None,  ylabel = None,
                                path = None, yticklabels = None, xticklabels = None, colors = None,
                                legend_list = None, title_legend = None, show = True, force_new_fig= True, 
                                legend_indices=None):

        # couleurs des barres 
        if colors in self.df.columns and not self.df[colors].empty:
            valid_colors = [c for c in self.df[colors] if not pd.isna(c)]
            n_color = max(valid_colors) + 1
            self.list_colors = cmap(np.linspace(0,1,n_color))
            colors_bars = ['lightgray' if pd.isna(n) else self.list_colors[n] for n in self.df[colors]]

            hatches = ['//' if pd.isna(n) else None for n in self.df[colors]]

        elif colors is None :
            self.list_colors = None
            colors_bars = colors
            hatches = None

        # Tracer le graphique
        if self.ax is None or self.fig is None or force_new_fig:
            self.fig, self.ax = plt.subplots(figsize=self.figsize)
        
        self.bars = self.ax.barh(self.y, self.x, color = colors_bars, hatch = hatches)

        if legend_list and colors is not None:
            legend_elements = []

            # Toujours ajouter la légende pour les valeurs manquantes (None)
            if any(pd.isna(c) or c is None for c in self.df[colors]):
                legend_elements.append(mpatches.Patch(facecolor='lightgray', hatch='//', label='Indisponible'))

            if legend_indices is None:
                legend_indices = list(range(len(legend_list)))  # toutes les légendes par défaut

            for idx in legend_indices:
                if idx < len(self.list_colors) and idx < len(legend_list):
                    legend_elements.append(mpatches.Patch(facecolor=self.list_colors[idx], label=legend_list[idx]))

            self.ax.legend(handles=legend_elements, loc='best', title=title_legend)

        if xticklabels is False :
            self.ax.set_xticklabels([])
        elif xticklabels is not None : 
            self.ax.set_xticklabels(xticklabels)

        if yticklabels is False :
            self.ax.set_yticklabels([])
        elif yticklabels is not None : 
            self.ax.set_yticklabels(yticklabels)

        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title, pad=30, color='black', fontsize=16)

        self.ax.grid(axis='x', linestyle='-', alpha=0.2)

        plt.tight_layout()

        if show :
            plt.show()
            
        if path:
            plt.savefig(path, dpi=500, bbox_inches='tight')

        return self.fig

    # partie à revoir selon les besoins des missions
    def annotation(self, pourcentage  = None, Nombre = None) : 

        if pourcentage and not Nombre : 
            for n, bar in enumerate(self.bars) : 
                width = bar.get_width()
                text = self.df.loc[n,pourcentage]
                self.ax.text(width * 1.01 if not np.isnan(width) else 0 , bar.get_y() + bar.get_height() / 2,
                            text, va='center', ha='left', color='gray', fontsize=9)
                
        elif Nombre and not pourcentage : 
            for n, bar in enumerate(self.bars) : 
                width = bar.get_width()
                text = self.df.loc[n,Nombre]
                self.ax.text(width * 1.01 if not np.isnan(width) else 0 , bar.get_y() + bar.get_height() / 2,
                            text, va='center', ha='left', color='gray', fontsize=9)
        
        elif Nombre and pourcentage : 
            for n, bar in enumerate(self.bars) : 
                width = bar.get_width()
                text = f'{self.df.loc[n,Nombre]} ({self.df.loc[n,pourcentage]} %)'
                self.ax.text(width * 1.01 if not np.isnan(width) else 0 , bar.get_y() + bar.get_height() / 2,
                            text, va='center', ha='left', color='gray', fontsize=9)
                

    def encadrer(self) : 

        """iscod_index = self.df[self.df['denomination_cfa'] == 'ISCOD'].index.values[0]
        bars[iscod_index].set_edgecolor('black')  # Couleur de la bordure
        bars[iscod_index].set_linewidth(2)        # Épaisseur de la bordure """

        pass