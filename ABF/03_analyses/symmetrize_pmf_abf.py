#!/usr/bin/env python

"""
TODO: How does diffusivity get symmetrized using counts as weights?
Maybe should create a separate script called symmetrize_input.py
which can be applied to US PMF, US diff, ABF diff (if can't use weighted)

TODO: separate the plotting function into another script which will
format labels and scales for either PMF or diffusivity

Usage: python symmetrize_pmf_abf.py -c abf_file.count -g abf_file.grad
       python symmetrize_pmf_abf.py -p abf_file_sympmf.dat

Purpose: Symmetrize PMF from ABF simulations by the following scheme:
         (1) compute weighted averages of the gradient
         (2) anti-symmetrize those weighted averages (see p. 558 of reference),
         (3) integrate anti-symmetrized gradients to get symmetrized PMF.

DOI of reference: 10.1021/ct400925s

By: Victoria T. Lim
Version: Sep 19 2018

Notes:
- colvar = collective variable

"""

import os, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def main(**kwargs):

    ### Load data and check that they have the same colvar grid.
    file_count = np.loadtxt(args.count)
    file_grad  = np.loadtxt(args.grad)
    colvar_values = file_count[:,0]
    colvar_values1 = file_grad[:,0]
    counts = file_count[:,1]
    grads =  file_grad[:,1]
    length = len(grads)
    if not np.array_equal(colvar_values,colvar_values1):
        sys.exit("ERROR: collective variable grid of .count and .grad files do not match")

    ### Find index where colvar changes sign (symmetrize around this point)
    ### z0 is where colvar=0 if present, else will be the negative colvar closest to 0
    zero_present = False
    z0 = np.where(colvar_values < 0)[0][-1]
    if colvar_values[z0] == 0:
        zero_present = True

    ### get the length of data points on the longest side
    longest_side_length = max(z0, length-z0)
    longer = "right"
    if longest_side_length == z0:
        longer = "left"
    longer_by = longest_side_length-z0
    print("# Symmetrization of the potential of mean force")
    print("# Input .grad file: {}\n# Input .count file: {}".format(args.grad, args.count))
    print("# Number of data points: {}\n# Zero-based index of the zero-value colvar: {}".format(length, z0))
    print("# The {} hand side of the PMF is longer by {} data points.".format(longer, longer_by))
    print("# Number of data points on longer edge: {}".format(longest_side_length))

    ### Initiate indices for symmetrization
    if zero_present:
        neg_i = z0
        pos_i = z0
    else:
        neg_i = z0
        pos_i = z0+1
        longest_side_length -= 1    # not sure if this should also apply to colvar-symmetric system, UNTESTED

    ### loop from zero to max edge, symmetrizing
    sym_grads = np.zeros([longest_side_length], np.float64)   # anti-symm gradients
    for i in range(longest_side_length):

        # handle cases that can't be symmetrized: (1) colvar=0, (2) no data on one side
        # zero case can be combined with one of others but written out for clarity
        if zero_present:
            sym_grads[i] = grads[neg_i]
        elif neg_i < 0:
            sym_grads[i] = grads[pos_i]
        elif pos_i > length:
            sym_grads[i] = grads[neg_i]
        else:
            #print(pos_i, counts[pos_i], grads[pos_i], counts[neg_i], grads[neg_i])
            top_frac = counts[pos_i]*grads[pos_i] - counts[neg_i]*grads[neg_i]
            bot_frac = counts[pos_i] + counts[neg_i]
            sym_grads[i] = top_frac / bot_frac

        neg_i -= 1
        pos_i += 1

    ### Integrate the symmetrized gradients. Trapezoid rule.
    # start from bulk water = 0. *-0.5 since going backwards.
    # TODO use numpy functions for integrating
    int_pmf = np.zeros([longest_side_length], np.float64)   # anti-symm gradients
    last = 0
    for i in reversed(range(longest_side_length)):
        int_pmf[i] = -0.5*0.1*(sym_grads[i]+sym_grads[i-1])+last
        last = int_pmf[i]

    ### Extract part of colvar array from zero-value-cv out to longest edge
    if longer == "right":
        half_cvs = colvar_values[z0:-1] # 0 to 43.9
    else:
        half_cvs = colvar_values[0:z0]  # untested

    ### Transform colvar unit from Angstroms to nanometers.
    half_cvs = 0.1*half_cvs

    ### Generate the other half by mirroring
    full_cvs = np.zeros([2*longest_side_length-1], np.float64)
    full_pmf = np.zeros([2*longest_side_length-1], np.float64)
    full_length = len(full_cvs)

    for i in range(full_length):
        if i < longest_side_length: # negative value colvars
            full_cvs[i] = -1*half_cvs[longest_side_length-1-i]
            full_pmf[i] = int_pmf[longest_side_length-1-i]
        else:                       # positive value colvars
            full_cvs[i] = half_cvs[i-longest_side_length+1]
            full_pmf[i] = int_pmf[i-longest_side_length+1]

    ### Write out PMF
    # abf_file_sympmf.dat
    print("\n\n# PMF (in units of nm, kcal/mol)")
    for i in range(full_length):
        print("\t{} {}".format(full_cvs[i], full_pmf[i]))


def plot_pmf(in_file, out_file):

    ptitle = 'Potential of Mean Force of Water\nthrough POPC bilayer (ABF)'
    pxlabel = 'z coordinate (nm)'
    pylabel = 'free energy (kcal/mol)'

    ### Read in data from file.
    # TODO get full_cvs and full_pmf from in_file

    ### Initialize figure.
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ### Label the figure.
    ax1.set_title(ptitle,   fontsize=20)
    ax1.set_xlabel(pxlabel, fontsize=18)
    ax1.set_ylabel(pylabel, fontsize=19)

    for xtick in ax1.get_xticklabels():
        xtick.set_fontsize(14)
    for ytick in ax1.get_yticklabels():
        ytick.set_fontsize(14)

    ### Plot the data.
    ax1.plot(full_cvs, full_pmf)

    ### set limits of the plot
    axes = plt.gca()
    axes.set_xlim([-3.7,3.7])
    axes.set_ylim([-0.4,8.4])

    ### tick mark frequencies
    ax1.set_yticks(np.arange(0,10,2)) # y: specify major ticks
    minorLocator = AutoMinorLocator(2)
    ax1.yaxis.set_minor_locator(minorLocator) # y: specify minor ticks
    #ax1.xaxis.set_minor_locator(minorLocator) # ??? no minor ticks for negatives
    ax1.set_xticks(np.arange(-3.5,4.5,1),minor=True) # x: explicitly set minor ticks

    ### make tick marks bolder
    ax1.tick_params('both', length=10, width=1.5, which='major')
    ax1.tick_params('both', length=6, width=1, which='minor')

    ### Save and show.
    plt.savefig(out_file,bbox_inches='tight')
    plt.show()



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--count",
                        help="Filename of ABF .count suffix with information on"
                             " total number of samples collected per grid point.")
    parser.add_argument("-g", "--grad",
                        help="Filename of ABF .grad suffix with information on"
                             " the ABF estimate of the free energy gradient.")
    parser.add_argument("-p", "--plot",
                        help="Filename of the symmetrized PMF (such as output"
                             "of this script) to plot.")

    args = parser.parse_args()
    opt = vars(args)
    main(**opt)
