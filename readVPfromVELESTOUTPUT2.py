'''
Coding: PYTHON UTF-8
Created On: 2022-07-13 21:29:05
Author: Putu Hendra Widyadharma
=== reading velest output .OUT
'''
import pandas as pd
from pathlib import Path
from localfunction import *

path = "G:\\My Drive\\Tomography\\120523\\velest-sum-110523\\"
fname = "model_sum_arrivals_sum_8P_wadatifilter_8P_150-10D_10PnS_110523.OUT"

# init
depth = []
initial_vp = []
initial_vs = []
residual = []
read_init_vp = False
read_init_vs = False
read_vp=False
read_vs=False
adjustment=False
count = 0
count2 = 0
count3 = 0
result_vp = pd.DataFrame([],columns=["depth","init"])
result_vs = pd.DataFrame([],columns=["depth","init"])

# define function float searcher
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# read
print(f"========== Start Reading {fname} ==========\n")
fin = open(path+fname)
readl = fin.readlines()

for i in readl:
    spl=i.split()
    # print(spl)
    # cari data model awal 
    if "velocity structure for model" in " ".join(spl).lower():
        if spl[4] == '1':
            read_init_vp = True
            print(f"## READING INITIAL DATA VP")
            # print(f'== step 1 read init\nread_init_vp = {read_init_vp}\nread_init_vs = {read_init_vs}')
        elif spl[4] == '2':
            read_init_vp = False
            read_init_vs = True
            print(f"## READING INITIAL DATA VS")
            # print(f'== step 2 read init\nread_init_vp = {read_init_vp}\nread_init_vs = {read_init_vs}')
        else:
            pass
    if len(spl)>0 and spl[0].isnumeric() and read_init_vp:
        depth.append(float(spl[2]))
        initial_vp.append(float(spl[1]))
        count+=1
    elif len(spl)>0 and spl[0].isnumeric() and read_init_vs:
        if count2 < count:
            initial_vs.append(float(spl[1]))
            count2+=1
        else:
            read_init_vs = False
            #save vp
            result_vp["depth"] = depth
            result_vp['init'] = initial_vp
            result_vp.set_index("depth",inplace=True)
            
            #save vs
            result_vs["depth"] = depth
            result_vs['init'] = initial_vs
            result_vs.set_index("depth",inplace=True)
            
            del count2
            # print(f'== step 3 read init\nread_init_vp = {read_init_vp}\nread_init_vs = {read_init_vs}')
            print(f"initial data stored in result_vp and result_vs")

    # cari rms residual 
    if "rms residual" in " ".join(spl).lower():
        residual.append(float(spl[-1]))
    
    # cari data dari setiap iterasi
    if "iteration no" in " ".join(spl).lower():
        iter = spl[2]
        adjustment=False
        read_vp=False
        read_vs=False
        vp_dump=[]
        vs_dump=[]
        count3=0
        print(f"## READING ITERATION {iter}")
    if "velocity adjustments:" in " ".join(spl).lower():
        # print(spl)
        adjustment=True
    if len(spl)==3 and adjustment and "velocity model" in " ".join(spl).lower():
        # print(spl)
        if spl[2] == '1':
            read_vp = True
            # print(f'== step 1 read data iteration: {iter}\nread_vp = {read_vp}\nread_vs = {read_vs}')
        elif spl[2] == '2':
            read_vp = False
            read_vs = True
            # print(f'== step 2 read data iteration: {iter}\nread_vp = {read_vp}\nread_vs = {read_vs}')
        else:
            pass
    if len(spl)>=3 and isfloat(spl[0]) and isfloat(spl[1]) and isfloat(spl[2]) and read_vp:
        vp_dump.append(spl[0])
    elif len(spl)>=3 and isfloat(spl[0]) and isfloat(spl[1]) and isfloat(spl[2]) and read_vs:
        if count3 < count:
            vs_dump.append(spl[0])
            count3+=1
    if count3==count and read_vs:
        read_vs = False
        #save vp
        result_vp[iter] = vp_dump
        #save vs
        result_vs[iter] = vs_dump
        # print(f'== step 3 read data iteration: {iter}\nread_vp = {read_vp}\nread_vs = {read_vs}')
        print(f"iteration data stored in result_vp and result_vs")
print(f"\n========== Finish Reading {fname} ==========")
fin.close()

#export
result_vp.to_csv(path+f'{Path(fname).stem}_vp.csv',index="depth")
result_vs.to_csv(path+f'{Path(fname).stem}_vs.csv',index="depth")
with open(path+f"residual {Path(fname).stem}.txt", "w") as res:
    res.write(f"{'iteration':<10} {'residuals':<10}\n")
    for i in range(count+1):
        if i ==0:
            res.write(f"{'init':<10} {residual[i]:<10}\n")
        else:
            res.write(f"{i:<10} {residual[i]:<10}\n")