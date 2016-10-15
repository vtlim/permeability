#!/usr/bin/env python

# Purpose: generate WHAM input file for use in Grossfield WHAM.
# Usage: python file.py

import os
import glob


# ==================================================

### Parameters from US simulations
winstart = 0
winend = 52
minZ = -8.0
maxZ = 44.0
spring = 1.5

### How much of the data to use
startns = 8
stopns = 12

### WHAM parameters
numbins = 180
tolerance = 0.0001
temp = 308.0
padding = 0

### Output file names
wham = "WHAM-INPUT_%d-%dns" % (startns, stopns)
pmf = "US_%d-%dns.pmf" % (startns, stopns)

os.chdir('/pub/limvt/pmf/07_us/02_analysis/trajfiles')

# ==================================================

time1 = 1000*startns
time2 = 1000*stopns+1

### open and read traj files 
for f in glob.glob('win*traj'):
    inf = open(f, 'r')
    lines = inf.readlines()
    inf.close()

    ### write out subset of each traj file    
    trajout = "%d-%dns_%s.traj" % (startns, stopns, f.split('.')[0])
    if not os.path.exists(trajout):
        outf = open(trajout, 'w')
        subset = lines[time1:time2]
        for i in subset:
            outf.write(str(i))
        outf.close()

### open and write WHAM input file header
### if error of whamf not defined, delete the old input file and try script again
if not os.path.exists(os.path.join('../03_wham',wham)):
    whamf = open(os.path.join('../03_wham',wham), 'w')
whamf.write("### wham %f %f %d %f %f %f %s %s" % (minZ, maxZ, numbins, tolerance, temp, padding, wham, pmf))
whamf.write("\n### /path/to/timeseries/file loc_win_min spring [correl time] [temp]")
whamf.write("\n###")

i = winstart
while i <= winend:
    ### set values for window number and wtt center
    if i < maxZ and i < 10:
        win = '0'+str(i)
        cent = str(i)
    elif i <= maxZ and i >= 10:
        win = str(i)
        cent = str(i)
    else:
        win = str(i)
        cent = str(maxZ-i)

    ### don't write to WHAM if the window didn't finish
    trajout = '%d-%dns_win%s.traj' % (startns, stopns, win)
    print trajout
    if not os.path.exists(trajout):
        print "No *.traj output for WHAM for %s" % (trajout)
        i += 1
        continue

    whamf.write("\n../trajfiles/%s %s %f" % (trajout, cent, spring))
    i += 1
whamf.close()
