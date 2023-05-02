#%%
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:20:20 2022

@author: UX425IA
"""
import numpy as np
import pandas as pd
import geopy.distance as gd
import matplotlib.pyplot as plt
from pathlib import Path
from localfunction import *
pd.options.mode.chained_assignment = None

#%%
# =============================================================================
# Filter Absolute based on
# selected station, phase, total station report, event rms value, magnitude value
# =============================================================================

path = 'G:\\My Drive\\Tomography\\300423\\'
fname = 'phase_sul_2022_8P_wadatifilter_sta-rms5.dat'
staname = 'selected_sta_sul.txt'

# baca data stasiun ==============================================
stafile = pd.read_csv(path+staname, delim_whitespace = True,names = [i for i in range(12)])
stafile.set_index(0, inplace = True)

# baca data =======================================================
df= readabsolute(path+fname)

# filter data by rms / magnitude / depth ==============================================
dfhead = df[df[0] == '#']
# rms event filter
# dfhead[13] = dfhead[13].apply(pd.to_numeric)
# dfhead = dfhead[abs(dfhead[13]) <= 1] # fill rms here
# magnitude filter
# dfhead[10] = dfhead[10].apply(pd.to_numeric)
# dfhead = dfhead[abs(dfhead[10]) >= 5.5] # fill magnitude here
# magnitude depth
# dfhead[9] = dfhead[9].apply(pd.to_numeric)
# dfhead = dfhead[(pd.to_numeric(dfhead[9]) != 10) & (pd.to_numeric(dfhead[9]) <= 150)] # fill depth here

#header index
idx = df[df[0] == '#'].index
#temp df header
tempheader = df[df[0] == '#']
#temp df data
tempdata = pd.DataFrame([],columns = df.columns)

#filtering data
for a in range (len(idx)):
    #buat data per kejadian gempa
    if a == len(idx)-1:
        if idx[a] in dfhead.index:
            tempdf = df.iloc[idx[a]::]
        else:
            tempheader.drop(idx[a], inplace = True)
            continue
    else:
        if idx[a] in dfhead.index:
            tempdf = df.iloc[idx[a]:idx[a+1],:]
        else:
            tempheader.drop(idx[a], inplace = True)
            continue
        
    # drop header
    tempdf.drop(idx[a], inplace = True)
    
    # time bug 86400 fixer ()
    for i in range(len(tempdf.index)):
        if tempdf.iloc[i,1] <= -84000:
            tempdf.iloc[i,1] = 86400 + float(tempdf.iloc[i,1])
        elif tempdf.iloc[i,1] >= 84000:
            tempdf.iloc[i,1] = abs(-86400 + float(tempdf.iloc[i,1]))
        else:
            continue
    # time bug small negative dropper 
    tempdf = tempdf[tempdf[1] > 0]
    
    #seleksi data berdasarkan stasiun
    tempdf = tempdf[tempdf[0].isin(stafile.index)]
    #clean hanya data fasa P dan S
    # tempdf = tempdf[(tempdf[3] == 'P') | (tempdf[3] == 'S')]
    
    #seleksi data berdasarkan jumlah laporan stasiun
    if (len(tempdf) >= 8): #isi batas jumlah laporan untuk semua jenis fasa
    # if (len(tempdf[tempdf[3] == 'P']) >= 8): #isi batas jumlah laporan hanya P yang dihitung
        tempdf[2] = pd.to_numeric(df[2])
        tempdf[2] = tempdf[2].map(lambda x: '%2.1f' % x)
        tempdata = pd.concat([tempdata,tempdf])
    else:
        #hapus header
        tempheader.drop(idx[a], inplace = True)

#remake df to filtered df
df=pd.concat([tempdata,tempheader])
df.sort_index(inplace = True)
df.reset_index(inplace = True, drop = True)

#output df
df2dat(df,evnum = 1, path = path, fname=Path(fname).stem+'_8PS.dat')
print("== data filter")
readeventphase(path+Path(fname).stem+'_8PS.dat')

  #%%
# ==================================================================
# Filter Absolute based on
# Latitude and Longitude
# ==================================================================

path = 'E:\\My Drive\\Tomography\\coding\\130622\\'
fname = 'convert_indoburma-andaman-19642020_filterinside.dat'

df = readabsolute(path+fname)
dfhead = df[df[0] == '#'] #take header
dfhead[[7,8]] = dfhead[[7,8]].apply(pd.to_numeric) #make lat and lon to float64

#detail batas lat dan lon untuk seleksi
latmin = 12
latmax = 30
lonmin = 86
lonmax = 106

#seleksi data yang masuk didalam batas lat dan lon
#sintaks seleksi disini:
dfhead = dfhead[((dfhead[7] >= latmin) & (dfhead[7] <= latmax)) \
                & ((dfhead[8] >= lonmin) & (dfhead[8] <= lonmax))]

# #cari yang bukan berada di dalam batas seleksi
# header = df[df[0] == '#'] #take header
# header[[7,8]] = header[[7,8]].apply(pd.to_numeric) #make lat and lon to float64
# dfhead = header[~header.index.isin(dfhead.index)]

idx = df[df[0] == '#'].index
#temp df header
tempheader = df[df[0] == '#']
#temp df data
tempdata = pd.DataFrame([],columns = df.columns)

#filtering data
for a in range (len(idx)):
    #buat data per kejadian gempa
    if a == len(idx)-1:
        if idx[a] in dfhead.index:
            tempdf = df.iloc[idx[a]::]
        else:
            tempheader.drop(idx[a], inplace = True)
            continue
    else:
        if idx[a] in dfhead.index:
            tempdf = df.iloc[idx[a]:idx[a+1],:]
        else:
            tempheader.drop(idx[a], inplace = True)
            continue
        
    #drop header
    tempdf.drop(idx[a], inplace = True)
    
    #seleksi data berdasarkan jumlah laporan stasiun
    if (len(tempdf.index) >= 1):
        tempdf[2] = pd.to_numeric(df[2])
        tempdf[2] = tempdf[2].map(lambda x: '%2.1f' % x)
        tempdata = pd.concat([tempdata,tempdf])
    else:
        #hapus header
        tempheader.drop(idx[a], inplace = True)

#remake df to filtered df
dfres=pd.concat([tempdata,tempheader])
dfres.sort_index(inplace = True)
dfres.reset_index(inplace = True, drop = True)

#output df
df2dat(dfres,evnum = 1, path = path, fname=Path(fname).stem+'_filterlatlon.dat')

#%%
# =============================================================================
# Filter Absolute based on
# station rms value
# =============================================================================

path = "G:\\My Drive\\Tomography\\300423\\"
absname = "phase_sul_2022_8P_wadatifilter.dat"
staname = 'selected_sta_sul.txt'
resname = 'tomoDD.res'

#read data
dfabs = readabsolute(path+absname)
dfsta = readsta(path+staname)
dfres = readres(path+resname)

#init tempdata
tempdata = pd.DataFrame([],columns = dfabs.columns)

#processing
RMSv_LIMIT = 7
tempheader = dfabs[dfabs[0] == '#']
idx = tempheader.index

for a in range (len(idx)):
    #load abs data
    if a == len(idx)-1:
        tempdfabs = dfabs.iloc[idx[a]+1::]
    else:
        tempdfabs = dfabs.iloc[idx[a]+1:idx[a+1],:]
    
    #load res data    
    tempdfres = dfres[dfres["C1"] == int(tempheader.loc[idx[a]][14])]

    #process
    for i in tempdfabs.index:
        st_ = tempdfabs.loc[[i]][0][i]
        if not tempdfres[tempdfres["STA"] == st_].empty:
            if (abs(tempdfres[tempdfres["STA"] == st_].RES.values[0]) > RMSv_LIMIT):
                tempdfabs.drop([i], inplace=True)
        else:
            tempdfabs.drop([i], inplace=True)
    tempdata = pd.concat([tempdata,tempdfabs])

dfresult=pd.concat([tempdata,tempheader])
dfresult.sort_index(inplace = True)
dfresult.reset_index(inplace = True, drop = True)

#output
df2dat(dfresult,evnum = 1, path = path, fname=Path(absname).stem+f'_sta-rms{RMSv_LIMIT}.dat')
readeventphase(path+Path(absname).stem+f'_sta-rms{RMSv_LIMIT}.dat')