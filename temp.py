from localfunction import *
import pandas as pd

path = "E:\\My Drive\\Tomography\\190722\\TaupyRUN\\"
fname = "output_data_ak135.csv"

fin = open(path+fname)
baris = fin.readlines()

x = []

for i in range(len(baris)):
    x.append(baris[i].split(","))

#delete 
x = x[1::]
[j.pop(0) for j in x]

df = pd.DataFrame(x)
dfhead = df[df[0] == "#"]
dfdata = df[df[0] != "#"]

dfdata[7] = dfdata[7].astype(float)

cleaned = dfdata[dfdata[7] >= -6]
cleaned = dfdata[dfdata[7] <= 6]
cleaned = cleaned.iloc[:,0:4]

result = pd.concat([dfhead,cleaned])
result.sort_index(inplace = True)
result.reset_index(inplace = True, drop = True)

# df2dat(result,evnum = 0,path = path,fname = 'filter_output_data_ak135.dat')

a = readabsolute("E:\\My Drive\\Tomography\\190722\\TaupyRUN\\phase-indoburma-3-fixed-plus-filter510-rms3.dat")