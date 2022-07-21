# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:08:08 2022

@author: UX425IA
"""
# =============================================================================
# membuat File MOD untuk input program
# =============================================================================

import pandas as pd

lon = pd.Series([80.000,82.000,85.000,86.300,87.600,88.900,90.200,91.500,92.800,94.100,95.400,96.700,98.000,99.300,100.600,101.900,103.200,104.500,105.800,107.100,108.000,110.000])
lat = pd.Series([1.000,3.000,5.000,7.000,8.300,9.600,10.900,12.200,13.500,14.800,16.100,17.400,18.700,20.000,21.300,22.600,23.900,25.200,26.500,27.800,29.100,30.400,32.000,35.000,40.000])
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