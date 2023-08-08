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
min_lon, max_lon = 118,127
min_lat, max_lat = -7,5
# end of configuration

# searching data in folder
files = glob.glob(path+'*.reloc')
files = Tcl().call('lsort', '-dict', files)
print(f'found {len(files)} file(s)')
# end of searching data in folder

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