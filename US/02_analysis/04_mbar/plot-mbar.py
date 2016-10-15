#!/usr/bin/env python

# Purpose: Plot PMF results from output of the mbar.py script.
# Usage: python file.py

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import AutoMinorLocator

nbins=180  # should match the nbins value from the MBAR script
dataf=['umbrella-sampling-v5a.out','umbrella-sampling-v5b.out','umbrella-sampling-v5c.out']
os.chdir('/tw/limvt/04_mbar')

origxs = []
origys = []
writeX = True # only write Xs for one file (all should be same)

for i, f in enumerate(dataf):
    origys.append([])

    ### open and read data
    indata = open(f, 'r')
    lines = indata.readlines()[-nbins:]
    indata.close()

    for line in lines:

        ### add z-coordinate info. should be same for all files.
        if writeX:
            origxs.append(float(line.split()[0]))
    
        ### add free energy data
        origys[i].append(float(line.split()[1])) 

    writeX = False


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
    lbls.append(f.split('.')[0])
lbls = ['0-4 ns','4-8 ns','8-12 ns']

### Plot the data.
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
plt.savefig('mbar-3x.png',bbox_inches='tight')
plt.show()
