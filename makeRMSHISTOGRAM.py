import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = 'E:\\My Drive\\Tomography\\030722\\rms-sblm-ssdh-sul\\'
outputpath = 'E:\\My Drive\\Tomography\\030722\\RMS Histogram\\'
fname = 'tomoDD-before-rel.res'
a = 'Sebelum'
b = 'Sulawesi'

file = open(path+fname,'r')
baris = file.readlines()
for i in range(len(baris)):
	baris[i]=baris[i].split()
file.close()


df = pd.DataFrame(baris, columns = baris[0])
df.drop(0, inplace = True)
df.reset_index(drop = True, inplace=True)

df = df[df['RES'] != '************']
df['RES'] = pd.to_numeric(df['RES'])
df['RES'] = df['RES'].div(1000)

df = df[df['RES'] < 15]

#%%
fig, ax = plt.subplots(dpi = 1200)
ax.hist(df["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', edgecolor='black',facecolor ='grey')
ax.set_xlim([-6.5,6.5])
ax.set_ylim([0,180000])
ax.set_xlabel('RMS (s)')
ax.set_xticks(np.arange(-6,7,1))
ax.set_ylabel('Counts')
ax.set_title('RMS {} {}'.format(a,b),y=1.03)
fig.savefig(outputpath+'RMS Histogram {} {}.jpg'.format(a,b),bbox_inches = 'tight')