from localfunction import *
import pandas as pd

path = "E:/My Drive/Tomography/100123/reloc-isc-ehb-indoburma-10012023/"
fname = 'phase-indoburma-3-fixed_filter5sta_plusehb_filter_sta_rms.dat'

readeventphase(path+fname)
df = readabsolute(path+fname)
data = df[df[0] != "#"]
head = df[df[0] == "#"]
P_phase = data[data[3] == "P"]
S_phase = data[data[3] != "P"]
print(f"{len(head): <6} Event \n{len(data): <6} Phase\n---P: {len(P_phase): >6}\n---S: {len(S_phase): >6}")

# df2dat(df,evnum = 1, path = path, fname = "test.dat")