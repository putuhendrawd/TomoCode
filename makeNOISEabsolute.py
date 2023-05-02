'''
Coding: PYTHON UTF-8
Created On: 2023-05-02 13:04:54
Author: Putu Hendra Widyadharma
=== add random noise to traveltime pha
'''

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from localfunction import *
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt

path = 'G:\\My Drive\\Tomography\\020523\\'
fname = 'phase_sul_2022.dat'
df= readabsolute(path+fname)
mu, sigma = 0, 0.2 # mean and standard deviation

#init tempdata
tempheader = df[df[0]=="#"]
idx=tempheader.index
tempdata = pd.DataFrame([],columns = df.columns)

for a in range (len(idx)):
    #load abs data
    if a == len(idx)-1:
        tempdf = df.iloc[idx[a]+1::]
    else:
        tempdf = df.iloc[idx[a]+1:idx[a+1],:]

    # process make random noise
    s = np.random.normal(mu, sigma, len(tempdf))
    # include
    tempdf[1] = round(tempdf[1].map(np.array)-s,2)
    tempdata = pd.concat([tempdata,tempdf])

dfresult=pd.concat([tempdata,tempheader])
dfresult.sort_index(inplace = True)
dfresult.reset_index(inplace = True, drop = True)

#output
df2dat(dfresult,evnum = 1, path = path, fname=f'noisestdev{str(sigma).replace(".","")}_'+Path(fname).name)
readeventphase(path+f'noisestdev{str(sigma).replace(".","")}_'+Path(fname).name)