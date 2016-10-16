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

dataf=['US_0-4ns.pmf', 'US_4-8ns.pmf', 'US_8-12ns.pmf']
os.chdir('/home/victoria/Documents/pmf/07_us/02_analysis/03_wham')
#os.chdir('/pub/limvt/pmf/07_us/02_analysis/03_wham')

# ------------------------------------------------- #


origxs = []
origys = []
writeX = True # only write Xs for one file (all *should* be same)

for i, f in enumerate(dataf):
    origys.append([])

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

    writeX = False

### Convert x's from Angs --> nm.
origxs = [0.1*i for i in origxs]

#### Generate lists to plot both sides of symmetrized data
#allx = np.zeros([2*len(symxs)-1], np.float64)  
#ally = np.zeros([2*len(symys)-1], np.float64)
#
#for i in range(len(allx)):
#    if i < len(symxs)-1:
#        allx[i] = -1*symxs[len(symxs)-1-i]
#        ally[i] = symys[len(symxs)-1-i]
#    else:
#        allx[i] = symxs[i-len(symxs)+1]
#        ally[i] = symys[i-len(symxs)+1]

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
plt.savefig('us-pmf-3x.png',bbox_inches='tight')
plt.show()

    
