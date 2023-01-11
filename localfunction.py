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
    print("readabsolute: read file success")
    return temp

def readazgap(arg,names = [i for i in range (0,16)]):
    temp= pd.read_csv(arg, delim_whitespace= True, names = names, keep_default_na=False, low_memory=False)
    return temp

def readres(arg):
    try:
        file = open(arg,'r')
        baris = file.readlines()
        for i in range(len(baris)):
            baris[i]=baris[i].split()
        file.close()

        df = pd.DataFrame(baris, columns = baris[0])
        df.drop(0, inplace = True)
        df.reset_index(drop = True, inplace=True)
        df.drop("OFFS", axis=1, inplace=True)
        df.columns = ["STA", "DT", "C1", "C2", "IDX", "QUAL", "RES", "WT", "OFFS"]
        df = df[df['C1'] == df['C2']]
        df = df[df['RES'] != '************']
        df['RES'] = pd.to_numeric(df['RES'])
        df['RES'] = df['RES'].div(1000)
        df.reset_index(drop = True, inplace=True)
        df["C1"]=df["C1"].apply(pd.to_numeric)
        df["C2"]=df["C2"].apply(pd.to_numeric)
        print("readres: read file success")
        return (df)
    except:
        print("readres: file could not be loaded, return zero dataframe")
        return(pd.DataFrame([]))

def readsta(arg, names=[i for i in range(12)]):
    temp = pd.read_csv(arg, delim_whitespace = True,names = names)
    temp.set_index(0, inplace = True)
    temp.dropna(axis=1, how='all',inplace=True)
    print("readsta: read file success")
    return(temp)

def pass_datetime(text):
    for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', \
        '%Y-%m-%d %H-%M-%S.%f','%Y-%m-%d %H-%M-%S'):
        try:
            return dt.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def df2dat(x,evnum = 0,path = os.getcwd(),fname = 'output.dat',mode='w'):
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
    files = open(path+'/'+fname, str(mode), newline='\n')
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
            format(str(df.iloc[i][0]),float(df.iloc[i][1]),float(df.iloc[i][2]),(df.iloc[i][3]))
            files.write(tempdata)
    files.close()  
    return print("Output finish: {} at {}".format(fname,path))

def readeventphase(x):
    df = readabsolute(x)
    data = df[df[0] != "#"]
    head = df[df[0] == "#"]
    print("{} event \n{} fasa".format(len(head),len(data)))