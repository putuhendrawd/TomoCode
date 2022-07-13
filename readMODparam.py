import pandas as pd
import numpy as np
from pathlib import Path

path = 'E:\\My Drive\\Tomography\\130722\\' 
filemod = path+'MOD-indoburma'

#auto column count ==================================================
largest_column_count = 0
with open(filemod, 'r') as temp_f:
    # Read the lines
    lines = temp_f.readlines()

    for l in lines:
        # Count the column count for the current line
        column_count = len(l.split('\t')) + 1
        
        # Set the new most column count
        largest_column_count = column_count if largest_column_count < column_count else largest_column_count

# Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
column_names = [i for i in range(0, largest_column_count)]
# ====================================================================

dfmod = pd.read_csv(filemod,delim_whitespace=True,names=column_names, header=None)

x = float(dfmod.iloc[0][2])
y = (dfmod.iloc[0][3])
velo = [dfmod.iloc[4,0]]
for i in range(5,int(x*y)):
    if (i+x)%x == 0:
        velo.append(dfmod.iloc[int(i+x),0])
velo = pd.Series(velo)

lon = dfmod.iloc[1,:]
lat = dfmod.iloc[2,:]
depth = dfmod.iloc[3,:]

res = [lon,lat,depth,velo]

dfres = pd.DataFrame(res, index=['lon','lat','depth','vp'])
dfres.to_csv(path+"MODparam.txt",header=None)