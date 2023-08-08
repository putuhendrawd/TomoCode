'''
Coding: PYTHON UTF-8
Created On: 2023-08-07 14:49:35
Author: Putu Hendra Widyadharma
=== pre-processing data .reloc 
=== include converting .reloc to have same event ID and event NUMBER 
'''

import numpy as np
import pandas as pd
import glob
from pathlib import Path
from tkinter import Tcl
import logging as log
import argparse
import os


# configuration 
path = 'G:\\My Drive\\Tomography\\040823\\bootstrp-result-sul-13042023-04082023\\'
# end of configuration

# argument parser
# parser = argparse.ArgumentParser()
# parser.add_argument('-v','--verbosity', action='count')
# end of argument parser

# verbose settings
# print(parser)
# end of verbose settings

# searching data in folder
files = glob.glob(path+'*.reloc')
files = Tcl().call('lsort', '-dict', files)
print(f'found {len(files)} file(s)')
# end of searching data in folder

# create output folder
if not os.path.exists(path+'/output'):
    output_path = path+'/output/'
    os.makedirs(path+'/output')
    print(f'output folder created')
else:
    output_path = path+'/output/'
    print(f'warning, output folder exist!')
# end of create output

# check last event number in all files
for i, file in enumerate(files):
    if (i != 0) and (int(np.loadtxt(file,usecols=(0))[-1]) > last_event_num):
        last_event_num = int(np.loadtxt(file,usecols=(0))[-1])
        last_event_num_file = Path(file).name
    else:
        last_event_num = int(np.loadtxt(file,usecols=(0))[-1])
        last_event_num_file = Path(file).name
print(f'maximum event number of {last_event_num} found in {last_event_num_file}')
# end of event number checker

# check event appearance in every reloc data
for i, file in enumerate(files):
    file_load = np.loadtxt(file, usecols=(0))
    if (i != 0):
        appearance_arr = np.vstack((appearance_arr, np.in1d(appearance_arr[0],file_load)))
    else:
        appearance_arr = np.array([x+1 for x in range(last_event_num)])
        appearance_arr = np.vstack((appearance_arr, np.in1d(appearance_arr,file_load)))
df_appearance = pd.DataFrame(appearance_arr.T)
deleted_event_list = df_appearance[(df_appearance.values == 0).any(axis=1)][0].values.tolist()
print(f'total event to delete: {len(deleted_event_list)}')
print(deleted_event_list)
# end of appearance checker 


# data cleaning and output
for i, file in enumerate(files):
    df = pd.read_csv(file, delim_whitespace=True, header=None)
    df = df[~df[0].isin(deleted_event_list)]
    df.to_csv(output_path+Path(file).stem+'_p.reloc',sep='\t',header=None, index=None)
    print(f'success convert {Path(file).name}')
# end of data cleaning and output

print(f'program convert finish')
# # check the shortest file length
# for i,file in enumerate(files):
#     with open(file, 'r') as f:
#         lines = len(f.readlines())
#         if i == 0:
#             min_length = lines
#             min_length_file = Path(file).name
#         else:
#             if lines < min_length:
#                 min_length = lines
#                 min_length_file = Path(file).name
#             else:
#                 pass
# print(f'minimum file length of {min_length} in {min_length_file} found')

# # filter all data by using shortest file
# # read the shortest file
# base_file = np.loadtxt(path+min_length_file, usecols=(0,1,2,3))