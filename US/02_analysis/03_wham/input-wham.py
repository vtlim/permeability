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
usePortion=True
startns = 30
stopns = 40
shortprefix = '20-30ns'

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

time1 = 1000*startns/2
time2 = (1000*stopns/2)+1

### open and read traj files 
for f in glob.glob('win*traj'):
    inf = open(f, 'r')
    lines = inf.readlines()
    inf.close()

    ### write out subset of each traj file
    if usePortion: 
        trajout = "%d-%dns_%s.traj" % (startns, stopns, f.split('.')[0])
        if not os.path.exists(trajout):
            outf = open(trajout, 'w')
            subset = lines[time1:time2]
            for i in subset:
                outf.write(str(i))
            outf.close()

### open and write WHAM input file header
fname = os.path.join('../03_wham',wham)
if not os.path.exists(fname):
    whamf = open(fname, 'w')
else:
    print("WHAM input file already exists: %s" % fname)
    quit()
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

    if usePortion:
        trajout = '%d-%dns_win%s.traj' % (startns, stopns, win)

        ### use prespecified files for some windows that ran for less time
        if os.stat(trajout).st_size == 0:
            os.remove(trajout)
            trajout = '%s_win%s.traj' % (shortprefix, win)
    else:
        trajout = 'win%s.traj' % win   
    print trajout

    ### don't write to WHAM if the window didn't finish
    if not os.path.exists(trajout):
        print "No *.traj output for WHAM for %s" % (trajout)
        i += 1
        continue

    whamf.write("\n../trajfiles/%s %s %f" % (trajout, cent, spring))
    i += 1
whamf.close()
