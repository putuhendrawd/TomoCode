'''
Coding: PYTHON UTF-8
Created On: 2022-08-01 08:02:19
Author: Putu Hendra Widyadharma
=== make trade off curve model variance vs data variance
=== new formula model var
'''

from xml.dom.pulldom import IGNORABLE_WHITESPACE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import float64, math
from pyparsing import lineStart
from localfunction import *
from matplotlib.ticker import FormatStrFormatter
import statistics

#initializaion
df = pd.DataFrame([],columns=['model_var','data_var','damp'])
damp = [10,30,60,70,80,100,180,200,220,300,400,500]
parent = 'G:\\My Drive\\Tomography\\010323\\varians_model_sul'
varvariable = 'weighted' # 'absolute' or 'weighted'
#read 
with open(parent+'\\MOD') as modf:
    mod=modf.readline().split()
    lenlon=int(mod[1])
    lenlat=int(mod[2])
    lendepth=int(mod[3])

for z in damp:
    path = parent+'\\Output_Files_damp_{}\\'.format(z)
    # path = parent
    #load data
    filevp = path+f'\\Vp_model.dat'
    datavp = np.loadtxt(filevp)
    varperlayer=[]
    for i in range(lendepth):
        data = datavp[lenlat*i:lenlat*(i+1)]
        mean = data[0,0]
        datatemp=data.ravel()
        #variance calc
        datatemp = (datatemp-mean)**2
        varperlayer.append(datatemp.sum()/len(datatemp))
    modelvar = statistics.mean(varperlayer)
    
    #load fort.10 data
    f = open(path+'\\fort.10_damp_{}'.format(z),encoding='utf8',errors='ignore')
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
        if (len(file[-i])>3) and mark and (file[-i][0] == varvariable) and (file[-i][1] =='variance'):
            datavar = float(file[-i][4]) 
            print(f'{varvariable} variance: {datavar}')
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

#select data
# df = df[(df['damp'] != 30)]
# df = df[(df['damp'] != 10)]
# df = df[(df['damp'] != 70)]
# df = df[(df['damp'] != 80)]
# df = df[(df['damp'] != 180)]
df.reset_index(inplace=True)

#make graph
fig,ax = plt.subplots(dpi=300)
ax.plot(df['model_var'],df['data_var'],marker='o',linestyle='-')
c=0
for x,y in zip(df['model_var'],df['data_var']):
    # if c==7:
    #     ax.annotate(int(df['damp'][c]),(x,y),textcoords="offset points",xytext=(10,2),ha='center')
    # elif c==10:
    #     ax.annotate(int(df['damp'][c]),(x,y),textcoords="offset points",xytext=(10,-2),ha='center')
    # elif c==9:
    #    ax.annotate(int(df['damp'][c]),(x,y),textcoords="offset points",xytext=(6,5),ha='center')
    # else:
    ax.annotate(int(df['damp'][c]),(x,y),textcoords="offset points",xytext=(10,5),ha='center')
    c=c+1

ax.set_xlim(min(df['model_var'])-0.003,max(df['model_var'])+0.003)   
ax.set_ylim(min(df['data_var'])-5,max(df['data_var'])+10)
ax.set_ylabel('data variance (s)')
ax.set_xlabel('model variance (km/s)')
fig.savefig(parent+f'\\TradeOffCurve2-{varvariable}-8.jpg',bbox_inches = 'tight')
