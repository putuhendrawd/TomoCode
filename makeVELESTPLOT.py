import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
from matplotlib.lines import Line2D
from localfunction import *

path = "E:\\My Drive\\Tomography\\130722\\"
# input from mod


#manual input 
depth = [-10.0,0.0,5.0,10.0,20.0,30.0,40.0,60.0]
vp = [[6.75,6.8,6.83,6.86,6.92,6.98,7.03,7.15],
      [6.75,6.79,6.82,6.85,6.96,7.05,7.14],
      [6.75,6.79,6.81,6.84,6.96,7.08,7.19],
      [6.75,6.79,6.81,6.83,6.95,7.11,7.22],
      [6.75,6.79,6.81,6.83,6.95,7.11,7.24],
      [6.75,6.79,6.81,6.83,6.94,7.11,7.25],
      [6.75,6.79,6.81,6.83,6.94,7.1,7.26],
      [6.75,6.78,6.81,6.82,6.94,7.1,7.26],
      [6.75,6.78,6.81,6.82,6.94,7.09,7.26],
      [6.75,6.78,6.81,6.82,6.94,7.09,7.26],
      [6.75,6.78,6.81,6.82,6.94,7.09,7.26,8.27]
      ]

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

#plot init
depth2,vp2 = makeinput(depth,vp[0])
ax.plot(vp2,depth2,color='blue',linestyle='--')

#plot iter
for i in range(1,len(vp)-1):
    depth2,vp2 = makeinput(depth[:7],vp[i])
    ax.plot(vp2,depth2,color='grey')

#plot output
depth2,vp2 = makeinput(depth,vp[-1])
ax.plot(vp2,depth2,color='blue')

#make legend
custom_lines = [Line2D([0], [0], color='blue', linestyle='--', lw=1),
                Line2D([0], [0], color='grey', lw=1),
                Line2D([0], [0], color='blue', lw=1)]
ax.legend(custom_lines, ['Input Model', 'Interation', 'Updated Model'],prop={'size': 5})

ax.set_xlim([6.7,7.3])
ax.set_ylim([-10,max(depth)])
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.xaxis.set_tick_params(top=True, direction='in',which = 'both')
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_tick_params(right=True, direction='in', which = 'both')
ax.invert_yaxis()
ax.set_title('1-D Model')
ax.set_xlabel('P-Wave Velocity [km/s]')
ax.set_ylabel('Depth [km]')
fig.savefig(path+"output_velest.jpg",bbox_inches = 'tight')