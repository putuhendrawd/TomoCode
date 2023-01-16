from localfunction import *
import pandas as pd

path = "E:/My Drive/Tomography/100123/reloc-isc-ehb-indoburma-10012023/"
fname = 'phase-indoburma-3-fixed_filter5sta_plusehb_filter_sta_rms.dat'

readeventphase(path+fname)
# df = readabsolute(path+fname)
# data = df[df[0] != "#"]
# head = df[df[0] == "#"]
# print(f"{len(head): <6} Event \n{len(data): <6} Phase")
# for i in data[3].unique():
#     x = data[data[3] == i]
#     print(f"--{i: <3}: {len(x): >6}")

# df2dat(df,evnum = 1, path = path, fname = "test.dat")