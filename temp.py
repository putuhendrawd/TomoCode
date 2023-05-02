import numpy as np
import pandas as pd
import geopy.distance as gd
import matplotlib.pyplot as plt
from pathlib import Path
from localfunction import *
pd.options.mode.chained_assignment = None

for nn in [3,4,5,6,7]:
    # =============================================================================
    # Filter Absolute based on
    # selected station, phase, total station report, event rms value, magnitude value
    # =============================================================================

    path = 'G:\\My Drive\\Tomography\\300423\\'
    fname = f'phase_sul_2022_8P_wadatifilter_sta-rms{nn}.dat'
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
        # if (len(tempdf) >= 8): #isi batas jumlah laporan untuk semua jenis fasa
        if (len(tempdf[tempdf[3] == 'P']) >= 8): #isi batas jumlah laporan hanya P yang dihitung
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
    df2dat(df,evnum = 1, path = path, fname=Path(fname).stem+'_8P.dat')
    print("== data filter")
    readeventphase(path+Path(fname).stem+'_8P.dat')