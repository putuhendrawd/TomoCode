import numpy as np
import pandas as pd
import geopy.distance as gd
import matplotlib.pyplot as plt
from numpy import float64, math
from localfunction import *
pd.options.mode.chained_assignment = None

# =============================================================================
# define function to calculate angle relative to north of the event
# =============================================================================
def kuadran1(x1,y1):
    depan1 = np.sqrt(y1*y1*111.325*111.325)
    samping1 = np.sqrt(x1*x1*111.325*111.325)
    teta1 = math.degrees(math.atan(depan1/samping1))
    azimuth1 = 90.0 - teta1 
    return(azimuth1)

def kuadran2(x2,y2):
    depan2 = np.sqrt(y2*y2*111.325*111.325)
    samping2 = np.sqrt(x2*x2*111.325*111.325)
    teta2 = math.degrees(math.atan(depan2/samping2))
    azimuth2 = 270.0 + teta2
    return(azimuth2)

def kuadran3(x3,y3):
    depan3 = np.sqrt(y3*y3*111.325*111.325)
    samping3 = np.sqrt(x3*x3*111.325*111.325)
    teta3 = math.degrees(math.atan(depan3/samping3))
    azimuth3 = 270.0 - teta3
    return(azimuth3)

def kuadran4(x4,y4):
    depan4 = np.sqrt(y4*y4*111.325*111.325)
    samping4 = np.sqrt(x4*x4*111.325*111.325)
    teta4 = math.degrees(math.atan(depan4/samping4))
    azimuth4 = 90.0 + teta4
    return(azimuth4)

# =============================================================================
# path and filename 
# =============================================================================
path = 'E:\\My Drive\\Tomography\\LatestData\\'
outputpath = 'E:\\My Drive\\Tomography\\290622\\Azimuth Gap Histogram\\'
fname = 'phase-indoburma-3-fixed-plus-510sta.dat'
staname = 'station-indoburma.dat'
daerah = 'Indoburma510'

# =============================================================================
# baca data absolute
# =============================================================================
df = readabsolute(path+fname)
idx = df[df[0] == '#'].index

# =============================================================================
# baca database stasiun
# =============================================================================
stafile = pd.read_csv(path+staname, delim_whitespace = True,names = [0,1,2,3])
stafile.set_index(0, inplace = True)

# =============================================================================
# cek ketersediaan stasiun di database stasiun
# =============================================================================
staavail = pd.DataFrame(columns = ['STA', 'Available'])
staavail['STA'] = df[0].unique()
for i in staavail.index:
    item = r'^' + str(staavail['STA'][i]) + '$'
    staavail['Available'][i] = stafile.index.str.match(item).any()
staavail.set_index('STA', inplace = True)

del(i,item)

# =============================================================================
# input data relative lat dan lon stasiun terhadap gempa + angle
# =============================================================================
for i in df.index:
    if i in idx:
        originlat = float(df.iloc[i,7])
        originlon = float(df.iloc[i,8])
        temporigin = (df.iloc[i,7],df.iloc[i,8])
    else:
        x = df.iloc[i,0]
        if staavail.loc[x].any() == False:
            df.iloc[i,4] = '#NA'
            df.iloc[i,5] = '#NA'
            #df = df.drop(i)
        else:
            stalat = stafile.loc[x,1]
            stalon = stafile.loc[x,2] 
            df.iloc[i,4] = stalat - originlat #relative latitude
            df.iloc[i,5] = stalon - originlon #relative longitude
            
            #calculating angle
            if df.iloc[i,5] > 0:
                if df.iloc[i,4] > 0:
                    az = kuadran1(df.iloc[i,5],df.iloc[i,4])
                    df.iloc[i,6] = az #angle from north
                else:
                    az = kuadran4(df.iloc[i,5],df.iloc[i,4])
                    df.iloc[i,6] = az #angle from north
            else:
                if df.iloc[i,4] > 0:
                    az = kuadran2(df.iloc[i,5],df.iloc[i,4])
                    df.iloc[i,6] = az #angle from north
                else:
                    az = kuadran3(df.iloc[i,5],df.iloc[i,4])
                    df.iloc[i,6] = az #angle from north

del(i,originlat,originlon,temporigin,x,stalat,stalon,az)

# =============================================================================
# sort by angle, calculate, and store data
# =============================================================================
df = df[df[4] != '#NA']
df.sort_index(inplace = True)
df.reset_index(inplace = True, drop = True)
idx = df[df[0] == '#'].index

tempheader = df[df[0]== '#']
tempdata = pd.DataFrame([],columns = df.columns)
azgapmax = []
for a in range (len(idx)):
    #buat data per kejadian gempa
    if a == len(idx)-1:
        tempdf = df.iloc[idx[a]::]
    else:
        tempdf = df.iloc[idx[a]:idx[a+1],:]
    #drop header
    tempdf.drop(idx[a], inplace = True)
    if (len(tempdf.index) >= 1):
        #tempdf[4,5,6].astype(float64)
        #drop duplicate station
        tempdf = tempdf.drop_duplicates(subset=[0], keep = 'first')
        #index template
        tempindex = tempdf.index
        #sort by angle
        tempdf.sort_values(by=[6], inplace = True)
        tempdf.set_index(pd.Index(tempindex), inplace = True)
        #calculate azimuth gap
        for i in range (len(tempdf)):
            if i == len(tempdf)-1:
                tempdf.iloc[i,7] = 360 - tempdf.iloc[i,6] + tempdf.iloc[0,6]
            else:
                tempdf.iloc[i,7] = tempdf.iloc[i+1,6] - tempdf.iloc[i,6] #azimuth gap of data [i+1] - [i]
        #save maximum az gap
        azgapmax.append(tempdf[7].max())
        #join data
        tempdata = pd.concat([tempdata,tempdf])
    else:
        #hapus header
        tempheader.drop(idx[a], inplace = True)

#append azgapmax
tempheader[15] = azgapmax
df = pd.concat([tempdata,tempheader])
df.sort_index(inplace = True)
df.reset_index(inplace = True, drop = True)

del(a,i,azgapmax,tempindex)

#%%
# =============================================================================
# make histogram
# =============================================================================

x = tempheader[15].to_list()
import matplotlib.ticker as ticker
from matplotlib.ticker import PercentFormatter
fig, ax = plt.subplots(dpi=1200)
ax.hist(x, bins = np.arange(15, 375, 30), align = 'mid',edgecolor='black',facecolor ='grey')
ax.set_xlim([-15,375])
ax.set_xlabel('Azimuthal Gap (deg)')
ax.set_ylabel('Number of Rays ')
# ax.yaxis.set_major_formatter(PercentFormatter(1,symbol = None))
ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
fig.savefig(outputpath+'Azimuthal Gap Histogram {}.jpg'.format(daerah))