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
from matplotlib.ticker import FormatStrFormatter

#initializaion
df = pd.DataFrame([],columns=['model_var','data_var','damp'])
damp = [10,20,40,90,100,120,150,200,300,400,500]
parent = 'G:\\My Drive\\Tomography\\020323\\vartes-sum-09092022\\'
#read 
for z in damp:
    path = parent+'Output_Files_damp_{}\\'.format(z)
    path=parent
    #load data
    filevp = path+f'Vp_model-damp{z}.dat'
    data = np.loadtxt(filevp)
    data = data[:-105]
    #data = data / 1000
    #calculate model variance
    modelvar = np.var(data, dtype=np.float64)

    #load fort.10 data
    f = open(path+'fort.10_damp_{}'.format(z),encoding='utf8',errors='ignore')
    print('open damp {}'.format(z))
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
        if (len(file[-i])>3) and mark and (file[-i][0] == 'weighted') and (file[-i][1] =='variance'):
            datavar = file[-i][4]
            print('weighted variance: {}'.format(datavar))
            print('model variance: {}'.format(modelvar))
            done = True
        if done:
            mark= False
            done= False
            break
    df = pd.concat([df,pd.Series([modelvar,datavar,z],index=df.columns).to_frame().transpose()])

df = df.astype('float64')
df.sort_values(by='model_var',inplace=True)
df.reset_index(inplace=True)

#make graph
fig,ax = plt.subplots()
ax.plot(df['model_var'],df['data_var'],marker='o',linestyle='None')
c=0
for x,y in zip(df['model_var'],df['data_var']):
    ax.annotate(df['damp'][c],(x,y),textcoords="offset points",xytext=(0,10),ha='center')
    c=c+1
#ax.set_ylim(min(df['model_var'])-0.005,max(df['model_var'])+0.005)
ax.set_ylabel('data variance')
ax.set_xlabel('model variance')
fig.show()
# fig.savefig(parent+'output.jpg',bbox_inches = 'tight')

#make graph dual y
# fig,ax = plt.subplots()
# ax.plot(df['damp'],df['model_var'],marker='o',linestyle='dashed', color='black')
# ax2=ax.twinx()
# ax2.plot(df['damp'],df['data_var'],marker='o',linestyle='dashed', color = 'blue')
# ax.set_ylim(1,1.06)
# ax.set_ylabel('model variance')
# ax.set_xlabel('damping')
# ax.tick_params(axis='y', color='black', labelcolor='black')
# ax2.set_ylabel('data variance',color='blue')
# ax2.tick_params(axis='y', color='blue', labelcolor='blue')
# ax2.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
# ax2.set_ylim(350,650)
# fig.savefig(parent+'output2.jpg',bbox_inches = 'tight')