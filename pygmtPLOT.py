# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 08:01:50 2022

@author: UX425IA
"""

import pygmt
import pandas as pd
import numpy as np
from localfunction import readabsolute
from pathlib import Path

lat = pd.read_csv("D:/grid5.txt",delim_whitespace=True)
lon = pd.read_csv("D:/grid6.txt",delim_whitespace=True)

#select
lat = lat.lat
lon = lon.lon

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

# #plot palu / sulawesi
# gr = 0.6
# #set longitude
# lon = np.arange(118,128,gr)
# lon = lon - 0.3
# lon = np.append(116, lon)
# lon = np.append(lon, 129)
# #set latitude
# lat = np.arange(-7,4,gr)
# lat=lat-0.3
# lat = np.append(-9, lat)
# lat = np.append(lat, 5)

#lat lon grid dari MOD
# lon = np.array([116.00,118.00,118.50,119.00,119.50,120.00,120.50,121.00,121.50,122.00,122.50,123.00,123.50,124.00,124.50,125.00,125.50,126.00,126.50,127.00,129.00])
# lat = np.array([-9.00,-7.00,-6.50,-6.00,-5.50,-5.00,-4.50,-4.00,-3.50,-3.00,-2.50,-2.00,-1.50,-1.00,-0.50,0.00,0.50,1.00,1.50,2.00,2.50,3.00,5.00])

#plot data gempa
# df = readabsolute('E:\\My Drive\\Tomography\\290622\\event - indoburma-isc-ehb.dat')
# df = df[df[0] == '#']

# buat pasangan lat dan lon
lats,lons = [],[]
for lt in lat.to_list():
  for ln in lon.to_list():
    lats.append(lt)
    lons.append(ln)

#%%
#input grd / nc image
for zz in [0,10,20,30,40,50,60,77,90,100,120,140,180,210]:
  z = f"D:/#BMKG_Local/Tomoplot/sum-real-{zz}km.grd"
  #run
  fig = pygmt.Figure()
  # cpt = pygmt.makecpt(cmap="polar", series=[-10,10,1],reverse=True)
  cpt = "etc/tomo2.cpt"
  region = [92,106,-7,7]
  frame = [f"WSNE+tDepth = {zz} km", "a4f2"]
  fig.basemap(region = region, frame = "f")
  fig.grdimage(z, cmap=cpt)
  fig.coast(region = region,
            frame = frame, 
            shorelines = "1")
  # adition
  fig.plot("etc/trench.gmt", pen = "1", fill = "black", style="f0.5i/0.13i+l+t")
  fig.plot("etc/ridge.gmt", pen = "1,blue")
  fig.plot("etc/pusgen/Indonesia_Confirmed_Thrust.gmt", pen = "1", fill = "black", style="f0.4i/0.08i+l+t")
  fig.plot("etc/pusgen/Indonesia_Inferred_Thrust.gmt", pen = "1,black,-", fill = "black", style="f0.4i/0.08i+l+t")
  fig.plot("etc/pusgen/Indonesia_Confirmed_Fault.gmt", pen = "1")
  fig.plot("etc/pusgen/Indonesia_Inferred_Fault.gmt", pen = "1,-")
  fig.plot("etc/pusgen/Indonesia_Confirmed_Normal.gmt", pen = "1", style="f0.4i/0.05i+l+c")
  fig.plot("etc/pusgen/Indonesia_Inferred_Normal.gmt", pen = "1,-", style="f0.4i/0.05i+l+c")
  fig.plot("etc/pusgen/Indonesia_Confirmed_Fold.gmt", pen = "1", style="f0.4i/0.05i+l+t")

  fig.colorbar(cmap=cpt,frame=["+l dVp","+u \\040"],position="x7.5c/-1.5c+w15.3c/0.45c+jBC+h")
  # fig.plot(x=lons,y=lats, style='+0.2', pen='1,red') 
  #fig.plot(x=df[8].to_list(),y=df[7].to_list(), style='p0.05', color='red')
  # fig.plot(x=[109.487,80.681,80.543,80.702,92.743,109.843,108.921], y = [30.272,6.089,8.397,7.273,11.656,19.029,34.039],style='t0.3', color='red')
  # fig.plot(x=87.3687,y=28.6056, style='c0.3', color = 'blue') 
  fig.savefig("D:/#BMKG_Local/Tomoplot/"+Path(z).stem+"-yosi.png")
# fig.show()
#%%
#save lat dan lon
# np.savetxt('lon',lon,newline=',',fmt='%2.1f')
# np.savetxt('lat',lat,newline=',',fmt='%2.1f')