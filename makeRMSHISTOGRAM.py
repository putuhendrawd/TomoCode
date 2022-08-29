import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = 'D:\\BMKG Putu\\Tomography\\270622\\plot-histogram-rms-sumatra\\'
outputpath = 'D:\\BMKG Putu\\Tomography\\260822\\rmssumatera\\'
fname1 = 'tomoDD-sebelum-sum.res'
fname2 = 'tomoDD-sesudah-sum.res'

def data(fname):
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
	return (df)

df1 = data(fname1)
df2 = data(fname2)
z = np.array([df1['RES'],df2['RES']])
aa = z.transpose()
#%%
fig, ax = plt.subplots(dpi = 1200)
#ax.hist(df1["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', edgecolor='black',facecolor ='grey')
#ax.hist(df2["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', edgecolor='black',facecolor ='grey')
ax.hist(aa, bins = np.arange(-15.75,15.75, 0.5),align = 'mid', stacked = True, color = ['#C0C4C5', '#4B4951'],edgecolor='black')
ax.set_xlim([-5,5])
ax.set_ylim([0,90000])
ax.set_xlabel('RMS Residual (s)')
ax.set_xticks(np.arange(-6,7,1))
ax.set_ylabel('Number of Observations')
ax.set_title('RMS Residual Sumatera',y=1.03)
fig.savefig(outputpath+'RMS Sumatera.jpg' ,bbox_inches = 'tight')
# %%
