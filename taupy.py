'''
Coding: PYTHON UTF-8
Created On: 2022-07-19 16:42:30
Author: Putu Hendra Widyadharma
=== compare arrival time vs syntetic arrival time using taupy
'''

from symtable import Symbol
import numpy as np
import pandas as pd
import geopy.distance as gd
import matplotlib.pyplot as plt
from localfunction import *
import math
pd.options.mode.chained_assignment = None

import obspy
from obspy.taup import TauPyModel
mod = "ak135"
model = TauPyModel(model=mod)


path = 'D:\\BMKG Putu\\Tomography\\210722\\taupy-sulawesi\\'
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
        depth = df.iloc[i,9]
        temporigin = (df.iloc[i,7],df.iloc[i,8])
    else:
        x = df.iloc[i,0]
        phase = df.iloc[i,3]
        if staavail.loc[x].any() == False:
            df.iloc[i,4] = '#NA'
        else:
            tempsta = (stafile.loc[x,1],stafile.loc[x,2]) #<<<< set lat and lon position
            df.iloc[i,4] = gd.distance(temporigin,tempsta).km #distance in km
            df.iloc[i,5] = df.iloc[i,4] / 111 #distance in degree
            try:
                z = model.get_travel_times(source_depth_in_km=float(depth), distance_in_degree=df.iloc[i,5], phase_list=phase.lower())
                z = z[0]
            except:
                z = model.get_travel_times(source_depth_in_km=float(depth), distance_in_degree=df.iloc[i,5], phase_list=phase)
                z = z[0]
            df.iloc[i,6] = z.time # calculatedarrival time 
            df.iloc[i,7] = df.iloc[i,1] - df.iloc[i,6]
del(i,originlat,originlon,temporigin,tempsta,x)

#save data to csv
df.to_csv(path+"output_data_{}.csv".format(mod))

#make plot of diff time
diffdf = df[df[0] != '#']
diffdf = diffdf[diffdf[4] != "#NA"]

fig, ax = plt.subplots(dpi = 300)
count, edges, bar = ax.hist(diffdf[7], bins = np.arange(-10, 10, 0.5), align = 'mid',edgecolor='black',facecolor ='grey')
ax.set_xlabel('(data - calculated) arrival (s)')
ax.set_ylabel('Number of Data')
fig.savefig(path+'Arrival difference {} - {}.jpg'.format(daerah,mod),bbox_inches = 'tight')

#filter start
dfhead = df[df[0] == "#"]
dfdata = df[df[0] != "#"]
dfdata = dfdata[dfdata[4] != "#NA"]
dfdata[7] = dfdata[7].astype(float)

#param
z = 6
cleaned = dfdata[(dfdata[7] >= -z) & (dfdata[7] <= z)]

#statistic output
print("==(data-calculated) sebelum seleksi")
print("min : {:.2f} s ".format(dfdata[7].min()))
print("max : {:.2f} s ".format(dfdata[7].max()))
print("median : {:.2f} s ".format(dfdata[7].median()))
print("std : {:.2f} s ".format(dfdata[7].std()))
print("\n")
print("==(data-calculated) setelah seleksi")
print("min : {:.2f} s ".format(cleaned[7].min()))
print("max : {:.2f} s ".format(cleaned[7].max()))
print("median : {:.2f} s ".format(cleaned[7].median()))
print("std : {:.2f} s ".format(cleaned[7].std()))

#apply
cleaned = cleaned.iloc[:,0:4]
result = pd.concat([dfhead,cleaned])
result.sort_index(inplace = True)
result.reset_index(inplace = True, drop = True)

#output result
df2dat(result,evnum = 1,path = path,fname = '{}_output_data_{}_difffilter_{}s.dat'.format(daerah,mod,z))

