# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 16:14:23 2022

@author: UX425IA
"""
#%%
# =============================================================================
# membuat wadati diagram
# =============================================================================

import numpy as np
import pandas as pd
import geopy.distance as gd
import matplotlib.pyplot as plt
from localfunction import *
from sklearn.metrics import r2_score
pd.options.mode.chained_assignment = None

path = "G:\\My Drive\\Tomography\\280823\\data-fase-indoburma-11072023\\"
outputpath = path
fname = 'phase-indoburma-3-fixed_filter5sta_plusehb_filter_sta_rms_stasiunfilter.dat'
staname = 'sta-usul-2-filter.txt'

#%%
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
wadati = pd.DataFrame(columns = ['sta','tp','ts','ts-tp','dist_from_event','event_id'])
for a in range (len(idx)):
    #buat data per kejadian gempa
    if a == len(idx)-1:
        tempdf = df.iloc[idx[a]::]
    else:
        tempdf = df.iloc[idx[a]:idx[a+1],:]
    event_id=df.iloc[idx[a],14]
    tempdf.drop(idx[a], inplace=True)
    tempdf = tempdf.drop_duplicates(subset=[0,3], keep = 'first')
    #cari data dengan P dan S 
    tempdf = tempdf[tempdf[0].duplicated(keep = False)]

    if tempdf.empty:
        pass
    else:
        for i in range (len(tempdf)):
            if (i%2) == 0:
                sta = tempdf.iloc[i][0]
                tp = tempdf.iloc[i][1]
                ts = tempdf.iloc[i+1][1]
                tstp = ts - tp
                dist = tempdf.iloc[i][4]
                bar = pd.Series([sta,tp,ts,tstp,dist,event_id], index = wadati.columns)
                wadati = pd.concat([wadati,bar.to_frame(1).T], axis = 0)
df.to_csv(outputpath+f'temppha_{Path(fname).stem}.txt',sep = '\t', index = None)
# del(tempdf,tp,tstp,i,dist,a,bar)

#cleaning wadati
wadati = wadati[wadati['tp'] > 0]
wadati = wadati[wadati['tp'] < 500]
wadati = wadati[wadati['dist_from_event'] != '#NA']
wadati = wadati[wadati['ts-tp']>0]
wadati = wadati[wadati['ts-tp']<350]

#output wadati file
wadati.to_csv(outputpath+f'tempwadati_{Path(fname).stem}.txt',sep = '\t', index = None)

#%%
#parameter vp/vs calculation
slope, intercept = np.polyfit(wadati['tp'].astype(float),wadati['ts-tp'].astype(float),1)

#manual slope
# slope = 0.589
# intercept = 0.917

#make predict
predict = np.poly1d([slope, intercept])

#hitung batas atas dan bawah regresi vp/vs
predictup = np.poly1d([slope,intercept+9.5])
predictdown = np.poly1d([slope,intercept-9.5])

#hitung stdev
std = np.std(wadati['ts-tp'])

#hitung standard_error
residuals = wadati['ts-tp'].to_numpy() - predict(wadati['tp'])
residuals = residuals**2
standard_error = (sum(residuals)/(len(residuals)-2))**0.5

#cek r-square score
r2 = r2_score(wadati['ts-tp'],predict(wadati['tp']))

print('VP/VS = ' + str(slope + 1))
print(f"R-square = {r2}")
print(f"std_err = {standard_error}")

#%%
# =============================================================================
# buat grafik wadati
# =============================================================================
#init
plt.rcParams.update({'font.size': 14})
fig, ax = plt.subplots(figsize = (5,5), dpi=1200)
ax.set_xlabel('tp (s)')
ax.set_ylabel('ts-tp (s)')
#ax.set_title('Wadati Diagram')
ax.set_xlim([0,500])
ax.set_ylim([-2,350])
#plot scatter data
ax.scatter(wadati['tp'],wadati['ts-tp'])
#sort data for antibacktracking plot
wadatis = wadati.sort_values('tp')
#plot regression line
ax.plot(wadatis['tp'],predict(wadatis['tp']),'r--')
# percentage error
# ax.plot(wadati['tp'],(slope*wadati['tp']+intercept)+(0.1*(slope*wadati['tp']+intercept)),'r--')
# ax.plot(wadati['tp'],(slope*wadati['tp']+intercept)-(0.1*(slope*wadati['tp']+intercept)),'r--')
# fix error 
# ax.plot(wadatis['tp'],predictup(wadatis['tp']),'r-')
# ax.plot(wadatis['tp'],predictdown(wadatis['tp']),'r-')
#add additional legend data
ax.text(300, 100, 'y = {:.4f}x{:+.4f}'.format(slope,intercept), fontsize=14)
ax.text(300, 75, 'Vp/Vs = {:.4f}'.format(slope+1), fontsize=14)
ax.text(300, 50, f'R$^2$ = {r2:.3f}', fontsize=14)
#add-on
fig.set_figheight(5)
fig.set_figwidth(10)
fig.savefig(outputpath+'Wadati Diagram {}.jpg'.format(Path(fname).stem))

# %%
# =============================================================================
# buat grafik travel time vs distance density plot 
# =============================================================================
plt.rcParams.update({'font.size': 14})
from matplotlib import colors
from matplotlib.colors import Colormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
fig, ax = plt.subplots(figsize = (5,5), dpi=1200)
# ax.scatter(wadati['dist'],wadati['tp'],color='blue',label="P-phase",edgecolors='black')
# ax.scatter(wadati['dist'],wadati['ts'],color='red',label="S-phase",edgecolors='black')
tp_ax = ax.hist2d(wadati['dist_from_event'],wadati['tp'],bins=[100,40],norm=colors.LogNorm(vmin=1,vmax=1000),cmap="Greens")
ts_ax = ax.hist2d(wadati['dist_from_event'],wadati['ts'],bins=[100,40],norm=colors.LogNorm(vmin=1,vmax=1000),cmap="Oranges",cmin=5)

ax.set_xlabel('Epicentral Distance (km)')
ax.set_ylabel('Travel Time (s)')
ax.set_xlim([-2,4000])
ax.set_ylim([-2,800])
fig.set_figheight(5)
fig.set_figwidth(10)
cbax1 = inset_axes(ax, width="30%", height="3%", loc=2,bbox_to_anchor=(0.05, 0, 1, 1),bbox_transform=ax.transAxes)
cbax2 = inset_axes(ax, width="30%", height="3%", loc=2,bbox_to_anchor=(0.05, -0.12, 1, 1),bbox_transform=ax.transAxes)  
ax.text(0.02,0.93,'P', transform=ax.transAxes, fontsize=18)
ax.text(0.02,0.81,'S', transform=ax.transAxes, fontsize=18)
fig.colorbar(tp_ax[3], cax=cbax1, orientation='horizontal')
fig.colorbar(ts_ax[3], cax=cbax2, orientation='horizontal')
fig.savefig(outputpath+'Time Travel Diagram {}.jpg'.format(Path(fname).stem))

# %%
# =============================================================================
# buat grafik travel time vs distance bubble plot
# =============================================================================
plt.rcParams.update({'font.size': 14})
from matplotlib import colors
from matplotlib.colors import Colormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# calculate slope and intercept
slope, intercept = np.polyfit(wadati['dist_from_event'].astype(float),wadati['tp'].astype(float),1)

#plot
fig, ax = plt.subplots(figsize = (5,5), dpi=1200)
ax.scatter(wadati['dist_from_event'],wadati['tp'],color='blue',label="P-phase",edgecolors='black',s=1)
# ax.plot(wadati['dist_from_event'],slope*wadati['dist_from_event']+intercept,'r--')
# ax.plot(wadati['dist_from_event'],(slope*wadati['dist_from_event']+intercept)+(0.1*(slope*wadati['dist_from_event']+intercept)),'g--')
# ax.plot(wadati['dist_from_event'],(slope*wadati['dist_from_event']+intercept)-(0.1*(slope*wadati['dist_from_event']+intercept)),'g--')
ax.scatter(wadati['dist_from_event'],wadati['ts'],color='red',label="S-phase",edgecolors='black',s=1)

ax.set_xlabel('Epicentral Distance (km)')
ax.set_ylabel('Travel Time (s)')
ax.set_xlim([-2,4000])
ax.set_ylim([-2,800])

# ax.legend()
ax.text(wadati['dist_from_event'].max()+50, wadati['tp'].max(), f'P', fontsize=20)
ax.text(wadati['dist_from_event'].max()+50, wadati['ts'].max(), f'S', fontsize=20)

fig.set_figheight(5)
fig.set_figwidth(10)
fig.savefig(outputpath+'Time Travel Diagram Bubble {}.jpg'.format(Path(fname).stem))

# %%
# =============================================================================
# buat grafik travel time vs distance bubble plot terpisah p dan s
# =============================================================================
plt.rcParams.update({'font.size': 14})
from matplotlib import colors
from matplotlib.colors import Colormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# calculate slope and intercept
slope, intercept = np.polyfit(wadati['dist_from_event'].astype(float),wadati['tp'].astype(float),1)

for iter in ['p','s']:
    #plot
    fig, ax = plt.subplots(figsize = (5,5), dpi=1200)
    if iter == 'p':
        ax.scatter(wadati['dist_from_event'],wadati['tp'],color='blue',label="P-phase",edgecolors='black', s=1)
    # ax.plot(wadati['dist_from_event'],slope*wadati['dist_from_event']+intercept,'r--')
    # ax.plot(wadati['dist_from_event'],(slope*wadati['dist_from_event']+intercept)+(0.1*(slope*wadati['dist_from_event']+intercept)),'g--')
    # ax.plot(wadati['dist_from_event'],(slope*wadati['dist_from_event']+intercept)-(0.1*(slope*wadati['dist_from_event']+intercept)),'g--')
    if iter == 's':
        ax.scatter(wadati['dist_from_event'],wadati['ts'],color='red',label="S-phase",edgecolors='black', s=1)

    ax.set_xlabel('Epicentral Distance (km)')
    ax.set_ylabel('Travel Time (s)')
    ax.set_xlim([-2,350])
    ax.set_ylim([-2,80])
    ax.legend(loc='upper left')
    fig.set_figheight(5)
    fig.set_figwidth(8)
    fig.savefig(outputpath+'Time Travel Diagram Bubble {} {}.jpg'.format(iter,Path(fname).stem))
# %%
