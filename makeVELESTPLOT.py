'''
Coding: PYTHON UTF-8
Created On: 2022-07-13 21:28:20
Author: Putu Hendra Widyadharma
=== make velest plot, input vp_extract.txt from readVPfromVELESTOUTPUT function
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
from matplotlib.lines import Line2D
from localfunction import *

path = "E:\\My Drive\\Tomography\\130722\\Velest33-indoburma\\output\\"
# input from mod
df = pd.read_csv(path+"vp_extract.txt")
depth = df['depth'].to_list()
vp = df.iloc[:,1:12].values.transpose().tolist()

#=========================================
def makeinput(depth,vp):
    depth2 = depth + depth
    depth2.sort()
    depth2.remove(min(depth2))
    depth2.append(max(depth2)+50)

    vp2 = vp + vp
    vp2.sort()
    return(depth2,vp2)
#=========================================

fig,ax = plt.subplots(figsize=(3,6), dpi = 300)

#plot iter
for i in range(1,len(vp)-1):
    depth2,vp2 = makeinput(depth,vp[i])
    ax.plot(vp2,depth2,color='grey')

#plot init
depth2,vp2 = makeinput(depth,vp[0])
ax.plot(vp2,depth2,color='blue',linestyle='--')

#plot output
depth2,vp2 = makeinput(depth,vp[-1])
ax.plot(vp2,depth2,color='blue')

#make legend
custom_lines = [Line2D([0], [0], color='blue', linestyle='--', lw=1),
                Line2D([0], [0], color='grey', lw=1),
                Line2D([0], [0], color='blue', lw=1)]
ax.legend(custom_lines, ['Input Model', 'Interation', 'Updated Model'],prop={'size': 5})

#image parameter
ax.set_xlim([5.5,10.3])
ax.set_ylim([-5,max(depth)])
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.xaxis.set_tick_params(top=True, direction='in',which = 'both')
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_tick_params(right=True, direction='in', which = 'both')
ax.invert_yaxis()
ax.set_title('1-D Model')
ax.set_xlabel('P-Wave Velocity [km/s]')
ax.set_ylabel('Depth [km]')
fig.savefig(path+"output_velest.jpg",bbox_inches = 'tight')