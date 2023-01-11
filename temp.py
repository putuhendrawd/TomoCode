from localfunction import *
import pandas as pd

path = "E:/My Drive/Tomography/100123/reloc-isc-ehb-indoburma-10012023/"
fname = 'tomoDD.res'

df=readres(path+fname)

df = readabsolute(path+fname)
data = df[df[0] != "#"]
head = df[df[0] == "#"]
print("{} event \n{} fasa".format(len(head),len(data)))

df2dat(df,evnum = 1, path = path, fname = "test.dat")