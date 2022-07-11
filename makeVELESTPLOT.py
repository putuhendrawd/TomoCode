import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
from localfunction import *

# input from mod


#manual input 
depth = [-5,0,10,20,30,40,50,60,70,90,120,140,210,360,510]
vp = [6.781,6.810,6.867,6.924,6.981,7.038,7.095,7.152,7.209,7.323,7.494,7.608,8.007,8.862,9.717]
#vp = [4.6,6.20,6.20,6.21,6.66,7.54,7.67,7.67,8.14,8.14,8.16,8.19,8.39,8.94,9.03]

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

depth2,vp2 = makeinput(depth,vp)

fig,ax = plt.subplots(figsize=(3,6), dpi = 300)
ax.plot(vp2,depth2)
ax.set_ylim([-10,max(depth2)-10])
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.invert_yaxis()
ax.set_title('1-D Model')
ax.set_xlabel('P-Wave Velocity [km/s]')
ax.set_ylabel('Depth [km]')