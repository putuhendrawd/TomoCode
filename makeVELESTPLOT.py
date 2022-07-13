import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
from matplotlib.lines import Line2D
from localfunction import *

path = "E:\\My Drive\\Tomography\\130722\\Velest33-indoburma\\output\\"
# input from mod


#manual input 
depth = [-5,0,10,20,40,50,60,70,90,120,140,165,210,360,510]
vp = [[5.51,5.51,5.51,5.74,5.91,6.11,6.5,6.76,6.95,7.55,8.07,8.3,8.75,9.12,9.27],
      [5.566,5.567,5.568,5.587,5.919,6.131,6.54,6.8,7.018,7.613,8.196,8.326,8.95,9.12,9.27],
      [5.624,5.625,5.626,5.627,5.907,6.146,6.571,6.842,7.074,7.669,8.261,8.262,9.15,9.151,9.27],
      [5.678,5.679,5.68,5.681,5.906,6.158,6.596,6.883,7.111,7.695,8.318,8.319,9.35,9.351,9.352],
      [5.737,5.738,5.739,5.74,5.909,6.164,6.622,6.953,7.132,7.725,8.375,8.376,9.547,9.548,9.549],
      [5.789,5.79,5.791,5.792,5.909,6.168,6.646,7.015,7.154,7.721,8.474,8.475,9.706,9.707,9.708],
      [5.845,5.864,5.865,5.866,5.908,6.171,6.662,7.083,7.153,7.71,8.589,8.59,9.853,9.854,9.855],
      [5.901,5.955,5.956,5.957,5.958,6.175,6.682,7.152,7.153,7.703,8.705,8.706,9.99,9.991,9.992],
      [5.96,6.062,6.063,6.064,6.065,6.184,6.706,7.221,7.222,7.681,8.822,8.823,10.117,10.118,10.119],
      [6.024,6.173,6.174,6.175,6.176,6.196,6.729,7.337,7.338,7.649,8.942,8.943,10.234,10.235,10.236],
      [6.02,6.17,6.17,6.18,6.18,6.2,6.73,7.34,7.34,7.65,8.94,8.94,10.23,10.23,10.24]
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