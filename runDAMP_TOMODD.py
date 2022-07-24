'''
Coding: PYTHON UTF-8
Created On: 2022-07-22 15:03:39
Author: Putu Hendra Widyadharma
=== autorun for tomodd with damping edit 
'''
import os
import numpy as np
import time

path = "D:\\BMKG Putu\\Tomography\\210722\\tomodd-running-test\\"
cmd = '/home/bagus/tomo/bootstrap-sulawesi/tomoSPDR/tomoDD-SE tomoDD-SE.inp'
damp=[1,2,3,4,500,600,700,1000]

print("=== now on {} ".format(os.getcwd()))
print("=== total iteration: {} \n=== damping value: {} ".format(len(damp),damp))
print("=========================")
for i in range(len(damp)):
    print("=== run iteration {} ".format(i+1))
    f = open(path+"hypoDD.inp", "w+")
    f.write('''\
* RELOC.INP:
*--- input file selection
* cross correlation diff times:\n
*
*catalog P diff times:
dt.ct
*
* event file:
event.dat
*
* station file:
stasiunjailolo.dat
*
*--- output file selection
* original locations:
hypoDD.loc
* relocations:
hypoDD.reloc
* station information:
hypoDD.sta
* residual information:
hypoDD.res
* source paramater information:
*hypoDD.src\n
*
*--- data type selection: 
* IDAT:  0 = synthetics; 1= cross corr; 2= catalog; 3= cross & cat 
* IPHA: 1= P; 2= S; 3= P&S
* DIST:max dist [km] between cluster centroid and station 
* IDAT   IPHA   DIST
    2     3      120
*
*--- event clustering:
* OBSCC:    min # of obs/pair for crosstime data (0= no clustering)
* OBSCT:    min # of obs/pair for network data (0= no clustering)
* OBSCC  OBSCT    
     0     4        
*
*--- solution control:
* ISTART:  	1 = from single source; 2 = from network sources
* ISOLV:	1 = SVD, 2=lsqr
* NSET:      	number of sets of iteration with specifications following
*  ISTART  ISOLV  NSET
    2        2      3 
*
*--- data weighting and re-weighting: 
* NITER: 		last iteration to used the following weights
* WTCCP, WTCCS:		weight cross P, S 
* WTCTP, WTCTS:		weight catalog P, S 
* WRCC, WRCT:		residual threshold in sec for cross, catalog data 
* WDCC, WDCT:  		max dist [km] between cross, catalog linked pairs
* DAMP:    		damping (for lsqr only) 
*       ---  CROSS DATA ----- ----CATALOG DATA ----
* NITER WTCCP WTCCS WRCC WDCC WTCTP WTCTS WRCT WDCT DAMP
  3     -9     -9   -9   -9    1    1      3   50   {0}
  3     -9     -9   -9   -9    1    1      3   50   {0}
  3     -9     -9   -9   -9    1    1      3   50   {0}
* 4     -9     -9   -9   -9    1    1      3   50   {0}
*
*--- 1D model:
* NLAY:		number of model layers  
* RATIO:	vp/vs ratio 
* TOP:		depths of top of layer (km) 
* VEL: 		layer velocities (km/s)
* NLAY  RATIO 
   6     1.73
* VEL
5 10 15 25 35 45 60 100 160 210 360 460
* TOP
5.00 6.00 6.75 7.11 7.24 7.37 7.60 7.95 8.17 8.30 8.80 9.52
*
*--- event selection:
* CID: 	cluster to be relocated (0 = all)
* ID:	cuspids of event to be relocated (8 per line)
* CID    
    1     
* ID
'''.format(damp[i]))
    f.close()

    #running hypoDD
    print("=== now running hypodd ")
    # os.system(cmd)
    time.sleep(10)

    #backup output files
    print("=== backup files start ")
    os.system("copy hypoDD.inp hypoDD_run{0}.inp".format(i+1))
    print("hypoDD.inp to hypoDD_run{0}.inp".format(i+1))
    os.system("copy hypoDD.reloc hypoDD_run{0}.reloc".format(i+1))
    print("hypoDD.reloc to hypoDD_run{0}.reloc".format(i+1))
    os.system("copy hypoDD.sta hypoDD_run{0}.sta".format(i+1))
    print("hypoDD.sta to hypoDD_run{0}.sta".format(i+1))
    os.system("copy hypoDD.res hypoDD_run{0}.res".format(i+1))
    print("hypoDD.res to hypoDD_run{0}.res".format(i+1))
    os.system("copy hypoDD.src hypoDD_run{0}.src".format(i+1))
    print("hypoDD.src to hypoDD_run{0}.src".format(i+1))
    print("=== backup finish ")
    print("=== interation {} finish ".format(i+1))
    print("=========================")
    
print("=== running finish!")