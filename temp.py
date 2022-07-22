from localfunction import *
import pandas as pd

path = "D:\\BMKG Putu\\Tomography\\210722\\taupy-sulawesi\\"
fname = 'phase-sulawesi.dat'

df = readabsolute(path+fname)
data = df[df[0] != "#"]
head = df[df[0] == "#"]
print("{} event \n{} fasa".format(len(head),len(data)))

df2dat(df,evnum = 1, path = path, fname = "test.dat")