import pandas as pd
from localfunction import *

path = "E:\\My Drive\\Tomography\\130722\\Velest33-indoburma\\"
fname = "VELEST_OUT.OUT"

fin = open(path+fname)
readl = fin.readlines()

depth = [-5.0,0.0,10.0,20.0,40.0,50.0,60.0,70.0,90.0,120.0,140.0,165.0,210.0,360.0,510.0]
result = []
start = False

for i in range(len(readl)):
    spl = readl[i].split()
    
    if len(spl) == 3 and spl[0] == "ITERATION":
        start = True
    
    if len(spl) == 3 and spl[0] == "ITERATION" and start:
        result.append([spl[0],spl[2]])
    try:
        if len(spl) == 3 and (float(spl[2]) in depth) and start:
            result.append([spl[2],spl[0]])
    except:
        continue
    
    if len(spl) == 12 and spl[0] == "nlay":
        start = 2
        result.append(["LAST","RESULT"])
    
    try:   
        if (float(spl[1].split('.')[0]) in depth) and start == 2:
            if len(readl[i].split()) == 13:
                result.append([spl[1].split('.')[0],spl[4]])
            else: 
                result.append([spl[1].split('.')[0],spl[3]])
    except:
        continue
    
#export

dfresult = pd.DataFrame(result)
dfresult.to_csv(path+'vp_extract.txt',header=False,index=False)