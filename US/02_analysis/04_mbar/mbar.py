#!/usr/bin/env python

# Purpose: Use MBAR to compute PMF from NAMD US simulations.
# Usage: python file.py > output.dat

# Adapted from:
# https://github.com/davecap/pymbar/blob/master/examples/umbrella-sampling.py


import os
import re
import numpy # numerical array library
import pymbar # multistate Bennett acceptance ratio
from pymbar import timeseries # timeseries analysis
import matplotlib.pyplot as plt

# =========== VARIABLES ============================

### Parameters from US simulations

K = 53          # number of windows
z_min = -8.0  # min independent variable
z_max = +44.0 # max independent variable
temp = 308.     # temperature 

nbins = 180     # number of bins for PMF (like nbins of histogram, more = finer data)
N_max = 52001   # maximum number of snapshots/simulation
#tstart = 0      # int start time (ns) for each window (assuming step*2/1e6 = time)
#tstop = 26     # int stop time (ns) for each window

os.chdir('/tw/limvt/04_mbar/')

### specify tstart and tstop to read 
portion = True
if portion:
    tstarts = numpy.ones(K,float)*39
    tstops = numpy.ones(K,float)*52

    for i in range(30,45,1):
        tstarts[i] = 13
        tstops[i] = 26
    tstarts[5] = 52
    tstarts[48] = 52
    tstops[5] = 104
    tstops[48] = 104

### Constants.
kB = 1.381e-23 * 6.022e23 / 1000.0 # Boltzmann constant in kJ/mol/K
beta = 1.0 / (kB * temp) # inverse temperature of simulations (in 1/(kJ/mol))


# =========== FUNCTIONS ============================


def parseWindow(filename, tstart=0, tstop=None):
    """
    For this window's data, get subset of data for specified start/end times.
    Not called by main script, but called inside prepWindow.

    Parameters
    ----------
    filename: string name of the file to process.
       For *.traj file, assumes all lines are data (e.g. no comment lines).
    tstart: integer nanosecond start time
    tstop: integer nanosecond stop time 

    Returns
    -------
    counts: int, number of entries for this particular window
    winZ: numpy list containing data for this window from tstart to tstop

    """

    # Read file.
    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()

    # Convert from time (ns) to step number.
    tstart = tstart/2*1000.
    if tstop != None:
        tstop = tstop/2*1000.+1
    else:
        tstop = len(lines)

    n = 0
    winZ = numpy.zeros([len(lines)])
    for line in lines:
        if n<tstart: 
            n += 1
            continue
        if n>=tstop: 
            n += 1
            break
        if line[0] != '#' and line[0] != '@':
            tokens = line.split()
            winZ[n] = float(tokens[1]) # transmemb position
            n += 1
    counts = min(tstop-tstart, len(lines))
    winZ = winZ[tstart:tstop]
    return counts, winZ



def prepWindow(filename, tstart=0, tstop=None):
    """
    Read window .traj file, compute correlation times, subsample data.

    Parameters
    ----------
    filename: string name of the file to process.
       For *.traj file, assumes all lines are data (e.g. no comment lines).
    tstart: integer nanosecond start time
    tstop: integer nanosecond stop time

    Returns
    -------
    counts: int, number of entries for this particular window
    winZ: numpy list containing SUBSAMPLED data for this window from tstart to tstop

    """
    # Parse data.
    n, z_sub = parseWindow(filename, tstart, tstop)

    # Compute correlation times for z (actual spring center position) timeseries.
    g = timeseries.statisticalInefficiency(z_sub)
    print "Correlation time for %s is %10.3f" % (re.split('\W+',filename)[1],g)
    indices = timeseries.subsampleCorrelatedData(z_sub, g) 

    # Subsample data.
    zsublen = len(indices)
    z_sub = z_sub[indices]
    return zsublen, z_sub


def plotPMF(xdata, ydata, devs, xlabel, ylabel, title, save=False, figname='plot.png'):
    ### Initialize figure.
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    ### Label the figure.
    ax1.set_title(title,fontsize=20)
    ax1.set_xlabel(xlabel,fontsize=18)
    ax1.set_ylabel(ylabel,fontsize=19)
    for xtick in ax1.get_xticklabels():
        xtick.set_fontsize(14)
    for ytick in ax1.get_yticklabels():
        ytick.set_fontsize(14)
    
    ### Plot the data.
    ax1.errorbar(xdata, ydata, yerr=devs, ecolor='k')
    #ax1.plot(xdata, ydata)
    if save: plt.savefig(figname)
    plt.show()
    
# ==================================================
# ==================================================


### Allocate storage for simulation data
T_k = numpy.ones(K,float)*temp # inital temperatures are all equal 
N_k = numpy.zeros([K], numpy.int32) # N_k[k] is the number of snapshots from umbrella simulation k
K_k = numpy.zeros([K], numpy.float64) # K_k[k] is the spring constant (in kJ/mol/Angs**2) for umbrella simulation k
z0_k = numpy.zeros([K], numpy.float64) # z0_k[k] is the spring center location (in Angs) for umbrella simulation k
z_kn = numpy.zeros([K,N_max], numpy.float64) # z_kn[k,n] is the transmembrane position (in Angs) for snapshot n from umbrella simulation k
u_kn = numpy.zeros([K,N_max], numpy.float64) # u_kn[k,n] is the reduced potential energy without umbrella restraints of snapshot n of umbrella simulation k

### beta factor for all temps. (See referenced code for diff. temp windows.)
beta_k = 1.0/(kB*T_k)

### Read in file containing US centers (column 1) and spring constants and (col 2). 
### Units of centers being Angstrom, spring constant as kJ/mol/Angs**2 (convert from kcal/mol).
infile = open('data/centers.dat', 'r')
lines = infile.readlines()
infile.close()
for k in range(K):
    # Parse line k.
    line = lines[k]
    tokens = line.split()
    z0_k[k] = float(tokens[0]) # spring center (Angs)
    K_k[k] = float(tokens[1]) # spring constant (kJ/mol/Angs**2)    


### Read/process simulation data for each window.
for k in range(K):

    # Get window number (e.g. 09)
    if k < 10: kk = '0'+str(k)
    else: kk = str(k)

    filename = 'data/win%s.traj' % kk
#    filename = 'data/26ns/win%d.traj' % k

    n, winZ = prepWindow(filename, tstarts[k], tstops[k])

    z_kn[k][0:len(winZ)] = winZ
    N_k[k] = n


### Shorten list of counts per window (N) and the US center (z). Create list for PEs.
N_max = numpy.max(N_k) # shorten the array size
u_kln = numpy.zeros([K,K,N_max], numpy.float64) # u_kln[k,l,n] is the reduced potential energy of snapshot n from umbrella simulation k evaluated at umbrella l

### Set zero of u_kn -- this is arbitrary.
### At this point, is still zero since orig script only defined for DiffTemp = True ?
u_kn -= u_kn.min()


### Bin the data.
print "Binning data..."

# Construct torsion bins
delta = (z_max - z_min) / float(nbins)

# compute bin centers
bin_center_i = numpy.zeros([nbins], numpy.float64)
for i in range(nbins):
    bin_center_i[i] = z_min + delta/2 + delta * i

# Compute bin assignment.
bin_kn = numpy.zeros([K,N_max], numpy.int32)
for k in range(K):
    for n in range(N_k[k]):
        bin_kn[k,n] = int((z_kn[k,n] - z_min) / delta)

### Evaluate reduced energies in all umbrellas
print "Evaluating reduced potential energies..."
for k in range(K):
    for n in range(N_k[k]):
        # Compute deviation from umbrella center
        dz = z_kn[k,n] - z0_k

        # Compute energy of snapshot n from simulation k in umbrella potential
        u_kln[k,:,n] = u_kn[k,n] + beta_k[k] * (K_k/2.0) * dz**2

### Initialize MBAR.
print "Running MBAR..."
mbar = pymbar.MBAR(u_kln, N_k, verbose = True, method = 'adaptive')

### Compute PMF in unbiased potential (in units of kT).
(f_i, df_i) = mbar.computePMF(u_kn, bin_kn, nbins)


### Write out PMF.
print "\n\nPMF (in units of Angs, kT)"
print "%8s %8s %8s" % ('bin', 'f', 'df')
for i in range(nbins):
    print "%8.6f %8.6f %8.6f" % (bin_center_i[i], f_i[i], df_i[i])

### Convert units: x (A --> nm), y (kT --> kcal/mol).
xs = [item/10 for item in bin_center_i]
ys = [item*0.6120 for item in f_i]
ss = [item*0.6120 for item in df_i]


### Write out PMF with converted units.
print "\n\nPMF (in units of nm, kcal/mol)"
print "%8s %8s" % ('bin', 'f')
for i in range(nbins):
    print "%8.6f %8.6f %8.6f" % (xs[i], ys[i], ss[i])


### Plot the PMF.
xlabel = 'z coordinate (nm)'
ylabel = 'free energy (kcal/mol)'
title = 'Potential of Mean Force of Water\nthrough POPC bilayer (0-52* ns)'
#plotPMF(xs, ys, ss, xlabel, ylabel, title, save=True, figname='0-52ns.eps')

