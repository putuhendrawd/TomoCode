import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits.basemap import Basemap
import pygmt

path = "G:\\My Drive\\Tomography\\140823\\btstrp-sul-13042023-11082023\\"
N = 50 #Number of Realization/Jumlah bootstrap sample
M = 10421 #>=ID event terakhir/Jumlah event
hypo = np.loadtxt(path+'tomo0.reloc', usecols=(0,1,2,3))
id = np.array([int(l)-1 for l in hypo[:,0]])
hx = hypo[:,2]
hy = hypo[:,1]
hz = hypo[:,3]

# init map parameter
lon_min=118
lon_max=127
lat_min=-7
lat_max=3
interval=2
dep_min=0
dep_max=750

# initialize projection
proj = pygmt.project(center=f'{lon_min}/{lat_min+(lat_max-lat_min)/2}',
                     endpoint=f'{lon_max}/{lat_min+(lat_max-lat_min)/2}',
                     unit=True,
                     generate='0.1')
lon_length_max = round(proj.p.max())

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
fig = plt.gcf()
ax = fig.add_subplot(111, aspect='auto')
ax.set_xlim(0, lon_length_max)
ax.set_ylim(dep_min, dep_max)

ll = 0
for mm in id:
    try:
        x = X[mm,:]
        y = Y[mm,:]
        z = Z[mm,:]

        x = np.delete(x, np.where(x==9999))
        y = np.delete(y, np.where(y==9999))
        z = np.delete(z, np.where(z==9999))

        con = np.column_stack((x,y,z))
        proj = pygmt.project(data=con,
                            center=f'{lon_min}/{lat_min+(lat_max-lat_min)/2}',
                            endpoint=f'{lon_max}/{lat_min+(lat_max-lat_min)/2}',
                            unit=True,
                            length='w',
                            convention='p')
        x_proj = proj.to_numpy().flatten()
        
        proj = pygmt.project(data=con,
                            center=f'{lon_min+(lon_max-lon_min)/2}/{lat_min}',
                            endpoint=f'{lon_min+(lon_max-lon_min)/2}/{lat_max}',
                            unit=True,
                            length='w',
                            convention='p')
        y_proj = proj.to_numpy().flatten()

        cov = np.cov(x_proj,y_proj)
        lambda_, v = np.linalg.eig(cov)
        lambda2 = np.sqrt(lambda_)
        lambda2[np.isnan(lambda2)] = 0

        cov = np.cov(y_proj,z)
        lambda_, v = np.linalg.eig(cov)
        lambdaz2 = np.sqrt(lambda_)
        lambdaz2[np.isnan(lambdaz2)] = 0
        theta=np.rad2deg(np.arccos(v[0, 0]))

        cov = np.cov(x_proj,z)
        lambda_, v = np.linalg.eig(cov)
        lambdaz1 = np.sqrt(lambda_)
        lambdaz1[np.isnan(lambdaz1)] = 0

        tempx = lambda2[0]
        tempy = lambda2[1]
        tempz = (lambdaz1[1] + lambdaz2[1])*0.5
    
        # ax.scatter(np.mean(x), np.mean(z), 0.1, 'r')
        ell = Ellipse(xy=(np.mean(x_proj), np.mean(z)),
                        width=lambda2[1]*1.96*2, height=tempz*1.96*2,
                        angle=np.rad2deg(np.arccos(v[0, 0])))
    
        ell.set_facecolor('none')
        ell.set_edgecolor('b')
        ell.set_linewidth(1)
        ax.add_artist(ell)
    except:
        pass
    # cov = np.cov(y,z/111.11)
    # lambda_, v = np.linalg.eig(cov)
    # lambdaz1 = np.sqrt(lambda_)
    # theta=np.rad2deg(np.arccos(v[0, 0]))

    ll += 1


ax.set_xlabel('Distance [Km]')
ax.set_ylabel('Depth [Km]')
ax.invert_yaxis()
fig.set_size_inches((10, 5), forward=False)
fig.savefig(path+'output/MapView_bootstrap1_EW_kmkm.png', dpi=500)
# fig.savefig(path+'output/MapView_bootstrap1_EW.eps', dpi=500)

plt.show()
