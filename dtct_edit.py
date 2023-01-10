from localfunction import *
import pandas as pd
import numpy as np
import glob
import os

path = "D:/BMKG Files/Tomography/231222/"

files = glob.glob(path+"*")
fname = [os.path.basename(x) for x in files]

#read dt.ct
df1 = pd.read_csv(files[0], delim_whitespace=True, names=[0,1,2,3,4])
df1_head = df1[df1[0] == "#"]
df1_head.drop([3,4], axis=1, inplace=True)
df1_head.columns= ["TAG", "C1", "C2"]
#read hypoDD.res
df2 = pd.read_csv(files[1], delim_whitespace=True, header = 0)
df2.drop("OFFS", axis=1, inplace=True)
df2.columns = ["STA", "DT", "C1", "C2", "IDX", "QUAL", "RES[ms]", "WT", "OFFS"]

#processing
idx = df1_head.index

df1_data = df1.iloc[idx[0]+1:idx[0+1],:]
df1_data.columns = ["STA", "C1", "C2", "WEIGHT", "PHASE"]
