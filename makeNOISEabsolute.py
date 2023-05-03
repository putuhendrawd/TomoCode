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

path = 'G:\\My Drive\\Tomography\\030523\\'
fname = 'syn.absolute.dat'
df= readabsolute(path+fname)
mu, sigma = 0, 0.1 # mean and standard deviation

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
    tempdf[1] = tempdf[1].map(np.array)-s
    tempdata = pd.concat([tempdata,tempdf])

dfresult=pd.concat([tempdata,tempheader])
dfresult.sort_index(inplace = True)
dfresult.reset_index(inplace = True, drop = True)

#output
df2dat(dfresult,evnum = 1, path = path, fname=f'noisestdev{str(sigma).replace(".","")}_'+Path(fname).name)
readeventphase(path+f'noisestdev{str(sigma).replace(".","")}_'+Path(fname).name)

#if running in absolute.dat
dfresult.loc[:,:3].to_csv(path+f'noisestdev{str(sigma).replace(".","")}_'+Path(fname).name, sep="\t",index=None, header=None)
'''
if running in absolute.dat, there is a bug and it need to fix by using:
replace "\t\t" char with none
replace "\t" with "  " (double space)
'''