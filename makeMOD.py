# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:08:08 2022

@author: UX425IA
"""
# =============================================================================
# membuat File MOD untuk input program
# =============================================================================

import pandas as pd

lon = pd.Series([80,82,85,86.5,88,89.5,91,92.5,94,95.5,97,98.5,100,101.5,103,104.5,106,107.5,109,110])
lat = pd.Series([1,3,5,5.5,7,8.5,10,11.5,13,14.5,16,17.5,19,20.5,22,23.5,25,26.5,28,29.5,31,32.5,35,40])
row4 = pd.Series([-5,0,5,10,20,30,40,60,80,120,165,210,510])
val = pd.Series([5.20,5.57,5.65,5.78,6.25,6.89,7.91,8.30,8.32,8.33,8.34,8.36])
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
  
df.to_csv('D:\BMKG Putu\\Tomography\\150822\\MOD_Indoburma_model3_150822', header = False, index = False, sep = '\t', float_format = '%.3f')