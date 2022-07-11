# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 16:14:23 2022

@author: UX425IA
"""
# =============================================================================
# membuat wadati diagram
# =============================================================================

import numpy as np
import pandas as pd
import geopy.distance as gd
import matplotlib.pyplot as plt
from localfunction import *
pd.options.mode.chained_assignment = None

path = 'E:\\My Drive\\Tomography\\LatestData\\'
outputpath = 'E:\\My Drive\\Tomography\\290622\\Wadati Plot\\'
fname = 'phase-sulawesi.dat'
staname = 'station-sulawesi.dat'
daerah = 'Sulawesi'

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
        tempdf = tempdf.drop_duplicates(subset=[0,3], keep = 'first')
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
            tempsta = (stafile.loc[x,1],stafile.loc[x,2]) #<<<< sumatera set 2,3 || indoburma set 1,2
            df.iloc[i,4] = gd.distance(temporigin,tempsta).km

del(i,originlat,originlon,temporigin,tempsta,x)

# =============================================================================
# mencari ts-tp, tp, dan jarak dari sumber ke stasiun pembaca
# =============================================================================
wadati = pd.DataFrame(columns = ['ts-tp','tp','dist'])
for a in range (len(idx)):
    #buat data per kejadian gempa
    if a == len(idx)-1:
        tempdf = df.iloc[idx[a]::]
    else:
        tempdf = df.iloc[idx[a]:idx[a+1],:]
    tempdf.drop(idx[a], inplace=True)
    tempdf = tempdf.drop_duplicates(subset=[0,3], keep = 'first')
    #cari data dengan P dan S 
    tempdf = tempdf[tempdf[0].duplicated(keep = False)]

    if tempdf.empty:
        pass
    else:
        for i in range (len(tempdf)):
            if (i%2) == 0:
                tp = tempdf.iloc[i][1]
                tstp = tempdf.iloc[i+1][1] - tp
                dist = tempdf.iloc[i][4]
                bar = pd.Series([tstp,tp,dist], index = wadati.columns)
                wadati = pd.concat([wadati,bar.to_frame(1).T], axis = 0)
    
del(tempdf,tp,tstp,i,dist,a,bar)

#cleaning wadati
wadati = wadati[wadati['tp'] > 0]
wadati = wadati[wadati['tp'] < 400]
#wadati = wadati[wadati['dist'] != '#NA']
wadati = wadati[wadati['ts-tp']>0]
# wadati = wadati[wadati['ts-tp']<180]

#parameter vp/vs calculation
wadati = wadati[['tp','ts-tp']].astype(float)
slope, intercept = np.polyfit(wadati['tp'],wadati['ts-tp'],1)

print('VP/VS = ' + str(slope + 1))

#output wadati file
#wadati.to_csv(path+'wadati_sumatera.txt',sep = '\t', index = None)

#%%
# =============================================================================
# buat grafik wadati
# =============================================================================
plt.rcParams.update({'font.size': 14})
fig, ax = plt.subplots(dpi=1200)
ax.scatter(wadati['tp'],wadati['ts-tp'])
ax.set_xlabel('tp (s)')
ax.set_ylabel('ts-tp (s)')
#ax.set_title('Wadati Diagram')
ax.set_xlim([-2,130])
ax.set_ylim([-2,130])
ax.plot(wadati['tp'],slope*wadati['tp']+intercept,'r--')
ax.text(80, 40, 'y = {:.4f}x{:+.4f}'.format(slope,intercept), fontsize=14)
ax.text(80, 25, 'Vp/Vs = {:.4f}'.format(slope+1), fontsize=14)
fig.set_figheight(5)
fig.set_figwidth(10)
fig.savefig(outputpath+'Wadati Diagram {}.jpg'.format(daerah))

