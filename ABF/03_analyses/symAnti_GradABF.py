#!/usr/bin/env python

# Purpose: Symmetrize PMF from ABF simulations using .pmf and .count files from merge.
# Usage: python file.py > output
# Version: 10/07/2016
# Note: damn, looks like you computed gradients for nothing here (there is a .grad file).
#       at least they're both consistent.
# Note: seems like symmetrizing PMF gives same result as antisymmetrizing grad(PMF).

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

dataf='merge3.pmf'
countsf='merge3.count'
anti=False  # antisymmetrize
anti=True

def ReadFile(infile):
    indata = open(infile, 'r')
    lines = indata.readlines()
    indata.close()
    return lines

os.chdir('/pub/limvt/pmf/06_abf/0oldscripts/win0merge/')
#os.chdir('/home/victoria/Documents/pmf/06_abf/win0merge')


### read in data file (e.g. with pmf values). skip comment and end line.
lines = ReadFile(dataf)[1:-1]

### Allocate numpy list storage
origxs = np.zeros([len(lines)], np.float64)  # distance from memb center
origys = np.zeros([len(lines)], np.float64)  # original unsymm pmf values
gradys = np.zeros([len(lines)], np.float64)  # gradients of unsymm pmf values
finys = np.zeros([len(lines)], np.float64)   # final symmetrized pmf values
symys = np.zeros([len(lines)], np.float64)   # symmetrized pmf values
counts = np.zeros([len(lines)], np.float64)  # number of counts per distance

### Parse data file.
for i, line in enumerate(lines):
    if line.strip() != '' and line[0] != '#':
        if line.split()[0] == '0': 
            zero = i        # get position of list where zero is
        origxs[i] = float(line.split()[0]) # z coordinate
        origys[i] = float(line.split()[1]) # transmemb position
print("Midpoint %.2f is the %d element in the data list." % (origxs[zero], zero))
dist = len(origys)-zero-1   # get magnitude away from zero
print("The furthest index away from zero is %d." % dist)

### read in and parse counts file
lines = ReadFile(countsf)[3:]
for i, line in enumerate(lines):
    if line.strip() != '' and line[0] != '#':
        counts[i] = float(line.split()[1]) # counts

### Compute gradients dy/dx.
for i in range(len(origys)-1):
    gradys[i] = (origys[i+1]-origys[i])/0.1

### loop from zero to dist, symmetrizing
for i in range(dist):
    plus = zero+i
    minus = zero-i

    # use orig value at z=0 or when no other side to symmetrize
    if minus<0 or plus==minus:
        symys[i] = gradys[plus]
        continue
    try:
        if not anti: numerator = counts[plus]*gradys[plus] + counts[minus]*gradys[minus]
        if anti: numerator = counts[plus]*gradys[plus] - counts[minus]*gradys[minus]
        denom = counts[plus] + counts[minus]
        symys[i] = numerator / denom
    except IndexError:
        symys[i] = gradys[plus]

### Integrate the symmetrized gradients. Trapezoid rule.
# start from bulk water = 0. *-0.5 since going backwards.
last = 0
for i in reversed(range(len(symys)-1)):
    print i, last
    finys[i] = -0.5*0.1*(symys[i]+symys[i-1])+last
    last = finys[i]

### List cleaning. And convert x's A --> nm.
symxs = origxs[zero:-1] # 0 to 43.9
finys = finys[:dist]
symxs = 0.1*symxs
origxs = 0.1*origxs


### Write out PMF
print "\n\n# PMF (in units of nm, kcal/mol)"
for i in range(dist):
    print '\t',symxs[i], finys[i]

### Generate lists to plot both sides of symmetrized data
allx = np.zeros([2*len(symxs)-1], np.float64)  
ally = np.zeros([2*len(finys)-1], np.float64)

for i in range(len(allx)):
    if i < len(symxs)-1:
        allx[i] = -1*symxs[len(symxs)-1-i]
        ally[i] = finys[len(symxs)-1-i]
    else:
        allx[i] = symxs[i-len(symxs)+1]
        ally[i] = finys[i-len(symxs)+1]

# ===========================================
#           PLOTTING
# ===========================================

### Initialize figure.
fig = plt.figure()
ax1 = fig.add_subplot(111)

### Label the figure.
ax1.set_title('Potential of Mean Force of Water\nthrough POPC bilayer (ABF)',fontsize=20)
ax1.set_xlabel('z coordinate (nm)',fontsize=18)
ax1.set_ylabel('free energy (kcal/mol)',fontsize=19)
for xtick in ax1.get_xticklabels():
    xtick.set_fontsize(14)
for ytick in ax1.get_yticklabels():
    ytick.set_fontsize(14)


### Plot the data.
ax1.plot(allx, ally)  # for all sides
#ax1.plot(symxs, finys) # for only half
#ax1.plot(origxs[1:-1],origys[1:-1]) # for original data

### If plotting ALL, set axis limits to match ABF paper
### DOI: 10.1021/ct400925s

### set limits of the plot
axes = plt.gca()
axes.set_xlim([-3.7,3.7])
axes.set_ylim([-0.4,8.4])

### tick mark frequencies
ax1.set_yticks(np.arange(0,10,2)) # y: explicitly specify major ticks
minorLocator = AutoMinorLocator(2)
ax1.yaxis.set_minor_locator(minorLocator) # y: explicitly specify minor ticks
#ax1.xaxis.set_minor_locator(minorLocator) # has no minor ticks for negatives
ax1.set_xticks(np.arange(-3.5,4.5,1),minor=True) # x: explicitly set minor ticks

### make tick marks bolder
ax1.tick_params('both', length=10, width=1.5, which='major')
ax1.tick_params('both', length=6, width=1, which='minor')

### Save and show.
plt.savefig('x-anti.png',bbox_inches='tight')
plt.show()

    
