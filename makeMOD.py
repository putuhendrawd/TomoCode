# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:08:08 2022

@author: UX425IA
"""
# =============================================================================
# membuat File MOD untuk input program
# =============================================================================

import pandas as pd

lon = pd.Series([116.0,117.7,118.3,118.9,119.5,120.1,120.7,121.3,121.9,122.5,123.1,123.7,124.3,124.9,125.5,126.1,126.7,127.3,129.0])
lat = pd.Series([-9.0,-7.3,-6.7,-6.1,-5.5,-4.9,-4.3,-3.7,-3.1,-2.5,-1.9,-1.3,-0.7,-0.1,0.5,1.1,1.7,2.3,2.9,3.5,5.0])
row4 = pd.Series([-5.0,0.0,10.0,20.0,40.0,50.0,60.0,70.0,90.0,120.0,140.0,165.0,210.0,360.0,510.0])
val = pd.Series([5.57,5.78,6.89,8.3,8.32,8.33,8.34,8.36,8.45,8.67,8.91,9.5,9.76,10.06,10.91])
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
  
df.to_csv('E:\\My Drive\\Tomography\\190722\\Velest33-indoburma-bandung\\MOD_Indoburma_190722', header = False, index = False, sep = '\t', float_format = '%.3f')