'''
Coding: PYTHON UTF-8
Created On: 2022-07-22 15:03:39
Author: Putu Hendra Widyadharma
=== autorun for tomodd with damping edit 
'''
import os
import time

path = os.getcwd()
cmd = './tomoDD-SE tomoDD-SE.inp'
damp=[10,20,40,70,100,150,200,300,500]
 
print("=== now on {} ".format(os.getcwd()))
print("=== total iteration: {} \n=== damping value: {} ".format(len(damp),damp))
print("=========================")
for i in range(len(damp)):
    print("=== run iteration {} ".format(i+1))
    if not os.path.exists(path+"/Output_Files"):
        os.mkdir(path+"/Output_Files")
    f = open(path+"/tomoDD-SE.inp", "w+")
    f.write('''\
* RELOC.INP:
*--- input file selection
* cross correlation diff times:
*Input_Files/dt.cc

*
*catalog P diff times:
Input_Files/dt.ct
*
* event file:
Input_Files/event.dat
*
* station file:
Input_Files/station.dat
*
*--- output file selection
* original locations:
Output_Files/tomoDD.loc
* relocations:
Output_Files/tomoDD.reloc
* station information:
Output_Files/tomoDD.sta
* residual information:
Output_Files/tomoDD.res
* source paramater information:

* Velocity file
Output_Files/tomoDD.vel
* Vp Model
Output_Files/Vp_model.dat
* Vs Model
Output_Files/Vs_model.dat
* Absolute file
Input_Files/absolute.dat
*
*--- data type selection: 
* IDAT:  0 = sichuannthetics; 1= cross corr; 2= catalog; 3= cross & cat 
* IPHA: 1= P; 2= S; 3= P&S
* DIST:max dist [km] between cluster centroid and station 
* IDAT   IPHA   DIST
   2      3     10000
*
*--- event clustering:
* OBSCC:    min # of obs/pair for crosstime data (0= no clustering)
* OBSCT:    min # of obs/pair for network data (0= no clustering)
* OBSCC  OBSCT   Air_dep 
    0      0      -5 
*
*--- solution control:
* ISTART:  	1 = from single source; 2 = from network sources
* ISOLV:	1 = SVD, 2=lsqr
* NSET:      	number of sets of iteration with specifications following
* wlat,wlon:    the location (latitude and longitude) of the coordinate center 
* CC_format:    the format of dt.cc
* weight1, weight2, weight3: the smoothing parameters of the direction of longitude, latitude and depth
*
*  ISTART  ISOLV  NSET
     2       2      10
* iuses iuseq invdel  stepl 
    2     0     0      0.45 
* wlat   wlon   rota
  -2.50   122.50   0
* weight1 weight2  weight3  CC_format
   40      40      15     1
*
*--- data weighting and re-weighting: 
* NITER: 		last iteration to used the following weights
* WTCCP, WTCCS:		weight cross P, S 
* WTCTP, WTCTS:		weight catalog P, S 
* WRCC, WRCT:		residual threshold in sec for cross, catalog data 
* WDCC, WDCT:  		max dist [km] between cross, catalog linked pairs
* DAMP:    		damping (for lsqr only) 
*       ---  CROSS DATA ----- ----CATALOG DATA ----
* NITER WTCCP WTCCS WRCC WDCC WTCTP WTCTS WRCT WDCT WTDD DAMP JOINT THRE
  2      -9    -9   -9    -9  1.0    0.8   -9   -9   10  {0}   0    0.1
  2      -9    -9   -9    -9  1.0    0.8   -9   -9   10  {0}   1    0.1
  2      -9    -9   -9    -9  0.8    0.6    6  100   10  {0}   0    0.1
  2      -9    -9   -9    -9  0.8    0.6    6  100   10  {0}   1    0.1
  2      -9    -9   -9    -9  0.6    0.4    5  100    1  {0}   0    0.1
  2      -9    -9   -9    -9  0.6    0.4    5  100    1  {0}   1    0.1
  2      -9    -9   -9    -9  0.4    0.2    5   50  0.1  {0}   0    0.1
  2      -9    -9   -9    -9  0.4    0.2    5   50  0.1  {0}   1    0.1
  2      -9    -9   -9    -9  0.2    0.1    5   50  0.01 {0}   0    0.1
  2      -9    -9   -9    -9  0.2    0.1    5   50  0.01 {0}   1    0.1
*--- even-9lection:
* CID: 	cluster to be relocated (0 = all)
* ID:	cuspids of event to be relocated (8 per line)
* CID    
    0      
* ID

'''.format(damp[i]))
    f.close()

    #running TomoDD-SE
    print("=== now running TomoDD-SE ")
    #output test
#    filesx = ["tomoDD.vel","Vp_model.dat","Vs_model.dat","tomoDD.loc",\
#        "tomoDD.reloc","tomoDD.sta","tomoDDres","tomoDD.src","tomoDD.log"]
#    for x in filesx:
#        open(path+"/Output_Files/"+x,"w+").close()
    os.system(cmd)
    time.sleep(2)

    #backup output files
    print("=== backup files start ")
    os.rename("Output_Files","Output_Files_damp_{}".format(damp[i]))
    print("output folder saved as Output_Files_damp_{}".format(damp[i]))
    print("=== backup finish ")
    print("=== interation {} finish ".format(i+1))
    print("=========================")
    
print("=== running finish!")
