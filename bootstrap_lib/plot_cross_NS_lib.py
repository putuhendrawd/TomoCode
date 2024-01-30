'''
Coding: PYTHON UTF-8
Created On: 2023-08-07 14:52:10
Author: Putu Hendra Widyadharma
=== plot bootstrap data as horizontal plot (lon,lat) with ellipse error
'''

import numpy as np
import pandas as pd
import pygmt 
import glob
from tkinter import Tcl
from pathlib import Path

# configuration 
path = 'G:\\My Drive\\Tomography\\040823\\bootstrp-result-sul-13042023-04082023\\output\\'
minlon, maxlon = 118,127
minlat, maxlat = -7,5
# minlon, maxlon = 122.02,122.05
# minlat, maxlat = 0.25,0.29
# end of configuration

# searching data in folder
files = glob.glob(path+'*.reloc')
files = Tcl().call('lsort', '-dict', files)
print(f'found {len(files)} file(s)')
# end of searching data in folder

# projection initialization
proj_lon = pygmt.project(
                     center=f'{minlon}/{minlat+(maxlat-minlat)/2}',
                     endpoint=f'{maxlon}/{minlat+(maxlat-minlat)/2}',
                     unit=True,
                     generate='0.1')
lon_length_max = round(proj_lon.p.max())

proj_lat = pygmt.project(center=f'{minlon+(maxlon-minlon)/2}/{minlat}',
                     endpoint=f'{minlon+(maxlon-minlon)/2}/{maxlat}',
                     unit=True,
                     generate='0.1')
lat_length_max = round(proj_lat.p.max())
# end of projection init

# matrix initialization 
init_ = np.loadtxt(files[0], usecols=(0,1,2,3))
X = np.zeros((len(init_),len(files)))
Y = np.zeros((len(init_),len(files)))
Z = np.zeros((len(init_),len(files)))
# end of matrix initialization 

# load matrix
for i, file in enumerate(files):
    init_ = np.loadtxt(file, usecols=(0,1,2,3))
    X[:,i] = init_[:,2]
    Y[:,i] = init_[:,1]
    Z[:,i] = init_[:,3]
# end of load matrix

# main try
# variance = open(path+'variance_data.txt', 'w+')
# variance.write('x_var [km]'+'\t'+'y_var [km]'+'\t'+'z_var [km]'+'\n')
fig = pygmt.Figure()
region = [minlon,maxlon,minlat,maxlat]
fig.basemap(region=region, frame=["WSne","xaf+lLongitude", "yaf+lLatitude","a2f2"], projection="M20c" )
fig.coast(region=region,
          projection='M20c',
          shorelines='0.5p,black'
         )


x = X[i,:]
y = Y[i,:]
z = Z[i,:]
con = np.column_stack((x,y,z))
proj_lon = pygmt.project(data=con,
                     center=f'{minlon}/{minlat+(maxlat-minlat)/2}',
                     endpoint=f'{maxlon}/{minlat+(maxlat-minlat)/2}',
                     unit=True,
                     length='w',
                     convention='pz')
x_proj = proj_lon.to_numpy()

cov = np.cov(x_proj,z)
pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
ell_radius_x = np.sqrt(1 + pearson)
ell_radius_y = np.sqrt(1 - pearson)

eig_val, eig_vec = np.linalg.eig(cov)
eig_val_sqrt = np.sqrt(eig_val)
theta =np.rad2deg(np.arccos(eig_vec[0, 0]))

# plot
# fig.plot(x=x.tolist(),y=y.tolist(),fill='red',style="c0.2c", pen="1p,black")
fig.plot(x=x.mean(), y=y.mean(), style=f"E{45}/{2*ell_radius_x}/{2*ell_radius_y}", fill=None, pen="0.2p,darkblue")
# end of main try

# # main
# variance = open(path+'variance_data.txt', 'w+')
# variance.write('x_var [km]'+'\t'+'y_var [km]'+'\t'+'z_var [km]'+'\n')
# fig = pygmt.Figure()
# region = [minlon,maxlon,minlat,maxlat]
# fig.basemap(region=region, frame=["WSne","xaf+lLongitude", "yaf+lLatitude","a2f2"], projection="M20c" )
# fig.coast(region=region,
#           projection='M20c',
#           shorelines='0.5p,black'
#          )

# for i in range(len(X)):
#     x = X[i,:]
#     y = Y[i,:]
#     z = Z[i,:]

#     # see x
#     # https://carstenschelp.github.io/2018/09/14/Plot_Confidence_Ellipse_001.html
#     # https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html
#     # basis code of drawing ellipse error

#     cov = np.cov(x,y)
#     pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
#     ell_radius_x = np.sqrt(1 + pearson)
#     ell_radius_y = np.sqrt(1 - pearson)

#     eig_val, eig_vec = np.linalg.eig(cov)
#     eig_val_sqrt = np.sqrt(eig_val)
#     theta =np.rad2deg(np.arccos(eig_vec[0, 0]))
    
#     # variance plot
#     variance.write(str(np.var(x*111.11))+'\t'+str(np.var(y*111.11))+'\t'+str(np.var(z*111.11))+'\n')

#     # plot
#     # fig.plot(x=x.tolist(),y=y.tolist(),fill='red',style="c0.2c", pen="1p,black")
#     fig.plot(x=x.mean(), y=y.mean(), style=f"E{45}/{2*ell_radius_x}/{2*ell_radius_y}", fill=None, pen="0.2p,darkblue")

# fig.show()
# fig.savefig(fname=f'{path}horizontal_output.png', dpi=1200)
# # end of main