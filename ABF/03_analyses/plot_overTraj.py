#!/usr/bin/python

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


# ============ Parameters ===================

win = 'win05-noMin'

filename = "xst1_win05_2-8.dat"
delimiter = " "
numCols = 3 # first n (non-time) data columns
#cols = [1,3] # first and 3 data columns
xlabel = "time (ns)"
ylabel = "dimension ($\AA$)"
plttitle = "PBC box size: %s" % (win.split('-')[0])
leglabel = ["X","Y","Z"]
figname = "plot_cell.png" 


#filename = "hv1+gbi_contacts.dat"
#delimiter = "  "
#numCols = 5
#xlabel = "time (ns)"
#ylabel = "Distance ($\AA$)"
#plttitle = "Hv1 Contacts with 2GBI, pose %s" % pose
#leglabel = ["F150-benzo","R211-guan","D112-imid","S181-imid","R211-imid"]
#figname = "plot_contacts.png"

# ===========================================



os.chdir('/pub/limvt/pmf/06_abf/%s/analysis/' % (win))

with open(filename) as f:
    data = f.read()
data = data.split('\n')[1:-1]

### Load data for x column.
x = [float(row.split(' ')[0]) for row in data]
# Convert the x-axis to ns (based on 2 fs step)
x = 0.000002*np.array(x)

### Load data for y columns.
y_mat = []
try:
    for i in cols:
       y_mat.append([row.split(delimiter)[i] for row in data])
except NameError:
    for i in range(1,numCols+1):
       y_mat.append([row.split(delimiter)[i] for row in data])
y_mat = np.array(y_mat)

### Initialize figure.
fig = plt.figure()
ax1 = fig.add_subplot(111)

### Label the figure.
ax1.set_title(plttitle,fontsize=20) 
ax1.set_xlabel(xlabel,fontsize=18)
ax1.set_ylabel(ylabel,fontsize=18)
for xtick in ax1.get_xticklabels():
    xtick.set_fontsize(16)
for ytick in ax1.get_yticklabels():
    ytick.set_fontsize(16)

### Set plot limits.
#axes = plt.gca()
#axes.set_ylim([0,6])

### Color the rainbow.
n, _ = y_mat.shape
colors = mpl.cm.rainbow(np.linspace(0, 1, n))
#colors = mpl.cm.rainbow(np.linspace(0, 0.4, n))

### Plot the data.
for color, y in zip(colors, y_mat):
    ax1.plot(x, y, color=color)
leg = ax1.legend(leglabel,loc=2)

plt.savefig(figname)
plt.show()


