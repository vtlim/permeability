#!/usr/bin/env python

"""

Usage: python plot_permeate.py -i abf_file_sympmf.dat [--pmf] [--diffuse]

Purpose: Plot PMF or diffusivity for membrane permeability, formatting axes accordingly.

By: Victoria T. Lim
Version: Sep 21 2018

"""

import os, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def plot_perm(in_file, out_file, pmf, diffuse):

    if pmf:
        ptitle = 'Potential of Mean Force of Water\nthrough POPC bilayer (ABF)'
        pxlabel = 'z coordinate ($\AA$)'
        pylabel = 'free energy (kcal/mol)'
    elif diffuse:
        ptitle = 'Diffusivity of Water\nthrough POPC bilayer (ABF)'
        pxlabel = 'z coordinate ($\AA$)'
        pylabel = 'diffusivity ($\AA^2/ns$)'

    ### Read in data from file.
    data_all = np.loadtxt(in_file)
    full_cvs = data_all[:,0]
    full_pmf = data_all[:,1]
    try:
        full_std = data_all[:,2]
        with_err = True
    except IndexError:
        with_err = False

    ### Initialize figure.
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ### Label the figure.
#    ax1.set_title(ptitle,   fontsize=20)
    ax1.set_xlabel(pxlabel, fontsize=18)
    ax1.set_ylabel(pylabel, fontsize=19)

    for xtick in ax1.get_xticklabels():
        xtick.set_fontsize(14)
    for ytick in ax1.get_yticklabels():
        ytick.set_fontsize(14)

    ### Plot the data.
    if with_err:
        ax1.errorbar(full_cvs, full_pmf, yerr=full_std,capsize=3,ecolor='k')
    else:
        ax1.plot(full_cvs, full_pmf)

    ### set axes limits and tick marks
    axes = plt.gca()
    minorLocator = AutoMinorLocator(2)

    axes.set_xlim([-37,37])
    ax1.set_xticks(np.arange(-35,37,5),minor=True) # x: explicitly set minor ticks

    if pmf:
        axes.set_ylim([-0.4,8.4])
        ax1.set_yticks(np.arange(0,10,2)) # y: specify major ticks
    elif diffuse:
        axes.set_ylim([-0,810])
    ax1.yaxis.set_minor_locator(minorLocator) # y: specify minor ticks

    ### make tick marks bolder
    ax1.tick_params('both', length=10, width=1.5, which='major')
    ax1.tick_params('both', length=6, width=1, which='minor')

    ### Save and show.
    plt.savefig(out_file,bbox_inches='tight')
    plt.show()



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile",
                        help="Filename of the full length membrane profile of"
                             " PMF or diffusivity to plot.")

    parser.add_argument("-p", "--pmf", action="store_true", default=False,
                        help="Format plot for potential of mean force.")

    parser.add_argument("-d", "--diffuse", action="store_true", default=False,
                        help="Format plot for diffusivity.")

    args = parser.parse_args()
    opt = vars(args)

    # define output name of figure
    oname = os.path.splitext(args.infile)[0] + '.png'

    plot_perm(args.infile, oname, args.pmf, args.diffuse)
