'''
Coding: PYTHON UTF-8
Created On: 2023-05-02 13:04:54
Author: Putu Hendra Widyadharma
=== add random noise to traveltime pha
'''

import numpy as np
import pandas as pd
from localfunction import *
pd.options.mode.chained_assignment = None

path = 'G:\\My Drive\\Tomography\\020623\\Syn-output-CRT2-sul-ModVel25052023-WdtFltrDamp100-28052023\\'
fname = 'syn.absolute.dat'
df = readabsolute(path+fname)
mu, sigma = 0, 0.25 # mean and standard deviation (max = 2* std dev)

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
df2dat(dfresult,evnum = 1, absolute=True, path = path, fname=f'noisestdev{str(sigma).replace(".","")}_'+Path(fname).name)