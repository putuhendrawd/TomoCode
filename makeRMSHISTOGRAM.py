#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = 'D:\\'
outputpath = 'D:\\'
fname1 = 'Cianjur-hypoDD-sebelum.res'
fname2 = 'Cianjur-hypoDD-setelah.res'

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

	#df = df[df['RES'] < 15]
	return (df)

df1 = data(fname1)
df2 = data(fname2)
z = np.array([df1['RES'],df2['RES']])
aa = z.transpose()
#%% combine
fig, ax = plt.subplots(dpi = 1200)
ax.hist(df1["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', edgecolor='black',facecolor ='#C0C4C5', label='before')
ax.hist(df2["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', edgecolor='black',facecolor ='#4B4951', label='after')
ax.hist(df1["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', facecolor='None', edgecolor='black')
# ax.hist(aa, bins = np.arange(-15.75,15.75, 0.5),align = 'mid', stacked = True, color = ['#C0C4C5', '#4B4951'],edgecolor='black')
ax.set_xlim([-1,1])
ax.set_ylim([0,30000])
ax.set_xlabel('RMS Residual (s)')
ax.set_xticks(np.arange(-6,7,1))
ax.set_ylabel('Number of Observations')
ax.set_title('RMS Residual Sumatera',y=1.03)
ax.legend()
fig.savefig(outputpath+'RMS Sumatera.jpg' ,bbox_inches = 'tight')
# fig.close()
# %% up and down
fig, ax = plt.subplots(nrows= 2,ncols=1, sharex = True, sharey = True, dpi = 1200)
# ax.hist(df1["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', edgecolor='None',facecolor ='#C0C4C5', label='before')
ax[0].hist(df1["RES"], bins = np.arange(-0.25,0.3, 0.025),align = 'left', edgecolor='black',facecolor ='#C0C4C5', label='before relocation')
ax[1].hist(df2["RES"], bins = np.arange(-0.25,0.3, 0.025),align = 'left', edgecolor='black',facecolor ='#4B4951', label='after relocation')
ax[0].set_xticks(np.arange(-0.3,0.4,0.1))
plt.setp(ax, xlim=[-0.3,0.3], ylim=[0,250])
fig.supxlabel('RMS Residual (s)', ha='center')
fig.supylabel('Number of Observations', va='center', x=-.01)
fig.suptitle('RMS Residual Cianjur',y=0.95)
ax[0].legend()
ax[1].legend()
fig.savefig(outputpath+'RMS Cianjur.jpg' ,bbox_inches = 'tight')
# %%
