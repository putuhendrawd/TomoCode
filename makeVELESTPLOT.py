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

path = "G:\\My Drive\\Tomography\\120523\\velest-sum-110523\\"
fname ="model_sum_arrivals_sum_8P_wadatifilter_8P_150-10D_10PnS_110523_vp.csv"
# input from mod
df = pd.read_csv(path+fname)
depth = df['depth'][:-1].astype('float').to_list()
vp = df.iloc[:-1,1::].values.transpose().tolist()

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
if len(vp) == 1:
    print('run 1')
    fig,ax = plt.subplots(figsize=(3,4), dpi = 1200)
    #plot iter
    # for i in range(1,len(vp)-1):
    #     depth2,vp2 = makeinput(depth,vp[i])
    #     ax.plot(vp2,depth2,color='grey',linestyle="--")

    #plot init
    depth2,vp2 = makeinput(depth,vp[0])
    ax.plot(vp2,depth2,color='black',linestyle='-')

    #plot init
    # depth2,vp2 = makeinput(depth,vp[1])
    # ax.plot(vp2,depth2,color='black',linestyle='--')

    #make legend
    custom_lines = [Line2D([0], [0], color='black', linestyle="-", lw=1),]
    ax.legend(custom_lines, [df.columns[1]],prop={'size': 8})

elif len(vp) == 2:
    print('run 2')
    fig,ax = plt.subplots(figsize=(3,4), dpi = 1200)
    #plot iter
    # for i in range(1,len(vp)-1):
    #     depth2,vp2 = makeinput(depth,vp[i])
    #     ax.plot(vp2,depth2,color='grey',linestyle="--")

    #plot init
    depth2,vp2 = makeinput(depth,vp[0])
    ax.plot(vp2,depth2,color='black',linestyle='-')

    #plot init
    depth2,vp2 = makeinput(depth,vp[1])
    ax.plot(vp2,depth2,color='black',linestyle='--')

    #make legend
    custom_lines = [Line2D([0], [0], color='black', linestyle="-", lw=1),
                    Line2D([0], [0], color='black', linestyle="--", lw=1)]
    ax.legend(custom_lines, [df.columns[1], df.columns[2]],prop={'size': 8})


elif len(vp) == 4:
    print('run 4')
    fig,ax = plt.subplots(figsize=(3,4), dpi = 1200)
    #plot iter
    # for i in range(1,len(vp)-1):
    #     depth2,vp2 = makeinput(depth,vp[i])
    #     ax.plot(vp2,depth2,color='grey',linestyle="--")

    #plot init
    depth2,vp2 = makeinput(depth,vp[0])
    ax.plot(vp2,depth2,color='black',linestyle='-')

    #plot init
    depth2,vp2 = makeinput(depth,vp[1])
    ax.plot(vp2,depth2,color='black',linestyle='--')
    
    #plot output
    depth2,vp2 = makeinput(depth,vp[2])
    ax.plot(vp2,depth2,color='grey',linestyle="-")
    
    #plot output
    depth2,vp2 = makeinput(depth,vp[-1])
    ax.plot(vp2,depth2,color='grey',linestyle="--")

    #make legend
    custom_lines = [Line2D([0], [0], color='black', linestyle="-", lw=1),
                    Line2D([0], [0], color='black', linestyle="--", lw=1),
                    Line2D([0], [0], color='grey', linestyle="-",lw=1),
                    Line2D([0], [0], color='grey', linestyle="--",lw=1)]
    ax.legend(custom_lines, [df.columns[1], df.columns[2], df.columns[3], df.columns[4]],prop={'size': 8})
    
else:
    print('run more')
    fig,ax = plt.subplots(figsize=(3,4), dpi = 1200)
    #plot iter
    for i in range(1,len(vp)-1):
        depth2,vp2 = makeinput(depth,vp[i])
        ax.plot(vp2,depth2,color='grey')

    #plot init
    depth2,vp2 = makeinput(depth,vp[0])
    ax.plot(vp2,depth2,color='black',linestyle='--')

    #plot output
    depth2,vp2 = makeinput(depth,vp[-1])
    ax.plot(vp2,depth2,color='blue',linestyle="-")

    #make legend
    custom_lines = [Line2D([0], [0], color='black', linestyle='--', lw=1),
                    Line2D([0], [0], color='grey', lw=1),
                    Line2D([0], [0], color='blue', lw=1)]
    ax.legend(custom_lines, ["initial", "iteration(s)", "final"],prop={'size': 8})



#image parameter
ax.set_xlim([5,8.5])
ax.set_ylim([0,150])
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.xaxis.set_label_position('top') 
ax.xaxis.set_tick_params(top=True, direction='in',which = 'both')
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_tick_params(right=True, direction='in', which = 'both')
ax.invert_yaxis()
# ax.set_title('1-D Model')
ax.set_xlabel('Velocity (km/s)')
ax.set_ylabel('Depth (km)')
fig.savefig(path+f"velocity model {Path(fname).stem}.png",bbox_inches = 'tight', transparent=False)