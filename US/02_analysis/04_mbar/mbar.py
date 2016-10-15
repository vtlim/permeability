#!/usr/bin/env python

# Purpose: Use MBAR to compute PMF from US simulation.
#   The data represents an umbrella sampling simulation for the
#   permeation of a tagged water molecule through a POPC lipid bilayer. 
# Usage: python file.py > output.dat

# Adapted from:
# https://github.com/davecap/pymbar/blob/master/examples/umbrella-sampling.py


import os
import numpy # numerical array library
import pymbar # multistate Bennett acceptance ratio
from pymbar import timeseries # timeseries analysis
import matplotlib.pyplot as plt


# Constants.
kB = 1.381e-23 * 6.022e23 / 1000.0 # Boltzmann constant in kJ/mol/K
temperature = 308 # assume a single temperature -- can be overridden with data from center.dat 
beta = 1.0 / (kB * temperature) # inverse temperature of simulations (in 1/(kJ/mol))

# Parameters
K = 53 # number of umbrellas
N_max = 13001 # maximum number of snapshots/simulation
chi_min = -8.0 # min for PMF
chi_max = +44.0 # max for PMF
nbins = 180 # number of bins for 1D PMF
tstart = 0 # start time in ns for each window (assuming file has 1000 data pts per ns)
tstop = 26 # stop time in ns for each window

# Allocate storage for simulation data
T_k = numpy.ones(K,float)*temperature # inital temperatures are all equal 
N_k = numpy.zeros([K], numpy.int32) # N_k[k] is the number of snapshots from umbrella simulation k
K_k = numpy.zeros([K], numpy.float64) # K_k[k] is the spring constant (in kJ/mol/Angs**2) for umbrella simulation k
chi0_k = numpy.zeros([K], numpy.float64) # chi0_k[k] is the spring center location (in Angs) for umbrella simulation k
chi_kn = numpy.zeros([K,N_max], numpy.float64) # chi_kn[k,n] is the transmembrane position (in Angs) for snapshot n from umbrella simulation k
u_kn = numpy.zeros([K,N_max], numpy.float64) # u_kn[k,n] is the reduced potential energy without umbrella restraints of snapshot n of umbrella simulation k
g_k = numpy.zeros([K],numpy.float32);

def parseData(lines, tstart=0, tstop=None):
    if tstop == None:
        tstop = len(lines)

    tstart = tstart/2*1000.
    tstop = tstop/2*1000.+1

    n = 0
    winZ = numpy.zeros([len(lines)])
    for line in lines:
        if n<tstart: 
            n += 1
            continue
        if n>=tstop: 
            n += 1
            continue
        if line[0] != '#' and line[0] != '@':
            tokens = line.split()
            chi = float(tokens[1]) # transmemb position
            winZ[n] = chi
            n += 1
    return tstop-tstart, winZ

# Read in umbrella spring constants and centers. Format columns by (1) center, (2) spring const, (3) temp optional.
os.chdir('/tw/limvt/04_mbar/')
infile = open('data/centers.dat', 'r')
lines = infile.readlines()
infile.close()
for k in range(K):
    # Parse line k.
    line = lines[k]
    tokens = line.split()
    chi0_k[k] = float(tokens[0]) # spring center location (in Angs)
    K_k[k] = float(tokens[1]) # spring constant (kJ/mol/Angs**2)    
    if len(tokens) > 2:
        T_k[k] = float(tokens[2])  # temperature the kth simulation was run at.

# beta factor for all (same) temps. (Code relevant to diff. temp windows was taken out.)
beta_k = 1.0/(kB*T_k)

# Read the simulation data
for k in range(K):
    # Read transmembrane position data.
    filename = 'data/win%d.traj' % k
    print "Reading %s..." % filename
    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()

    # Parse data.
    n, winZ = parseData(lines, tstart, tstop)
    chi_kn[k] = winZ
    N_k[k] = n

    # Compute correlation times for potential energy and chi timeseries. 
    # If the temperatures differ, use energies to determine samples; otherwise, use the cosine of chi
    chi_radians = chi_kn[k,tstart*1000:tstart*1000+N_k[k]]
    g_cos = timeseries.statisticalInefficiency(numpy.cos(chi_radians))
    g_sin = timeseries.statisticalInefficiency(numpy.sin(chi_radians))
    print "g_cos = %.1f | g_sin = %.1f" % (g_cos, g_sin)
    g_k[k] = max(g_cos, g_sin)
    print "Correlation time for set %5d is %10.3f" % (k,g_k[k])
    indices = timeseries.subsampleCorrelatedData(chi_radians, g=g_k[k]) 
    indices = [tstart*1000+i for i in indices]

    # Subsample data.
    N_k[k] = len(indices)
    u_kn[k,tstart*1000:tstart*1000+N_k[k]] = u_kn[k,indices]
    chi_kn[k,tstart*1000:tstart*1000+N_k[k]] = chi_kn[k,indices]

N_max = numpy.max(N_k) # shorten the array size
chi_kn = chi_kn[:,tstart*1000:tstart*1000+N_max]
u_kln = numpy.zeros([K,K,N_max], numpy.float64) # u_kln[k,l,n] is the reduced potential energy of snapshot n from umbrella simulation k evaluated at umbrella l


# Set zero of u_kn -- this is arbitrary.
u_kn -= u_kn.min()

# Construct torsion bins
print "Binning data..."
delta = (chi_max - chi_min) / float(nbins)

# compute bin centers
bin_center_i = numpy.zeros([nbins], numpy.float64)
for i in range(nbins):
    bin_center_i[i] = chi_min + delta/2 + delta * i

# Bin data
bin_kn = numpy.zeros([K,N_max], numpy.int32)
for k in range(K):
    for n in range(N_k[k]):
        # Compute bin assignment.
        bin_kn[k,n] = int((chi_kn[k,n] - chi_min) / delta)

# Evaluate reduced energies in all umbrellas
print "Evaluating reduced potential energies..."
for k in range(K):
    for n in range(N_k[k]):
        # Compute minimum-image torsion deviation from umbrella center l
        dchi = chi_kn[k,n] - chi0_k
        for l in range(K):
            if (abs(dchi[l]) > 180.0):
                dchi[l] = 360.0 - abs(dchi[l])

        # Compute energy of snapshot n from simulation k in umbrella potential l
        u_kln[k,:,n] = u_kn[k,n] + beta_k[k] * (K_k/2.0) * dchi**2

# Initialize MBAR.
print "Running MBAR..."
mbar = pymbar.MBAR(u_kln, N_k, verbose = True, method = 'adaptive')

# Compute PMF in unbiased potential (in units of kT).
(f_i, df_i) = mbar.computePMF(u_kn, bin_kn, nbins)

# Write out PMF
print "\n\nPMF (in units of Angs, kT)"
print "%8s %8s %8s" % ('bin', 'f', 'df')
for i in range(nbins):
    print "%8.6f %8.6f %8.6f" % (bin_center_i[i], f_i[i], df_i[i])

### Convert units: x (A --> nm), y (kT --> kcal/mol).
xs = [item/10 for item in bin_center_i]
ys = [item*0.6120 for item in f_i]

### Write out PMF
print "\n\nPMF (in units of nm, kcal/mol)"
print "%8s %8s" % ('bin', 'f')
for i in range(nbins):
    print "%8.6f %8.6f" % (xs[i], ys[i])

# ===========================================
#           PLOTTING
# ===========================================

### Initialize figure.
fig = plt.figure()
ax1 = fig.add_subplot(111)

### Label the figure.
ax1.set_title('Potential of Mean Force of Water\nthrough POPC bilayer (0-13 ns)',fontsize=20)
ax1.set_xlabel('z coordinate (nm)',fontsize=18)
ax1.set_ylabel('free energy (kcal/mol)',fontsize=19)
for xtick in ax1.get_xticklabels():
    xtick.set_fontsize(14)
for ytick in ax1.get_yticklabels():
    ytick.set_fontsize(14)

### Plot the data.
ax1.plot(xs, ys)
#plt.savefig('0-13ns.png')
plt.show()

