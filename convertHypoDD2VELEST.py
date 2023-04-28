# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:24:14 2022
Program for Converting Eq. Parameter & Phase Data 
from HypoDD to Velest Format
@author: Nova Heryandoko
"""


import glob
from pathlib import Path

## RECTANGLE AREA
#minlon = 100.
#maxlon = 145.
#minlat = -12.
#maxlat = 3

#### SET THE FOLDER FOR WRITING OUTPUT FILES ################
outdir = 'G:\\My Drive\\Tomography\\280423\\'

#### SEARCH INPUT FILE FOR GIVEN FOLDER PATH ################
sfiles = [outdir+'phase_sul_2022_6P_150-10D_PnS.dat']

#### READ EACH FILE #########################################
first = True
for sfile in sfiles:
    fin = open(sfile,'r')
#    print('Read Data from File:',sfile)
    baris = fin.readlines()
    outfile = outdir+'/{0:s}.cnv'.format(Path(sfile).stem)
    fout = open(outfile,'w')
    for i in range(len(baris)):
        spl = baris[i].split()
#        print('BARIS :',spl)
        if spl and len(spl) > 1:
            if spl[0] == '#':
                if first:
                    fout.write("\n")
                    first=False
                else:
                    fout.write("\n\n")
                
#                print(spl)
                tahun = spl[1]
                bulan =spl[2]
                tanggal = spl[3]
                jam = spl[4]
                menit = spl[5]
                detik = spl[6]
                lat = spl[7]
                lon = spl[8]
                if float(lat) < 0:
                    lat = -(float(lat))
                    lat_id = 'S'
                else:
                    lat_id = 'N'
                if float(lon) < 0:
                    lon = -(float(lon))
                    lon_id = 'W'
                else:
                    lon_id = 'E'
                dep = spl[9]
                mag = spl[10]
                
                print(tahun,bulan,tanggal,jam,menit,detik)
                fout.write("{0}{1:0>2}{2:0>2} {3:0>2}{4:0>2} {5:0>5}"\
                        .format(tahun[2:4],bulan,tanggal,jam,menit\
                        ,detik)+'%8.4f%s%9.4f%s%8.2f%7.2f%7s\n'%(float(lat),lat_id\
                        ,float(lon),lon_id,float(dep),float(mag),'0'))
            else:                
                
                stacode_i = spl[0]
                s = len(stacode_i)
                #print('STA CODE LENGTH :', s, stacode_i)
                if s > 4:
                    stacode = stacode_i[:4]
                elif s < 4:
                    stacode = "{0:>4}".format(stacode_i)
                else:
                    stacode = stacode_i
                   
                time_i = spl[1]
                if float(time_i) <= 200.:
                    time = time_i
                else:
                    continue
                flag = int(float(spl[2]))
                pha = spl[3]
                fout.write('%s%s%s%6s'%(stacode,pha,flag,time))
fin.close()
fout.close()