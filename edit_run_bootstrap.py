import os
import numpy as np
import time

# manipulating earthquake data in ph2dt
fname1 = '/home/bagus/tomo/bootstrap-sulawesi/ph2dt/src/phase_sul5.dat'
data1 = open(fname1)
with open(fname1) as f1:
    content1 = f1.read().splitlines()

firstLine1 = data1.readlines()
for i in range(len(firstLine1)):
	firstLine1[i]=firstLine1[i].split()
data1.close()

# manipulating earthquake data in tomoDD
fname2 = '/home/bagus/tomo/bootstrap-sulawesi/ph2dt/src/absolute.dat'
data2 = open(fname2)
with open(fname2) as f2:
    content2 = f2.read().splitlines()

firstLine2 = data2.readlines()
for i in range(len(firstLine2)):
    firstLine2[i]=firstLine2[i].split()
data2.close()

#standard deviation of pick-time in seconds
std = 0.001

# number of realization
N = 2

for nn in range(N):
    #write DATA
    ph2dt = open('/home/bagus/tomo/bootstrap-sulawesi/ph2dt/src/phase_sul5'+str(nn)+'.dat', 'w+')
    tomodd = open('/home/bagus/tomo/bootstrap-sulawesi/ph2dt/src/absolute'+str(nn)+'.dat', 'w+')
    # hypodd.write(content[0]+'\n')
    j = 1
    while j < len(content1)-1:
        ph2dt.write(content1[j - 1]+'\n')
        tomodd.write(content2[j - 1]+'\n')
        i = 0
        while firstLine1[j][0] != '#':
            i += 1
            j += 1
            if j == len(content1):
                break
        j += 1

        # Generating random number with normal distribution
        rand = np.random.normal(loc = 0, scale = std, size = i)

        k = j-i-1
        count = np.arange(k, j - 1, 1)
        r = 0
        for m in count:
            tp = np.round(float(firstLine1[m][1]) - rand[r], decimals=5)
            ph2dt.write('%5s'%firstLine1[m][0]+' '+'%12s'%str(tp)+' '+'%8s'%firstLine1[m][2]+' '+'%4s'%firstLine1[m][3]+'\n')
            tomodd.write('%5s'%firstLine1[m][0]+' '+'%12s'%str(tp)+' '+'%8s'%firstLine1[m][2]+' '+'%4s'%firstLine1[m][3]+'\n')
            r += 1

    ph2dt.close()
    tomodd.close()

    time.sleep(2)
    # modify and run ph2dt
    print('===================================')
    print('===================================')
    print('=========Now running ph2dt=========')
    print('===================================')
    print('===================================')
    with open('/home/bagus/tomo/bootstrap-sulawesi/ph2dt/src/ph2dt.inp', 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    # now change the line
    data[4] = '/home/bagus/tomo/bootstrap-sulawesi/ph2dt/src/phase_sul5'+str(nn)+'.dat\n'

    # and write everything back
    with open('ph2dt.inp', 'w') as file:
        file.writelines( data )
    cmd = '/home/bagus/tomo/bootstrap-sulawesi/ph2dt/src/ph2dtN3 ph2dt.inp'
    os.system(cmd)

    time.sleep(3)
    os.rename('dt.ct', 'dt'+str(nn)+'.ct')
    os.rename('absolute.dat', 'absolute'+str(nn)+'.dat')
    os.rename('event.dat', 'event'+str(nn)+'.dat')
    
    # Add 0 to event.dat
    # event_n = 'event.dat'
    # data_n = open(event_n)
    # with open(data_n, 'w') as f_n:
    #     content_n = f_n.read()
        

        
    time.sleep(2)
    
    print('===================================')
    print('===================================')
    print('=========Now running tomoDD========')
    print('===================================')
    print('===================================')

    with open('/home/bagus/tomo/bootstrap-sulawesi/tomoSPDR/tomoDD-SE.inp', 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    # now change the line
    data[19] = '/home/bagus/tomo/bootstrap-sulawesi/tomoSPDR/Output_Files/tomo'+str(nn)+'.reloc\n'

 	# now change the line
    data[8] = '/home/bagus/tomo/bootstrap-sulawesi/ph2dt/src/absolute'+str(nn)+'.dat\n'

    # and write everything back
    with open('/home/bagus/tomo/bootstrap-sulawesi/tomoSPDR/tomoDD-SE.inp', 'w') as file:
        file.writelines( data )
		
    cmd = '/home/bagus/tomo/bootstrap-sulawesi/tomoSPDR/tomoDD-SE tomoDD-SE.inp'
    os.system(cmd)
    time.sleep(1)