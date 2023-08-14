import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits.basemap import Basemap

path = "G:\\My Drive\\Tomography\\080823\\btstrp-sul-13042023-08082023\\"
N = 50 #Number of Realization/Jumlah bootstrap sample
M = 10421 #>=ID event terakhir/Jumlah event
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
#tentukan batas koordinat peta
lon_min=118
lon_max=127
lat_min=-7
lat_max=3
interval=2
dep_min=0
dep_max=750
fig = plt.gcf()
ax = fig.add_subplot(111, aspect='auto')
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(dep_min, dep_max)

ll = 0
for mm in id:
    x = X[mm,:]
    y = Y[mm,:]
    z = Z[mm,:]

    x = np.delete(x, np.where(x==9999))
    y = np.delete(y, np.where(y==9999))
    z = np.delete(z, np.where(z==9999))


    cov = np.cov(x,y)
    lambda_, v = np.linalg.eig(cov)
    lambda2 = np.sqrt(lambda_)


    cov = np.cov(y,z)
    lambda_, v = np.linalg.eig(cov)
    lambdaz2 = np.sqrt(lambda_)
    theta=np.rad2deg(np.arccos(v[0, 0]))

    cov = np.cov(x,z)
    lambda_, v = np.linalg.eig(cov)
    lambdaz1 = np.sqrt(lambda_)


    tempx = lambda2[0] * 111.11
    tempy = lambda2[1] * 111.11
    tempz = (lambdaz1[1] + lambdaz2[1])*0.5
 
    # ax.scatter(np.mean(x), np.mean(z), 0.1, 'r')
    ell = Ellipse(xy=(np.mean(x), np.mean(z)),
                      width=lambda2[1]*1.96*2, height=tempz*1.96*2,
                      angle=np.rad2deg(np.arccos(v[0, 0])))
  
    ell.set_facecolor('none')
    ell.set_edgecolor('b')
    ell.set_linewidth(1)
    ax.add_artist(ell)

    # cov = np.cov(y,z/111.11)
    # lambda_, v = np.linalg.eig(cov)
    # lambdaz1 = np.sqrt(lambda_)
    # theta=np.rad2deg(np.arccos(v[0, 0]))

    ll += 1


ax.set_xlabel('Longitude [$^o$]')
ax.set_ylabel('Depth [Km]')
ax.invert_yaxis()
fig.set_size_inches((10, 5), forward=False)
fig.savefig(path+'output/MapView_bootstrap1_EW.png', dpi=500)
# fig.savefig(path+'output/MapView_bootstrap1_EW.eps', dpi=500)

plt.show()
