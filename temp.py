# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 20:46:12 2022

@author: UX425IA
"""
# =============================================================================
# reformat data dari ISC ke bentuk data bacaan hypodd
# =============================================================================
from email import header
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from localfunction import *

# =============================================================================
# reading and cleaning data
# =============================================================================
path = 'D:\\BMKG Putu\\Tomography\\290622\\indoburma-isc-ehb\\'
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

#filter
#data = data[abs(data['RES']) < 3.25 ]

#plot histogram
fig, ax = plt.subplots(dpi = 1200)
ax.hist(data["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', edgecolor='black',facecolor ='grey')
ax.set_xlim([-6.5,6.5])
ax.set_ylim([0,10000])
ax.set_xlabel('RMS (s)')
ax.set_xticks(np.arange(-8,9,1))
ax.set_ylabel('Counts')
# ax.set_title('RMS {} {}'.format(a,b),y=1.03)
fig.savefig('RMS Histogram.jpg', bbox_inches = 'tight')

print("data length : {}".format(len(data)))
print("total event : {}".format(len(data['EVENTID'].unique())))

#test edit branch
#test edit branch with new account