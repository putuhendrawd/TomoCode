import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits.basemap import Basemap
import os

path = "G:\\My Drive\\Tomography\\140823\\btstrp-sul-13042023-11082023\\"
N = 50 #Number of Realization/Jumlah bootstrap sample
M = 10421 #>= ID event terakhir
hypo = np.loadtxt(path+'tomoDD.loc', usecols=(0,1,2,3))
id = np.array([int(l)-1 for l in hypo[:,0]])
hx = hypo[:,2]
hy = hypo[:,1]
hz = hypo[:,3]

# create output folder
if not os.path.exists(path+'/output'):
    output_path = path+'/output/'
    os.makedirs(path+'/output')
    print(f'output folder created')
else:
    output_path = path+'/output/'
    print(f'warning, output folder exist!')
# end of create output

# initialize matrix
X = np.zeros((M,N))
Y = np.zeros((M,N))
Z = np.zeros((M,N))

for i in range(N):
    data = np.loadtxt(path+'tomo'+str(i)+'.reloc', usecols=(0,1,2,3))
    idx = np.array([int(l)-1 for l in data[:,0]])
    X[idx,i] = data[:,2]
    Y[idx,i] = data[:,1]
    Z[idx,i] = data[:,3]

X[X==0]=9999
Y[Y==0]=9999
Z[Z==0]=9999

## MapView
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
relative_error = open(path+'output/relative_error.txt', 'w+')
relative_error.write('x_err [km]'+'\t'+'y_err [km]'+'\t'+'z_err [km]'+'\n')
lon_min=118
lon_max=127
lat_min=-7
lat_max=3
interval=2
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
m = Basemap(llcrnrlat=lat_min,urcrnrlat=lat_max,\
            llcrnrlon=lon_min,urcrnrlon=lon_max,lat_ts=interval,resolution='h', ax=ax)
m.drawcoastlines(linewidth=0.5)
m.fillcontinents(color='lightgray',lake_color='white')
m.drawmapboundary(fill_color='white')
m.drawparallels(np.arange(lat_min,lat_max ,interval),labels=[1,0,0,0], linewidth=0.5)
m.drawmeridians(np.arange(lon_min,lon_max ,interval),labels=[0,0,0,1], linewidth=0.5)

ll = 0
for mm in id:
    try:
        x = X[mm,:]
        y = Y[mm,:]
        z = Z[mm,:]

        x = np.delete(x, np.where(x==9999))
        y = np.delete(y, np.where(y==9999))
        z = np.delete(z, np.where(z==9999))


        cov = np.cov(x,z)
        lambda_, v = np.linalg.eig(cov)
        lambdaz1 = np.sqrt(lambda_)
        lambdaz1[np.isnan(lambdaz1)] = 0

        cov = np.cov(y,z)
        lambda_, v = np.linalg.eig(cov)
        lambdaz2 = np.sqrt(lambda_)
        lambdaz2[np.isnan(lambdaz2)] = 0

        cov = np.cov(x,y)
        lambda_, v = np.linalg.eig(cov)
        lambda2 = np.sqrt(lambda_)
        lambda2[np.isnan(lambda2)] = 0
        theta =np.rad2deg(np.arccos(v[0, 0]))

        tempx = lambda2[0] * 111.11
        tempy = lambda2[1] * 111.11
        tempz = (lambdaz1[1] + lambdaz2[1])*0.5

        relative_error.write(str(tempx)+'\t'+str(tempy)+'\t'+str(tempz)+'\n')

        ell = Ellipse(xy=(np.mean(x), np.mean(y)),
                        width=lambda2[0]*2*2, height=lambda2[1]*2*2,
                        angle=theta)

        ell.set_facecolor('none')
        ell.set_edgecolor('b')
        ell.set_linewidth(0.5)
        ax.add_artist(ell)
        # ax.scatter(np.mean(x), np.mean(y), 0.1, edgecolors="blue", facecolor=None)

        ll += 1
    except:
        pass

relative_error.close()

# ax.set_xlabel('Lon [$^o$]')
# ax.set_ylabel('Lat [$^o$]')
#tentukan batas koordinat peta

fig.savefig(path+'output/Top_View_bootstrap1.png', dpi=1200, bbox_inches='tight')
# fig.savefig('output/Top_View_bootstrap1.eps', dpi=2000, bbox_inches='tight')

plt.show()