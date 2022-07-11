import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from localfunction import *


path = "D:\\BMKG Putu\\Tomography\\050722\\"
inname = "sta-usul-2-filter.txt"

fin = open(path+inname)
baris = fin.readlines()
for i in range(len(baris)):
    baris[i] = baris[i].split()

#format
for i in range(len(baris)):
    #format lat
    if float(baris[i][1]) >= 0:
        baris[i][1] = "{:.4f}N".format(float(baris[i][1]))
    else:
        baris[i][1] ="{:.4f}S".format(abs(float(baris[i][1])))
    #format lon
    if float(baris[i][2]) >= 0:
        baris[i][2] ="{:.4f}E".format(float(baris[i][2]))
    else:
        baris[i][2] ="{:.4f}W".format(abs(float(baris[i][2])))
    #format staname > 4
    if len(baris[i][0]) > 4 :
        baris[i][0] = baris[i][0][:4]
    #format altitude
    baris[i][3] = "{:0>4}".format(round(float(baris[i][3])))

#output
fout = open(path+'output_'+inname, 'w')
fout.write("(a4,f7.4,a1,1x,f8.4,a1,1x,i5,1x,i1,1x,i3,1x,f5.2,2x,f5.2)\n")
for z in range(len(baris)):
    fout.write("{0: >4}{1: >8}{2: >10}{3: >6}{4: ^3}{5:0>3}{6: >6}{7: >7}{8: >4}\n".format(baris[z][0],baris[z][1],baris[z][2]\
        ,baris[z][3], "1",z+1,"0.00","0.00","1"))
fout.close()