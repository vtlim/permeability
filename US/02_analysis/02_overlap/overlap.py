#!/usr/bin/env python

# Purpose: Plot histograms of all umbrella sampling windows altogether; 
#    they should overlap.
# Usage: python file.py

import os
import numpy as np
import matplotlib.pyplot as p

# -------------------- Variables ------------------ #

os.chdir("/pub/limvt/pmf/07_us/02_analysis/trajfiles")

numWins = 53 # total number of US windows
eqt = 8000  # equil time to discard. 1000 = 1 ns

# ------------------------------------------------- #

data = []
for i in range(numWins):
    if i < 10:
        index = "0"+str(i)
    else:
        index = str(i)
    tfile = "win"+index+".traj"
    print tfile

    if not os.path.isfile(tfile):
        continue

    with open(tfile) as f:
        lines = f.readlines()[eqt:]

        zlist = []
        for line in lines:
            parts = line.split() # split line into parts
            if len(parts) > 1:   # if at least 2 parts/columns
                zlist.append(float(parts[1]))   # print column 2
    data.append(zlist)
    
print len(data)
print len(zlist)


p.figure(figsize=(20,8))
for i, zlist in enumerate(data):
    y,binEdges = np.histogram(zlist,bins=100)
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    p.plot(bincenters,y,'-')
p.tick_params(axis='both', which='major', labelsize=14)
p.xlabel("z coordinate ($\AA$)",fontsize=16)
p.ylabel("count",fontsize=16)

p.savefig(os.path.join("/pub/limvt/pmf/07_us/02_analysis/02_overlap","overlap.png"))
p.show()
