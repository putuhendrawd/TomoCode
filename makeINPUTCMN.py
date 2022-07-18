'''
Coding: PYTHON UTF-8
Created On: 2022-07-14 20:57:26
Author: Putu Hendra Widyadharma
=== make multi input cmn for iterative velest process
'''

import os
path = "E:\\My Drive\\Tomography\\140722\\testrunmakeINPUTCMN\\"
fout = open(path+"velest.cmn",'w')
fout.write("""******* CONTROL-FILE FOR PROGRAM  V E L E S T  (28-SEPT1993) *******
***
*** ( all lines starting with  *  are ignored! )
*** ( where no filename is specified,\ 
***   leave the line BLANK. Do NOT delete!)
***
*** next line contains a title (printed on output):
CALAVERAS area7 1.10.93 EK startmodell vers. 1.1  
***      starting model 1.1 based on Castillo and Ellsworth 1993, JGR
***  olat       olon   icoordsystem      zshift   itrial ztrial    ised
   18.70      96.05    0             0.000      0     0.00       0
***
*** neqs   nshot   rotate
    20      0      0.0
***
*** isingle   iresolcalc
       0          0
***
*** dmax    itopo    zmin     veladj    zadj   lowveloclay
    10000.0       0      0.0        0.2      5.0       0
***
*** nsp    swtfac   vpvs       nmod
     2      0.5       1.770       1
***
*** othet   xythet    zthet    vthet   stathet
     0.01     0.01       0.01         1.0     0.1
***
*** nsinv   nshcor   nshfix     iuseelev    iusestacorr
       0       0       0           1            1
**
*** iturbo    icnvout   istaout   ismpout
       1         1         1         0
***
*** irayout   idrvout   ialeout   idspout   irflout   irfrout   iresout
       0         0         0         0         0         0         0
***
*** delmin   ittmax   invertratio
    0.01     9         1
***
*** Modelfile:
input.mod
***
*** Stationfile:
station-indoburma.sta
***
*** Seismofile:
                                                                                
***
*** File with region names:

***
*** File with region coordinates:

***
*** File #1 with topo data:
                                                                                
***
*** File #2 with topo data:
                                                                                
***
*** DATA INPUT files:
***
*** File with Earthquake data:
indoburmaehb.cnv
***
*** File with Shot data:
                                                                                
***
*** OUTPUT files:
***
*** Main print output file:
VELEST_OUT5.OUT
***
*** File with single event locations:

***
*** File with final hypocenters in *.cnv format:
VELEST_HYPO_OUT5.CNV
***
*** File with new station corrections:
VELEST_STATION_OUT5.STA
***
*** File with summary cards (e.g. for plotting):

***
*** File with raypoints:

***
*** File with derivatives:

***
*** File with ALEs:

***
*** File with Dirichlet spreads:

***
*** File with reflection points:

***
*** File with refraction points:

***
*** File with residuals:

***
******* END OF THE CONTROL-FILE FOR PROGRAM  V E L E S T  *******
""")
fout.close()