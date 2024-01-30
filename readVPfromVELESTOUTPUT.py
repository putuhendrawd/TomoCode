'''
Coding: PYTHON UTF-8
Created On: 2022-07-13 21:29:05
Author: Putu Hendra Widyadharma
=== reading velest output .OUT || need input depth and initial vp from velocity model .mod
'''
import pandas as pd
from pathlib import Path
from localfunction import *

path = "G:\\My Drive\\Tomography\\170823\\velest-indoburma-16082023\\"
input_path = "output\\"
fname = "model_indoburma_160823.OUT"


depth = []
initial = []

fin = open(path+fname)
#skip row 1 and 2
readl = fin.readlines()
#read
for i in range(len(readl)):
    spl = readl[i].split()
    try:
        depth.append(spl[1])
        initial.append(spl[0])
    except:
        continue
fin.close()

depth = depth[2::]
initial = initial[2::]
depth = [float(i) for i in depth]
initial = [float(i) for i in initial]

#initial dataframe to store result
result = pd.DataFrame([],columns=["depth","init"])
result["depth"] = depth
result['init'] = initial
result.set_index("depth",inplace=True)
start = False

#start
fin = open(path+input_path+fname)
readl = fin.readlines()
for i in range(len(readl)):
    spl = readl[i].split()
    
    if len(spl) == 3 and spl[0] == "ITERATION":
        start = True
    
    if len(spl) == 3 and spl[0] == "ITERATION" and start:
        iter = spl[2]
    try:
        if len(spl) == 3 and (float(spl[2]) in depth) and start:
            result.loc[float(spl[2]),iter] = spl[0]
    except:
        continue
    
    if len(spl) == 12 and spl[0] == "nlay":
        start = 2
        iter = 'updated'
    
    try:   
        if (float(spl[1].split('.')[0]) in depth) and start == 2:
            if len(readl[i].split()) == 13:
                result.loc[float(spl[1].split('.')[0]),iter] = spl[4]
            else: 
                result.loc[float(spl[1].split('.')[0]),iter] = spl[3]
    except:
        continue
    
#export
result.to_csv(path+f'{input_path}convert/{Path(fname).stem}_vp_extract.txt',index="depth")
#export transpose
tresult = result.transpose()
tresult.to_csv(path+f'{input_path}convert/{Path(fname).stem}_vp_extract_transpose.txt')