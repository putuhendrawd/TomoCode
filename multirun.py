import numpy as np
import pandas as pd
import geopy.distance as gd
import matplotlib.pyplot as plt
from localfunction import *
from sklearn.metrics import r2_score
import glob
plt.rcParams.update({'font.size': 14})
from matplotlib import colors
from matplotlib.colors import Colormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
pd.options.mode.chained_assignment = None

path = 'G:\\My Drive\\Tomography\\060623\\filter_update_with_real_data\\'
outputpath = path
staname = 'selected_sta_sul.txt'

files = glob.glob(path+"\\tempwadati*")
files = [Path(x).name for x in files]

# =============================================================================
# buat grafik travel time vs distance bubble plot terpisah p dan s
# =============================================================================
for file in files:
    wadati = pd.read_csv(path+file,sep='\t')
    # calculate slope and intercept
    slope, intercept = np.polyfit(wadati['dist_from_event'].astype(float),wadati['tp'].astype(float),1)

    for iter in ['p','s']:
        #plot
        fig, ax = plt.subplots(figsize = (5,5), dpi=1200)
        if iter == 'p':
            ax.scatter(wadati['dist_from_event'],wadati['tp'],color='blue',label="P-phase",edgecolors='black')
        # ax.plot(wadati['dist_from_event'],slope*wadati['dist_from_event']+intercept,'r--')
        # ax.plot(wadati['dist_from_event'],(slope*wadati['dist_from_event']+intercept)+(0.1*(slope*wadati['dist_from_event']+intercept)),'g--')
        # ax.plot(wadati['dist_from_event'],(slope*wadati['dist_from_event']+intercept)-(0.1*(slope*wadati['dist_from_event']+intercept)),'g--')
        if iter == 's':
            ax.scatter(wadati['dist_from_event'],wadati['ts'],color='red',label="S-phase",edgecolors='black')

        ax.set_xlabel('Epicentral Distance (km)')
        ax.set_ylabel('Travel Time (s)')
        ax.set_xlim([-2,1000])
        ax.set_ylim([-2,250])
        ax.legend(loc='upper left')
        fig.set_figheight(5)
        fig.set_figwidth(10)
        fig.savefig(outputpath+'Time Travel Diagram Bubble {} {}.jpg'.format(iter,Path(file).stem))