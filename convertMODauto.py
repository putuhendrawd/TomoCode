# =============================================================================
# convert data agar dapat di plot dalam bentuk xyz
# =============================================================================

import pandas as pd
import numpy as np
import os
from pathlib import Path

print("Running Converter")
# folder path
path = os.getcwd() + '\\'
# 1: vpvsdwpdws 0: vpvs
vdws = int(input("Select Mode [0:vpvs | 1:all] = "))

# =============================================================================
filemod = path+'MOD' #deklarasi file MOD
n = 1 #grid yang dipotong || tidak bisa n = 0 / tidak dipotong

#auto column count ==================================================
largest_column_count = 0
with open(filemod, 'r') as temp_f:
    # Read the lines
    lines = temp_f.readlines()

    for l in lines:
        # Count the column count for the current line
        column_count = len(l.split('\t')) + 1
        
        # Set the new most column count
        largest_column_count = column_count if largest_column_count < column_count else largest_column_count

# Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
column_names = [i for i in range(0, largest_column_count)]
# ====================================================================

dfmod = pd.read_csv(filemod,delim_whitespace=True,nrows=3, skiprows= 1,names=column_names, header=None) #file MOD hanya baca 3 baris pertama
lon = dfmod.iloc[0].to_numpy() #ambil baris pertama sebagai longitude
lon = lon[~np.isnan(lon)][n:-n] # buang data pertama dan akhir longitude
lat = dfmod.iloc[1].to_numpy()
lat = lat[~np.isnan(lat)][n:-n]
lvl = dfmod.iloc[2].to_numpy() #ambil levelnya
lvl = lvl[~np.isnan(lvl)]
nbaris = len(lat) + (2*n) #jumlah kelipatan baris tanpa dipotong

# print('==lat ',len(lat),lat)
# print('==lon ',len(lon),lon)
# print('==lvl ',len(lvl),lvl)
# print('nbaris',nbaris)

#Membuat data silang latitude-longitude
lats,lons = [],[]
for lt in lat:
  for ln in lon:
    #print(lt,ln)
    lats.append(lt)
    lons.append(ln)
    #print(lt,ln)
# print('==lats ',len(lats),lats)

#=================================================================================================
for x in ['p','s']:
    filevp= path+'V{}_model.dat'.format(x) #deklarasi file VP

    #mengambil level yang akan digunakan
    dflvl = np.loadtxt(filevp,usecols=(0)) #hanya kolom pertama

    datavp = np.loadtxt(filevp)
    datafix = []
    for i in range(len(lvl)):

        #edit code untuk n grid
        data = (datavp[nbaris*i+n:nbaris*(i+1)-n,n:-n]) #pilih data perlapisan
        #-----
        #data =np.flip(data) #membalik data
        data = data.ravel() #memflatkan data

        #edit code untuk n grid
        ikat = dflvl[i*nbaris+n] # buat ikatan
        #-----
        
        data = ((data-ikat)/ikat)*100 #formula dari pak Supri
        data = data.tolist() #ubah array ke list
        datafix.append(data)
        
    df = pd.DataFrame(datafix) #membaca data dalam format dataframe pandas
    df = df.transpose()
    df = df.set_axis(lvl, axis='columns') #beri nama columns dengan lvl 0, 0.5, ..
    df.drop(df.columns[[0,-1]], axis=1, inplace=True) #hapus data pada level awal dan akhir
    #print('panjang lats',len(lats))
    df.insert(0,'Lat', lats) #menyisipkan lats pada kolom pertama
    df.insert(1,'Lon', lons)

    #simpan hasil dalam format csv
    filename = path+Path(filevp).stem +'_output.csv'
    df.to_csv (filename, index = False, header=True)

#=================================================================================================
if vdws == 1:
    for x in ['P','S']:
        filevp= path+'DWS_{}'.format(x) #deklarasi file VP

        #mengambil level yang akan digunakan
        dflvl = np.loadtxt(filevp,usecols=(0)) #hanya kolom pertama

        datavp = np.loadtxt(filevp)
        datafix = []
        for i in range(len(lvl)):

            #edit code untuk n grid
            data = (datavp[nbaris*i+n:nbaris*(i+1)-n,n:-n]) #pilih data perlapisan
            #----- 

            #data =np.flip(data) #membalik data
            data = data.ravel() #memflatkan data

            #edit code untuk n grid
            #ikat = dflvl[i*nbaris+n] # buat ikatan
            #-----
            
            #data = ((data-ikat)/ikat)*100 #formula dari pak Supri
            data = data.tolist() #ubah array ke list
            datafix.append(data)
            
        df = pd.DataFrame(datafix) #membaca data dalam format dataframe pandas
        df = df.transpose()
        df = df.set_axis(lvl, axis='columns') #beri nama columns dengan lvl 0, 0.5, ..
        df.drop(df.columns[[0,-1]], axis=1, inplace=True) #hapus data pada level awal dan akhir
        #print('panjang lats',len(lats))
        df.insert(0,'Lat', lats) #menyisipkan lats pada kolom pertama
        df.insert(1,'Lon', lons)

        #simpan hasil dalam format csv
        filename = path+Path(filevp).stem +'_output.csv'
        df.to_csv (filename, index = False, header=True)

print("Convert Finish")