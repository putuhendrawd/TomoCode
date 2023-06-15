#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = 'G:\\My Drive\\Tomography\\060623\\rms_residual_plot\\'
outputpath = path
fname1 = 'tomoDD-before3.res' #before
fname2 = 'tomoDD-after6.res' #after

def data(fname):
	try:
		file = open(path+fname,'r')
		baris = file.readlines()
		for i in range(len(baris)):
			baris[i]=baris[i].split()
		file.close()


		df = pd.DataFrame(baris, columns = baris[0])
		df.drop(0, inplace = True)
		df.reset_index(drop = True, inplace=True)

		df = df[df['C1'] == df['C2']]
		df = df[df['RES'] != '************']
		df['RES'] = pd.to_numeric(df['RES'])
		df['RES'] = df['RES'].div(1000)

		#df = df[df['RES'] < 15]
		print("read file success")
		return (df)
	except:
		print("file could not be loaded, return zero dataframe")
		return(pd.DataFrame([]))
print("==read before")
df1 = data(fname1)
print("==read after")
df2 = data(fname2)
# z = np.array([df1['RES'],df2['RES']])
# aa = z.transpose()
#%% combine
bins_ = np.arange(-9.5,10.5,1)
fig, ax = plt.subplots(dpi = 1200)
ax.hist(df1["RES"], bins = bins_,align = 'mid', edgecolor='black',facecolor ='#C0C4C5', label='before')
ax.hist(df2["RES"], bins = bins_,align = 'mid', edgecolor='black',facecolor ='#4B4951', label='after')
ax.hist(df1["RES"], bins = bins_,align = 'mid', facecolor='None', edgecolor='black')
# ax.hist(aa, bins = np.arange(-15.75,15.75, 0.5),align = 'mid', stacked = True, color = ['#C0C4C5', '#4B4951'],edgecolor='black')
ax.set_xlim([-1,1])
ax.set_ylim([0,50000])
ax.set_xlabel('RMS Residual (s)')
ax.set_xticks(np.arange(-6,7,1))
ax.set_ylabel('Number of Observations')
ax.set_title('RMS Residual Sumatera',y=1.03)
ax.legend()
fig.savefig(outputpath+'RMS Combine.jpg' ,bbox_inches = 'tight')
# fig.close()

# %% up and down
print("==run up and down plot")
bins_ = np.arange(-9.5,10.5,1)
fig, ax = plt.subplots(nrows= 2,ncols=1, sharex = True, sharey = True, dpi = 1200)
if not df1.empty:
	max = round(df1["RES"].max(),3)
	min = round(df1["RES"].min(),3)
	med = round(df1["RES"].median(),3)
	ax[0].hist(df1["RES"], bins = bins_,align = 'mid', edgecolor='black',facecolor ='#C0C4C5', label='before relocation')
	ax[0].text(0.02,0.85,f"min: {min:>6}", size = "small", family= "monospace", transform=ax[0].transAxes)
	ax[0].text(0.02,0.75,f"max: {max:>6}", size = "small", family= "monospace", transform=ax[0].transAxes)
	ax[0].text(0.02,0.65,f"med: {med:>6}", size = "small", family= "monospace", transform=ax[0].transAxes)	
	ax[0].legend()
if not df2.empty:
    max = round(df2["RES"].max(),3)
    min = round(df2["RES"].min(),3)
    med = round(df2["RES"].median(),3)
    ax[1].hist(df2["RES"], bins = bins_,align = 'mid', edgecolor='black',facecolor ='#4B4951', label='after relocation')
    ax[1].text(0.02,0.85,f"min: {min:>6}", size = "small", family= "monospace", transform=ax[1].transAxes)
    ax[1].text(0.02,0.75,f"max: {max:>6}", size = "small", family= "monospace", transform=ax[1].transAxes)
    ax[1].text(0.02,0.65,f"med: {med:>6}", size = "small", family= "monospace", transform=ax[1].transAxes)	
    ax[1].legend()
plt.setp(ax, xlim=[-6,7], ylim=[0,150000])
fig.supxlabel('RMS Residual (s)', ha='center')
fig.supylabel('Number of Observations', va='center', x=-.01)
fig.suptitle('RMS Residual',y=0.95)
fig.savefig(outputpath+'RMS Split.jpg' ,bbox_inches = 'tight')
print(f"==save complete on {outputpath}")
# %%

