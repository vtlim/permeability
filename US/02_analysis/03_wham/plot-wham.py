#!/usr/bin/env python

# Purpose: Plot PMFs generated from Grossfield WHAM.
#   Can plot several over time.
# Usage: python file.py

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import AutoMinorLocator


# -------------------- Variables ------------------ #

#dataf=['US_0-10ns.pmf', 'US_4-8ns.pmf', 'US_8-12ns.pmf']
#dataf=['US_0-13ns.pmf', 'US_13-26ns.pmf', 'US_26-39ns.pmf', 'US_39-52ns.pmf', 'US_52-104ns.pmf']
dataf=['US_0-104ns.pmf']

figname='pmf_all_mc10-noErr.png'
plotErr = False
# ------------------------------------------------- #

#os.chdir('/home/victoria/Documents/pmf/07_us/02_analysis/03_wham')
os.chdir('/pub/limvt/pmf/07_us/02_analysis/03_wham')

origxs = []
origys = []
stdevs = []
writeX = True # only write Xs for one file (all *should* be same)

for i, f in enumerate(dataf):
    origys.append([])
    stdevs.append([])

    ### open and read data
    indata = open(f, 'r')
    lines = indata.readlines()[1:]
    indata.close()

    for line in lines:
        if '#' in line[0]:
            continue

        ### add z-coordinate info. should be same for all files.
        if writeX:
            origxs.append(float(line.split()[0]))
    
        ### add free energy data
        origys[i].append(float(line.split()[1])) 

        ### add deviations from Monte Carlo bootstrap error analysis
        stdevs[i].append(float(line.split()[2])) 

    writeX = False

### Convert x's from Angs --> nm.
origxs = [0.1*i for i in origxs]


# ===========================================
#           PLOTTING
# ===========================================

### Initialize figure.
fig = plt.figure()
ax1 = fig.add_subplot(111)
colors = mpl.cm.rainbow(np.linspace(0, 1, len(origys)))

### Label the figure.
ax1.set_title('Potential of Mean Force of Water\nthrough POPC bilayer (US)',fontsize=20)
ax1.set_xlabel('z coordinate (nm)',fontsize=20)
ax1.set_ylabel('free energy (kcal/mol)',fontsize=20)
# increase tick label font sizes
for xtick in ax1.get_xticklabels():
    xtick.set_fontsize(20)
for ytick in ax1.get_yticklabels():
    ytick.set_fontsize(20)
# get legend labels
lbls = []
for f in dataf:
    lbls.append(f.split('.')[0].split('_')[1])


### Plot the data.
if plotErr:
    for color, y, dev in zip(colors, origys, stdevs):
        ax1.errorbar(origxs, y, yerr=dev, ecolor='k')
else:
    for color, y in zip(colors, origys):
        ax1.plot(origxs, y, color=color)
leg = ax1.legend(lbls,loc=1)

# plot only one list
#ax1.plot(origxs,origys[0])

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
plt.savefig(figname,bbox_inches='tight')
plt.show()

    
