import pandas as pd
from localfunction import *

path = 'D:/cache/gabung/'
fname = 'outputF1_indoburma_1964-2020.txt'
staname = 'STA_LIST.dat'

#load absolute data
df = readabsolute(path+fname)

#load station data
stafile = pd.read_csv(path+staname, delim_whitespace = True,names = [0,1,2,3], header=None)
#cleaning and formating
stafile.drop_duplicates(subset=0,keep='first',inplace=True)
stafile.set_index(0, inplace = True)
stafile.drop(stafile.head(1).index, inplace=True)
stafile = stafile.astype(float)


#compare
staavail = pd.DataFrame(columns = ['STA', 'Available'])
staavail['STA'] = df[0].unique()
for i in staavail.index:
    item = r'^' + str(staavail['STA'][i]) + '$'
    staavail['Available'][i] = stafile.index.str.match(item).any()
staavail.set_index('STA', inplace = True)

del(i,item)


#cek grid
checker = []
for i in stafile.index:
    if ((91.5 <= stafile.loc[i][1] <= 98.1) and (18.5 <= stafile.loc[i][2] <= 28.1)):
        checker.append('Grid Dalam')
    elif (((84 <= stafile.loc[i][1] < 91.5) or (98.1 < stafile.loc[i][1] <= 105)) and \
        ((12 <= stafile.loc[i][2] < 18.5) or (28.1 < stafile.loc[i][2] <= 34))):
        checker.append('Grid Luar')
    else:
        checker.append('Diluar Batas Grid')
    
stafile['status'] = checker
#df2dat(df,path=path,evnum=1)