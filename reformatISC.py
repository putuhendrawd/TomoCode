# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 20:46:12 2022

@author: UX425IA
"""
# =============================================================================
# reformat data dari ISC ke bentuk data bacaan hypodd
# =============================================================================
import numpy as np
import pandas as pd
import datetime as dt
from localfunction import *

# =============================================================================
# reading and cleaning data
# =============================================================================
path = 'D:\\BMKG Putu\\Tomography\\290622\\indoburma-isc-ehb\\'
outputpath = 'D:\\BMKG Putu\\Tomography\\070722\\'
fname = 'indoburma-isc-ehb-1964-2020.txt'

data = pd.read_csv(path+fname, skiprows=[0], low_memory=False)
#change name column num 25
data.rename(columns = {'TYPE  ':'TYPE.MAG'}, inplace=True)
#space remover columns
data.columns = data.columns.str.replace(' ','')
#replace empty data represented with whitespace data with nan
data = data.replace(r'^\s*$', np.nan, regex=True)

#space remover in object-type columns
for i in data.columns:
    if data[i].dtypes == object:
        data[i] = data[i].str.strip()
    else:
        pass

#remove nan magnitude data
data = data[data['MAG'].notna()]

# =============================================================================
# reformat data
# =============================================================================

z = 1
files = open(outputpath+'convert_'+fname, 'w')
for i in data['EVENTID'].unique():
    df = data[data['EVENTID'] == i].reset_index(drop=True)
   
    #search for station with more than 1 report
    s2 = df['STA'].value_counts().loc[lambda x: x>1].index
    #search station with reporter == nan
    repna = df[df['REPORTER'].isna()].index
    
    #selection level 1: delete reports from same station that has no reporter
    if len(repna) != len(df): #if all data reporter == nan then skip
        for k in range (0, len(df.index)):
            if (df['STA'][k] in s2) & (k in repna):
                df.drop(k, axis = 0, inplace = True)
        
    #selection level 2: select first report if there is more than 1 report with reporter in the same station #correction for different phase
    df = df.drop_duplicates(subset=['STA','PHASE'], keep="first")
    
    #reset dataframe index
    df.reset_index(inplace = True)
    
    # RMS 
    rms = df["RES"].mean()

    #origin time
    origintime = pass_datetime(str(df['DATE.1'][0] + ' ' +df['TIME.1'][0]))
    
    #make header
    tempheader = '#\t' + str(origintime.year) + '\t' + str(origintime.month) + '\t' + str(origintime.day) + \
        '\t' + str(origintime.hour) + '\t' + str(origintime.minute) + '\t' + str(origintime.strftime('%S.%f')[:-4]) + '\t' + \
            str(df['LAT.1'][0]) + '\t' + str(df['LON.1'][0]) + '\t' + str(df['DEPTH'][0]) + '\t' + str(df['MAG'][0]) + \
                '\t' + str('0.0') + '\t' + str('0.0') + '\t' + str(round(rms,1)) + '\t' + str(z) + '\n'
    files.write(tempheader)
    
    #make data 
    for j in range (0, len(df.index)):
        ttime1 = pass_datetime(str(df['DATE'][j] + ' ' +df['TIME'][j]))
        traveltime = (ttime1-origintime).total_seconds()
        tempdata = '\t' + str(df['STA'][j]) + '\t' + str(traveltime) + '\t' + '1.0' + '\t' + str(df['PHASE'][j]) + '\t\t\t\t\t\t\t\t\t\t' +'\n'
        files.write(tempdata)
    
    #event number interation
    z = z+1
files.close()