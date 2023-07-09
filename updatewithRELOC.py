'''
Coding: PYTHON UTF-8
Created On: 2023-05-02 14:53:08
Author: Putu Hendra Widyadharma
=== update pha with .reloc parameter
=== .reloc file should have same event id with .pha
'''

import numpy as np
import pandas as pd
from localfunction import *
from tqdm import trange


path="G:\\My Drive\\Tomography\\230623\\reloc_update_with_final_real\\"
fname= "phase_sul_2022_8P_wadatifilter_sta-rms5.dat"
relocname = "tomoDD.reloc"
df=readabsolute(path+fname)
relocdf = pd.read_csv(path+relocname, delim_whitespace=True, index_col=False, header=None,\
    names="ID, LAT, LON, DEPTH, X, Y, Z, EX, EY, EZ, YR, MO, DY, HR, MI, SC, MAG, NCCP, NCTP, NCTS, RCC, RCT, CID, UNKNOWN".replace(" ","").split(","))

# iterables
idx = df[df[0]=="#"].index
tempdata = pd.DataFrame([],columns = df.columns)
i=0

for iter in range(len(idx)):
    #grab data
    if iter == len(idx)-1: # last iteration 
        tempdf = df.iloc[idx[iter]::]
        if int(tempdf.iloc[0,14]) in (relocdf['ID'].astype(int).to_list()):
            temp = relocdf[relocdf['ID'] == int(tempdf.iloc[0,14])]
            # print(f"(last iter) event id --> {tempdf.iloc[0,14]} in reloc")
        else:
            print(f"(last iter) event id --> {tempdf.iloc[0,14]} !!! not in reloc")
            continue
    else: # iter 1 - (n-1)
        tempdf = df.iloc[idx[iter]:idx[iter+1]]
        if int(tempdf.iloc[0,14]) in (relocdf['ID'].astype(int).to_list()):
            temp = relocdf[relocdf['ID'] == int(tempdf.iloc[0,14])]
            # print(f"event id --> {tempdf.iloc[0,14]} in reloc")
        else:
            print(f"event id --> {tempdf.iloc[0,14]} !!! not in reloc")
            continue
    
    #process the data
    #ubah header
    tempdf.iloc[0,1] = temp['YR'].values[0] #year
    tempdf.iloc[0,2] = temp['MO'].values[0] #month
    tempdf.iloc[0,3] = temp['DY'].values[0] #day
    tempdf.iloc[0,4] = temp['HR'].values[0] #hour
    tempdf.iloc[0,5] = temp['MI'].values[0] #minute
    tempdf.iloc[0,6] = temp['SC'].values[0] #second,msec
    tempdf.iloc[0,7] = temp['LAT'].values[0] #lat
    tempdf.iloc[0,8] = temp['LON'].values[0] #lon
    tempdf.iloc[0,9] = temp['DEPTH'].values[0] #depth
    # tempdf.iloc[0,10]= temp['MAG'].values[0] #mag
    
    #gabungkan data
    tempdata=pd.concat([tempdata,tempdf])
    i+=1

# reset and sort index
tempdata.sort_index(inplace = True)
tempdata.reset_index(inplace = True, drop = True)

#output df
df2dat(tempdata,evnum = 1, path = path, fname=f"relocupdate_"+Path(fname).name)
print(f"total iter = {i}")
readeventphase(path+f"relocupdate_"+Path(fname).name)
