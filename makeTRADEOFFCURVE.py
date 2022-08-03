'''
Coding: PYTHON UTF-8
Created On: 2022-08-01 08:02:19
Author: Putu Hendra Widyadharma
=== make trade off curve model variance vs data variance
'''

from xml.dom.pulldom import IGNORABLE_WHITESPACE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import float64, math
from pyparsing import lineStart
from localfunction import *

#initializaion
df = pd.DataFrame([],columns=['model_var','data_var','damp'])
damp = [10,80,100,200,300,500]
parent = 'E:\\My Drive\\Tomography\\030822\\multidamp-02082022\\'
#read 
for z in damp:
    path = parent+'\\Output_Files_damp_{}\\'.format(z)
    #load data
    filevp = path+'Vp_model.dat'
    data = np.loadtxt(filevp)
    #calculate model variance
    modelvar = np.var(data, dtype=np.float64)

    #load fort.10 data
    f = open(path+'fort.10_damp_{}'.format(z),encoding='utf8',errors='ignore')
    file = f.readlines()
    for i in range(len(file)):
        file[i] = file[i].split()
    #read data variance
    iter = list(range(1,len(file)+1))
    mark = False
    done = False
    for i in iter:
        if (len(file[-i])>3) and (file[-i][0] == 'Iteration') and (file[-i][2] == 'finished') and (mark == False):
            print('Iteration end: {}'.format(file[-i][1]))
            mark = True
        if (len(file[-i])>3) and mark and (file[-i][0] == 'absolute') and (file[-i][1] =='variance'):
            datavar = file[-i][4]
            print('absolute variance: {}'.format(datavar))
            print('model variance: {}'.format(modelvar))
            done = True
        if done:
            mark= False
            done= False
            break
    df = pd.concat([df,pd.Series([modelvar,datavar,z],index=df.columns).to_frame().transpose()])

df.sort_values(by='data_var',inplace=True)
df.reset_index(inplace=True)
#make graph
fig,ax = plt.subplots()
ax.plot(df['data_var'],df['model_var'],marker='o',linestyle='dashed')
c=0
for x,y in zip(df['data_var'],df['model_var']):
    ax.annotate(df['damp'][c],(x,y),textcoords="offset points",xytext=(0,10),ha='center')
    c=c+1
ax.set_ylim(min(df['model_var'])-0.005,max(df['model_var'])+0.005)
ax.set_ylabel('model variance')
ax.set_xlabel('data variance')
fig.savefig(parent+'output.png')