#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = 'E:\\My Drive\\Tomography\\041022\\rms-sta-sebelum-ssdh-indoburma\\'
outputpath = 'E:\\My Drive\\Tomography\\Shared Hasil\\Indoburma\\hasil\\'
fname1 = 'tomoDD-sblm-indoburma.res'
fname2 = 'tomoDD-ssdh-indoburma.res'

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
ax.set_xlim([-6,6])
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
ax[0].hist(df1["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', edgecolor='black',facecolor ='#C0C4C5', label='before')
ax[1].hist(df2["RES"], bins = np.arange(-15.75,15.75, 0.5),align = 'mid', edgecolor='black',facecolor ='#4B4951', label='after')
ax[0].set_xticks(np.arange(-6,7,1))
plt.setp(ax, xlim=[-6,6], ylim=[0,30000])
fig.supxlabel('RMS Residual (s)', ha='center')
fig.supylabel('Number of Observations', va='center', x=-.01)
fig.suptitle('RMS Residual Indoburma',y=0.95)
ax[0].legend()
ax[1].legend()
fig.savefig(outputpath+'RMS Indoburma.jpg' ,bbox_inches = 'tight')
# %%
