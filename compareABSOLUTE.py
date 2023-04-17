import numpy as np
import pandas as pd
from pathlib import Path
import datetime as dt
from localfunction import *
import os

ti = dt.datetime.now()

###############################################################
# file input                                                  #
# data di f1 akan dihapus jika ada event yang sama dengan f2  #
###############################################################
path = 'G:\\My Drive\\Tomography\\050423\\'
#file compare 1
f1 = 'phase_sul5.dat'
#file compare 2
f2 = 'phase_sul5.dat'
#output filename
outputname = "compare_"+f1.split('.')[0] #without extension

#read file
df1 = readabsolute(path+f1)
df2 = readabsolute(path+f2)

#index of header
tempidx1 = df1[df1[0] == '#'].index
tempidx2 = df2[df2[0] == '#'].index

#buat list date
tempdate1 = []
templat1 = []
templon1 = []
tempdate2 = []
templat2 = []
templon2 = []

#ambil data tanggal dan jam
for i in tempidx1:
    x = "{:.0f}-{:.0f}-{:.0f} {:.0f}-{:.0f}-{:.2f}".format(int(df1.loc[i][1]),int(df1.loc[i][2]),\
        int(df1.loc[i][3]),int(df1.loc[i][4]),int(df1.loc[i][5]),\
            float(df1.loc[i][6]))
    tempdate1.append(pass_datetime(x))
    templat1.append(float(df1.loc[i][7]))
    templon1.append(float(df1.loc[i][8]))
data1 = pd.DataFrame(list(zip(tempdate1, templat1, templon1,tempidx1)))
    
for i in tempidx2:
    x = "{:.0f}-{:.0f}-{:.0f} {:.0f}-{:.0f}-{:.2f}".format(int(df2.loc[i][1]),int(df2.loc[i][2]),\
        int(df2.loc[i][3]),int(df2.loc[i][4]),int(df2.loc[i][5]),\
            float(df2.loc[i][6]))
    tempdate2.append(pass_datetime(x))
    templat2.append(float(df2.loc[i][7]))
    templon2.append(float(df2.loc[i][8]))
data2 = pd.DataFrame(list(zip(tempdate2, templat2, templon2,tempidx2)))

del(tempdate1,tempdate2,tempidx1,tempidx2,templat1,templat2,templon1,templon2)

#compare
compare = []
cidx1 = []
cidx2 = []

for i in range(len(data1)):
    for j in range(len(data2)):
        if ((abs(data1[0][i] - data2[0][j]) < dt.timedelta(seconds=120)) \
            & (abs(data1[1][i] - data2[1][j]) < 0.5) & \
                (abs(data1[2][i] - data2[2][j]) < 0.5)):
            compare.append('True')
            cidx1.append(data1[3][i])
            cidx2.append(data2[3][j])
        else:
            compare.append('False')
            cidx1.append(data1[3][i])
            cidx2.append(data2[3][j])

result = pd.DataFrame(list(zip(cidx1, cidx2, compare)), columns=['cidx1','cidx2','identical'])

#identical 
rm = result[result['identical'] == 'True']

#memory release
del(cidx1,cidx2,compare)
del(x,i,j)

##########################################
# hapus data duplikat di file            #
##########################################

#hapus data di df1 sesuai header yang telah diketahui

idx = df1[df1[0] == '#'].index
tempheader = df1[df1[0] == '#']
tempdata = []

for i in range(len(idx)):
    if idx[i] in rm['cidx1'].values:
        if i == len(idx)-1:
            df1.drop(index = [x for x in range(idx[i],df1.index[-1]+1)], inplace=True)
        else:
            pjbrs = idx[i+1]-idx[i]
            df1.drop(index = [x for x in range(idx[i],idx[i]+pjbrs)], inplace=True)
    else:
        pass

del (tempdata,tempheader)

######################################
#output files                        #
######################################

if df1.empty:
    print("=============================")
    print("===Two Files Are Identical===")
    print("=============================")
else:
    #bugfixing
    df1.to_csv(path+outputname+'.csv',sep='\t',header=None,index=None)
    temp = readabsolute(path+outputname+'.csv')
    ##########
    df2dat(temp, path = path, fname=outputname+'.dat')
    os.remove(path+outputname+'.csv')
    del(temp,i)
    ##########
    notes = open(path+'notes_compare.txt','w+')
    notes.write('files: {} compared with {}'.format(f1,f2))
    notes.close()

#End of Program
tf = dt.datetime.now()
print('finished in : {} seconds'.format(abs(tf-ti).seconds))