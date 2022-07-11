# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:08:08 2022

@author: UX425IA
"""
# =============================================================================
# membuat File MOD untuk input program
# =============================================================================

import pandas as pd

lon = pd.Series([80,82,85,86.3,87.6,88.9,90.2,91.5,92.8,94.1,95.4,96.7,98,99.3,100.6,101.9,103.2,104.5,105.8,107.1,108,110])
lat = pd.Series([1,3,5,7,8.3,9.6,10.9,12.2,13.5,14.8,16.1,17.4,18.7,20,21.3,22.6,23.9,25.2,26.5,27.8,29.1,30.4,32,35,40])
row4 = pd.Series([-5,0,5,10,15,20,30,40,50,60,77,90,100,120,140,180,210,510])
val = pd.Series([5.25,5.68,6.69,6.69,6.72,6.72,7.42,7.59,7.65,7.79,7.93,7.96,8.02,8.12,8.17,8.33,8.33,9.03])
temp = []
temp2 = []
numlat = len(lat)
numlon = len(lon)
numval = len(val)
df = pd.DataFrame()
header = pd.Series([0.1, numlon, numlat, numval])

#input output data
df = df.append(header, ignore_index=True)
df = df.append(lon, ignore_index=True)
df = df.append(lat, ignore_index=True)
df = df.append(row4, ignore_index=True)

for c,v in enumerate(val):
    for x in range (numlat):
        for y in range (numlon):
            temp.append(val[c])
        tempseries = pd.Series(temp)
        df = df.append(tempseries, ignore_index=True)
        temp = []
    
for x in range (len(df.index)-4):
    for y in range (numlon):
        temp2.append(1.77) #data angka dari wadati diagram
    temp2series = pd.Series(temp2)
    df = df.append(temp2series, ignore_index=True)
    temp2 = []
  
df.to_csv('MOD_Indoburma_sum_3', header = False, index = False, sep = '\t', float_format = '%.3f')