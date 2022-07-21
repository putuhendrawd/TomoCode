# ======================================================
# buat epicenter distance vs ray number
# ======================================================

from symtable import Symbol
import numpy as np
import pandas as pd
import geopy.distance as gd
import matplotlib.pyplot as plt
from localfunction import *
import math
pd.options.mode.chained_assignment = None

path = 'E:\\My Drive\\Tomography\\190722\\TaupyRUN\\'
outputpath = 'E:\\My Drive\\Tomography\\190722\\TaupyRUN\\'
fname = 'phase-indoburma-3-fixed-plus-filter510-rms3.dat'
staname = 'station-indoburma.dat'
daerah = 'Indoburma510'

# =============================================================================
# baca data dan cleaning
# =============================================================================
df= readabsolute(path+fname)

#header index
idx = df[df[0] == '#'].index

#header
tempheader = df[df[0]== '#']

#tempat data
tempdata = pd.DataFrame([],columns = df.columns)

#cleaning data
for a in range (len(idx)):
    #buat data per kejadian gempa
    if a == len(idx)-1:
        tempdf = df.iloc[idx[a]::]
    else:
        tempdf = df.iloc[idx[a]:idx[a+1],:]
    #drop header
    tempdf.drop(idx[a], inplace = True)
    if (len(tempdf.index) >= 1):
        #clean hanya data fasa P dan S
        tempdf = tempdf[(tempdf[3] == 'P') | (tempdf[3] == 'S')]
        #drop duplikat stasiun dan fasa
        tempdf = tempdf.drop_duplicates(subset=[0], keep = 'first')
        tempdf[2] = pd.to_numeric(df[2])
        tempdf[2] = tempdf[2].map(lambda x: '%2.1f' % x)
        tempdata = pd.concat([tempdata,tempdf])
    else:
        #hapus header
        tempheader.drop(idx[a], inplace = True)

df = pd.concat([tempdata,tempheader])
df.sort_index(inplace = True)
df.reset_index(inplace = True, drop = True)

del(tempdf,tempdata,tempheader,a)

#baca ulang header index
idx = df[df[0] == '#'].index

# =============================================================================
# baca database stasiun inatews
# =============================================================================
# stafile = pd.read_csv(path+'sumatera_phase_data/stations_new_inatews.txt', sep ='\t',names = [0,1,2,3,4])
# stafilenantrue = stafile[stafile[2].isnull() == true].index.to_list()
# stafile.iloc[stafilenantrue,2::] = stafile.iloc[stafilenantrue,2::].shift(periods = -1, axis = 1)
# stafile.drop(columns = 4, inplace = true)
# stafile.set_index(1, inplace = true)
# stafile = stafile[~stafile.index.duplicated(keep = 'first')]

# del(stafilenantrue)

# =============================================================================
# baca database stasiun indoburma
# =============================================================================
stafile = pd.read_csv(path+staname, delim_whitespace = True,names = [0,1,2,3])
stafile.set_index(0, inplace = True)

# =============================================================================
# cek ketersediaan stasiun di database stasiun
# =============================================================================
staavail = pd.DataFrame(columns = ['STA', 'Available'])
staavail['STA'] = df[0].unique()
for i in staavail.index:
    item = r'^' + str(staavail['STA'][i]) + '$'
    staavail['Available'][i] = stafile.index.str.match(item).any()
staavail.set_index('STA', inplace = True)

del(i,item)

# =============================================================================
# hitung jarak stasiun dari kejadian gempa
# =============================================================================
for i in df.index:
    if i in idx:
        originlat = df.iloc[i,7]
        originlon = df.iloc[i,8]
        temporigin = (df.iloc[i,7],df.iloc[i,8])
    else:
        x = df.iloc[i,0]
        if staavail.loc[x].any() == False:
            df.iloc[i,4] = '#NA'
        else:
            tempsta = (stafile.loc[x,1],stafile.loc[x,2]) #<<<< set lat and lon position
            df.iloc[i,4] = gd.distance(temporigin,tempsta).km
            df.iloc[i,5] = df.iloc[i,4] / 111

del(i,originlat,originlon,temporigin,tempsta,x)

#%%
# =============================================================================
# collect data and plot
# =============================================================================

raydf = df[df[0] != '#']
raydf = raydf[raydf[4] != '#NA']
raydfdeg = raydf[4].mul(0.01).sub(1.11).to_list()

from matplotlib.ticker import PercentFormatter
fig, ax = plt.subplots(dpi=1200)
ax.hist(raydfdeg, bins = np.arange(-1, 23, 2),weights=np.ones(len(raydfdeg)) / len(raydfdeg), align = 'mid',edgecolor='black',facecolor ='grey')
ax.set_xlim([-1,math.ceil(max(raydfdeg))+1])
ax.set_xlabel('Epicentral distance (deg)')
ax.set_ylabel('Ray Number (%)')
#ax.set_yticks(range(0,50,10))
ax.set_xticks(range(0,math.ceil(max(raydfdeg)),4))
ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0,symbol = None))
fig.savefig(outputpath+'Ray Distance Histogram {}.jpg'.format(daerah))