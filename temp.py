from localfunction import *
import pandas as pd

path = "D:\\BMKG Putu\\Tomography\\210722\\taupy-sulawesi\\"
fname = 'Sulawesi_output_data_ak135_difffilter_6s_phase8.dat'

df = readabsolute(path+fname)
data = df[df[0] != "#"]
head = df[df[0] == "#"]
print("{} event \n{} fasa".format(len(head),len(data)))