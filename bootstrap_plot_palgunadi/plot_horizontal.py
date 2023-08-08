import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits.basemap import Basemap

path = "G:\\My Drive\\Tomography\\080823\\btstrp-sul-13042023-08082023\\"
N = 50 #Number of Realization/Jumlah bootstrap sample
M = 10421 #>= ID event terakhir
hypo = np.loadtxt(path+'tomo0.reloc', usecols=(0,1,2,3))
id = np.array([int(l)-1 for l in hypo[:,0]])
hx = hypo[:,2]
hy = hypo[:,1]
hz = hypo[:,3]

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

ll = 0
for mm in id:
    x = X[mm,:]
    y = Y[mm,:]
    z = Z[mm,:]

    x = np.delete(x, np.where(x==9999))
    y = np.delete(y, np.where(y==9999))
    z = np.delete(z, np.where(z==9999))


    cov = np.cov(x,z)
    lambda_, v = np.linalg.eig(cov)
    lambdaz1 = np.sqrt(lambda_)

    cov = np.cov(y,z)
    lambda_, v = np.linalg.eig(cov)
    lambdaz2 = np.sqrt(lambda_)

    cov = np.cov(x,y)
    lambda_, v = np.linalg.eig(cov)
    lambda2 = np.sqrt(lambda_)
    theta =np.rad2deg(np.arccos(v[0, 0]))

    tempx = lambda2[0] * 111.11
    tempy = lambda2[1] * 111.11
    tempz = (lambdaz1[1] + lambdaz2[1])*0.5

    relative_error.write(str(tempx)+'\t'+str(tempy)+'\t'+str(tempz)+'\n')

    ell = Ellipse(xy=(np.mean(x), np.mean(y)),
                    width=lambda2[0]*2*2, height=lambda2[1]*2*2,
                    angle=theta)

    ell.set_facecolor('none')
    ell.set_edgecolor('k')
    ell.set_linewidth(0.5)
    ax.add_artist(ell)
    ax.scatter(np.mean(x), np.mean(y), 0.5, edgecolors="blue", facecolor=None)


    #print(np.mean(x), np.mean(y),tempx,tempy,theta)
    # lebar=lambda2[0]*1.96*2*111.11
    # tinggi=lambda2[1]*1.96*2*111.11
    #print(np.mean(x), np.mean(y),lebar,tinggi)

    ll += 1


relative_error.close()

ax.set_xlabel('Lon.[$^o$]')
ax.set_ylabel('Lat.[$^o$]')
#tentukan batas koordinat peta
lon_min=118.0
lon_max=127.0
lat_min=-7
lat_max=5
interval=1
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
m = Basemap(llcrnrlat=lat_min,urcrnrlat=lat_max,\
            llcrnrlon=lon_min,urcrnrlon=lon_max,lat_ts=interval,resolution='h', ax=ax)
m.drawcoastlines(linewidth=0.5)
m.fillcontinents(color='lightgray',lake_color='white')
m.drawmapboundary(fill_color='white')
m.drawparallels(np.arange(lat_min,lat_max ,interval),labels=[1,0,0,0], linewidth=0.0)
m.drawmeridians(np.arange(lon_min,lon_max ,interval),labels=[0,0,0,1], linewidth=0.0)
# fig.savefig(path+'output/Top_View_bootstrap1.png', dpi=300, bbox_inches='tight')
# fig.savefig('output/Top_View_bootstrap1.eps', dpi=2000, bbox_inches='tight')

plt.show()