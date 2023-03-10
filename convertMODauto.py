# =============================================================================
# convert data agar dapat di plot dalam bentuk xyz
# =============================================================================

import pandas as pd
import numpy as np
import os
from pathlib import Path
import sys

# folder path
path = os.getcwd() + '\\'
# path = "G:\\My Drive\\Tomography\\Shared Hasil\\Sulawesi\\input_data\\early-res-sul5-fix-2019\\real-inversi\\"
# 1: vpvsdwpdws 0: vpvs
print("running converter")
vdws = int(input("input mode [ 0: vpvs | 1: all ] = "))

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
    try:
        filevp= path+'V{}_model.dat'.format(x) #deklarasi file VP

        #mengambil level yang akan digunakan
        dflvl = np.loadtxt(filevp,usecols=(0)) #hanya kolom pertama

        datavp = np.loadtxt(filevp)
        datafix = []
        datavpvsfix = []
        for i in range(len(lvl)):

            #edit code untuk n grid
            data = (datavp[nbaris*i+n:nbaris*(i+1)-n,n:-n]) #pilih data perlapisan
            #-----
            #data =np.flip(data) #membalik data
            data = data.ravel() #memflatkan data
            datavpvs = data.ravel() # pengolahan vpvs
            #edit code untuk n grid
            ikat = dflvl[i*nbaris+n] # buat ikatan
            #-----
            
            data = ((data-ikat)/ikat)*100 #formula dari pak Supri
            data = data.tolist() #ubah array ke list
            datavpvs = datavpvs.tolist() # pengolahan vpvs
            datafix.append(data)
            datavpvsfix.append(datavpvs) # pengolahan vpvs
            
        df = pd.DataFrame(datafix) #membaca data dalam format dataframe pandas
        df = df.transpose()
        df = df.set_axis(lvl, axis='columns') #beri nama columns dengan lvl 0, 0.5, ..
        df.drop(df.columns[[0,-1]], axis=1, inplace=True) #hapus data pada level awal dan akhir
        #print('panjang lats',len(lats))
        df.insert(0,'Lat', lats) #menyisipkan lats pada kolom pertama
        df.insert(1,'Lon', lons)

        # pengolahan vpvs
        dfvpvs = pd.DataFrame(datavpvsfix) #membaca data dalam format dataframe pandas
        dfvpvs = dfvpvs.transpose()
        dfvpvs = dfvpvs.set_axis(lvl, axis='columns') #beri nama columns dengan lvl 0, 0.5, ..
        dfvpvs.drop(dfvpvs.columns[[0,-1]], axis=1, inplace=True) #hapus data pada level awal dan akhir
        #print('panjang lats',len(lats))
        dfvpvs.insert(0,'Lat', lats) #menyisipkan lats pada kolom pertama
        dfvpvs.insert(1,'Lon', lons)

        #simpan hasil dalam format csv
        filename = path+Path(filevp).stem +'_output.csv'
        if x == 'p':
            dfp = dfvpvs
        else:
            dfs = dfvpvs
        df.to_csv (filename, index = False, header=True)
    except:
        print('V{}_model.dat running error'.format(x))
try:
    dfvs = pd.DataFrame([],columns=dfp.columns)
    dfvs['Lat'] = lats
    dfvs['Lon'] = lons
    for z in dfp.columns:
        if z == 'Lat' or z == 'Lon':
            pass
        else:
            dfvs[z] = dfp[z] / dfs[z]
    dfvs.replace([np.inf, -np.inf], np.nan, inplace=True)
    dfvs.to_csv(path+'VpperVs_model_output.csv', index = False, header=True, na_rep='NaN')
except:
    print('VpperVs_model_output.csv cannot be created')
#=================================================================================================
if vdws == 1:
    try:
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
    except:
        print('DWS_{} running error'.format(x))
        
print("converter finish")