# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 16:09:34 2022

@author: UX425IA
"""
# =============================================================================
# reformat data InaTEWS menjadi data bacaan standar input program
# =============================================================================

import numpy as np
import pandas as pd
from pathlib import Path

#filepath
path = 'D:/BMKG/Tomography/coding/SUMATERA_PHASE_DATA/'
file = ['Phase_2019.txt', 'Phase_2020.txt']

#file output setup, appending in 'output' file
files = open('output', 'a')
idnum = 1

for f in file:
    #open data
    name = f
    pathname = path+name
    data = pd.read_csv(pathname, sep='\t', header = None)

    #index header picker
    headidx = data.loc[data[0].str.contains("bmg",case=False)].index

    for i in data.index:
        if (i in headidx):
            #read header
            a = data.iloc[i,0].split(" ")
            a = [ele for ele in a if ele.strip()]
            b = data.iloc[i,1].split(" ")
            b = [ele for ele in b if ele.strip()]
            region = data.iloc[i,2]
            #pisah tanggal dan waktu
            tbt = a[1].split("-")
            jmd = a[2].split(":")
            #ambil data header
            evid = a[0]
            lon = a[3]
            lat = b[0]
            depth = b[1]
            mag = b[2]
            rms = b[3]
            azgap = b[4]
            
            #convert header
            tempheader = '# '+str(tbt[0])+' '+str(tbt[1])+' '+str(tbt[2])+' '+\
                str(jmd[0])+' '+str(jmd[1])+' '+str(jmd[2])+' '+str(lat)+' '+\
                    str(lon)+' '+str(depth)+' '+str(mag)+' 0 '+'0 '+str(rms)+'0 '+str(idnum)
            idnum = idnum+1
            #input to txt
            files.write(tempheader + '\n')
        else:
            #read data
            c = data.iloc[i,0].split(" ")
            c = [ele for ele in c if ele.strip()]
            sta = c[0]
            ttime = c[4]
            distdeg = c[2]
            azimdeg = c[3]
            phase = c[1]
            
            f = 14 - len(sta) - len(str(ttime))
            #convert data
            tempdata = '     '+str(sta)+' '*f+str(ttime)+'   1.0   '+str(phase)
            #input to txt
            files.write(tempdata + '\n')


files.close()
