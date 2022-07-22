'''
Coding: PYTHON UTF-8
Created On: 2022-07-11 13:26:14
Author: Putu Hendra Widyadharma
=== define function for tomocode repository
'''

import pandas as pd
import datetime as dt
import numpy as np
import os

def readabsolute(arg,names = [i for i in range (0,15)]):
    temp= pd.read_csv(arg, delim_whitespace= True, names = names, keep_default_na=False, low_memory=False)
    return temp

def readazgap(arg,names = [i for i in range (0,16)]):
    temp= pd.read_csv(arg, delim_whitespace= True, names = names, keep_default_na=False, low_memory=False)
    return temp

def pass_datetime(text):
    for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', \
        '%Y-%m-%d %H-%M-%S.%f','%Y-%m-%d %H-%M-%S'):
        try:
            return dt.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def df2dat(x,evnum = 0,path = os.getcwd(),fname = 'output.dat'):
    df = x
    
    #if evnum != 0 then remake event number by the evnum input as first event number
    if evnum != 0:
        pd.options.mode.chained_assignment = None
        tempheader = df[df[0] == '#']
        tempdata = df[df[0] != '#']
        tempheader[tempheader.columns[-1]] = np.arange(evnum,evnum+len(tempheader),1)
        df = pd.concat([tempdata,tempheader])
        df.sort_index(inplace = True)
        df.reset_index(inplace = True, drop = True)
    else:
        pass
    
    idx = df[df[0] == '#']
    files = open(path+'/'+fname, 'a', newline='\n')
    for i in range(len(df.index)):
        if i in idx.index:
            tempheader = "{} {: >4.0f} {: >2.0f} {: >2.0f} {: >2.0f} {: >2.0f} {: >4.2f} {: >8.4f} {: >8.4f} {: >3.0f} {: >4.2f} {: >3.0f} {: >3.0f} {: >6.3f} {: >6.0f}\n".\
            format(str(df.iloc[i][0]),float(df.iloc[i][1]),float(df.iloc[i][2]),float(df.iloc[i][3])\
            ,float((df.iloc[i][4])),float(df.iloc[i][5]),float(df.iloc[i][6]),float(df.iloc[i][7])\
            ,float(df.iloc[i][8]),float(df.iloc[i][9]),float(df.iloc[i][10]),float(df.iloc[i][11])\
            ,float(df.iloc[i][12]),float(df.iloc[i][13]),float(df.iloc[i][14]))
            files.write(tempheader)
        else:
            tempdata = "     {: <7}{: >7.2f}{: >6}{: >4} \n".\
            format(str(df.iloc[i][0]),float(df.iloc[i][1]),float(df.iloc[i][2]),(df.iloc[i][3])\
            )
            files.write(tempdata)
    files.close()  
    return print("Output finish: {} at {}".format(fname,path))

def readeventphase(x):
    df = readabsolute(x)
    data = df[df[0] != "#"]
    head = df[df[0] == "#"]
    print("{} event \n{} fasa".format(len(head),len(data)))