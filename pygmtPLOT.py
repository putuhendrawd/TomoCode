# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 08:01:50 2022

@author: UX425IA
"""

import pygmt
import pandas as pd
import numpy as np
from localfunction import readabsolute

#plot sumatera
#gr = 0.5
#set longitude
# lon = np.arange(92,106.5,gr)
# lon = np.append(min(lon)-2, lon)
# lon = np.append(lon, max(lon)+2)
# #set latitude
# lat = np.arange(-7,7.5,gr)
# lat = np.append(min(lat)-2, lat)
# lat = np.append(lat, max(lat)+2)

#plot himalaya / indoburma
# gr = 0.6
# #set longitude
# lon = np.linspace(91.5,98.2,gr)
# lon = np.append([84,87,89],lon)
# lon = np.append(lon, [100,102,105])
# #set latitude
# lat = np.linspace(18.5,28.2,gr)
# lat = np.append([12,15,16.5],lat)
# lat = np.append(lat, [29.5,31,34])

#lat lon grid dari MOD
lon = np.array([80,82,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,108,110])
lat = np.array([1,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,40])

#plot data gempa
df = readabsolute('E:\\My Drive\\Tomography\\290622\\event - indoburma-isc-ehb.dat')
df = df[df[0] == '#']

#buat pasangan lat dan lon
lats,lons = [],[]
for lt in lat:
  for ln in lon:
    lats.append(lt)
    lons.append(ln)

fig = pygmt.Figure()
fig.coast(region = [min(lon)-10,max(lon)+10,min(lat)-10,max(lat)+10],
          frame = ["WSNE", "a"], 
          shorelines = "0.5")
fig.plot(x=lons,y=lats, style='+0.1') 
fig.plot(x=df[8].to_list(),y=df[7].to_list(), style='p0.05', color='red')
# fig.plot(x=[109.487,80.681,80.543,80.702,92.743,109.843,108.921], y = [30.272,6.089,8.397,7.273,11.656,19.029,34.039],style='t0.3', color='red')
# fig.plot(x=87.3687,y=28.6056, style='c0.3', color = 'blue') 
fig.savefig("output.png")

#save lat dan lon
# np.savetxt('lon',lon,newline=',',fmt='%2.1f')
# np.savetxt('lat',lat,newline=',',fmt='%2.1f')