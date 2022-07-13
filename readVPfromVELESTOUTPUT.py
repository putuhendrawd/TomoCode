'''
Coding: PYTHON UTF-8
Created On: 2022-07-13 21:29:05
Author: Putu Hendra Widyadharma
=== reading velest output .OUT || need input depth and initial vp from readMODparam function
'''
import pandas as pd
from localfunction import *

path = "E:\\My Drive\\Tomography\\130722\\Velest33-indoburma\\"
fname = "VELEST_OUT.OUT"

#input parameter
fin = open(path+'inputreformat\\MODparam.txt')
readl = fin.readlines()
#depth
depth = readl[2].split(",")
depth = ' '.join(depth).split()
depth = depth[1::]
depth = [float(i) for i in depth]
#initial vp
initial = readl[3].split(",")
initial = ' '.join(initial).split()
initial = initial[1::]
initial = [float(i) for i in initial]
fin.close()

#initial dataframe to store result
result = pd.DataFrame([],columns=["depth","init"])
result["depth"] = depth
result['init'] = initial
result.set_index("depth",inplace=True)
start = False

#start
fin = open(path+fname)
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
        if (float(spl[1].split('.')[0]) in depth) and start == 'updated':
            if len(readl[i].split()) == 13:
                result.loc[float(spl[1].split('.')[0]),iter] = spl[4]
            else: 
                result.loc[float(spl[1].split('.')[0]),iter] = spl[3]
    except:
        continue
    
#export
result.to_csv(path+'\\output\\vp_extract.txt',index="depth")