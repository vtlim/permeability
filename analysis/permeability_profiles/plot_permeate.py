#!/usr/bin/env python

"""

plot_permeate.py

Purpose: Plot PMF or diffusivity profiles. Check that units in script are
    consistent with units in input files.

Examples:
- python plot_permeate.py -i pmf_symmetrized_with_errbars.dat --pmf         -w 'talk'
- python plot_permeate.py -i diffusivity_symmetrized.dat      --diffusivity -w 'paper'

By: Victoria T. Lim
Version: Jan 21 2020

"""

import os
import numpy as np
import matplotlib.pyplot as plt


def subsample_errors(errlist, every_nth=20):
    "Only keep every Nth value of error values."""
    size = len(errlist)
    subsamp = np.zeros(size)

    # get indices which should be kept
    keep_idx = range(0, size, every_nth)

    # transfer the to-keep values into the array of zeros
    subsamp[keep_idx] = np.array(errlist)[keep_idx]

    return subsamp


def plot_perm(in_files, out_file, data_type, what_for='talk'):

    if data_type == 'pmf':
        y_label = 'potential of mean\nforce (kcal/mol)'
        y_range = (-10, 15)
    elif data_type == 'diffuse':
        y_label = 'diffusivity ($\mathrm{\AA}^2/ns$)'
        y_range = (0, 800)
    elif data_type == 'orient':
        y_label = 'permeant orientation'
        y_range = (-1.4, 1.4)
    elif data_type == 'pka':
        y_label = '$\Delta \mathrm{pK_a}$'
        y_range = (-0.9, 4.0)

    # google hex codes
    #colors = ['#0f9d58', '#ab30c4', '#46bdc6', '#f4b400', '#db4437', '#4285f4', '#ff6d00']
    colors = ['#0f9d58', '#ab30c4', '#f4b400'] # 2GBI
    #colors = ['#46bdc6', '#db4437'] # CGBI

    # read in data from file(s)
    y_list = []
    x_list = []
    s_list = []
    err_check_list = []
    num_files = 0

    for f in in_files:

        # load data but don't unpack bc not sure of number of columns
        data_all = np.loadtxt(f)

        # get components of the data
        x_list.append(data_all[:,0])
        y_list.append(data_all[:,1])

        # see if error bar values are in 2nd column
        try:
            s_list.append(data_all[:,2])
            err_check_list.append(True)
        except IndexError:
            err_check_list.append(False)

        # increment count
        num_files += 1

    # get legend labels from filenames
    labels = [os.path.splitext(os.path.basename(x))[0] for x in in_files]

    # initialize figure
    fig = plt.figure()
    ax = fig.gca()

    # set figure and font sizes based on what_for
    if what_for == 'talk':
        fig.set_size_inches(8, 6)
        small_font = 16
        large_font = 20
    elif what_for == 'paper':
        fig.set_size_inches(3.5, 2.5)
        small_font = 10
        large_font = 12

    ax.set_xlabel('distance from membrane center ($\mathrm{\AA}$)', fontsize=large_font)
    ax.set_ylabel(y_label, fontsize=large_font)
    for xtick in ax.get_xticklabels():
        xtick.set_fontsize(small_font)
    for ytick in ax.get_yticklabels():
        ytick.set_fontsize(small_font)

    # plot the data
    for i in range(num_files):

        # add error region
        if err_check_list[i] == True:

            # option 1: plot with solid error bars, every nth
            subsamp_errs = subsample_errors(s_list[i], 10)
            ax.errorbar(x_list[i], y_list[i], label=labels[i], color=colors[i],
                yerr=subsamp_errs, elinewidth=1.0)

#            # option 2: plot with shaded error regions
#            ax.plot(x_list[i], y_list[i], label=labels[i], color=colors[i])
#            ax.fill_between(x_list[i], y_list[i]-s_list[i], y_list[i]+s_list[i],
#                color=colors[i], alpha=0.12)

        else:
            ax.plot(x_list[i], y_list[i], label=labels[i], color=colors[i])

    # show minor ticks on both sets of edges but not for major ticks
#    ax.xaxis.set_ticks_position('both')
#    ax.yaxis.set_ticks_position('both')
#    ax.tick_params('y', which='major', right=False)
#    ax.tick_params('x', which='major', top=False)

    # format x and y ranges
    ax.set_ylim([y_range[0], y_range[1]])
    ax.set_xlim([-40, 40])
#    ax.set_xticks(np.arange(-40, 40, 2), minor=True)
#    ax.tick_params('both', which='minor', direction='in')

#    if data_type == 'pmf':
#        ax.set_yticks(np.arange(y_range[0], y_range[1], 2.5), minor=True)

#    # (optional) shade custom regions for orientation plot
#    ax.axvspan(8, 20, facecolor='lightgrey', alpha=0.95)

    # add legend if multiple files
    if num_files > 1:

        # generate legend
        plt.legend(fontsize=small_font-2)

    # save and show
    plt.grid()
    plt.savefig(out_file,bbox_inches='tight')
    plt.show()



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infiles", nargs='+',
                        help="Filename(s) of PMF or diffusivity profile(s).")

    parser.add_argument("-d", "--data_type", default='pmf',
                        help="Type of input data. Options: 'pmf', 'diffuse', "
                             "'orient', 'pka' ")

    parser.add_argument("-w", "--what_for", default='talk',
                        help="Format plot for either 'talk' or 'paper'.")

    args = parser.parse_args()
    opt = vars(args)

    plot_perm(args.infiles, 'pka_2gbi.png', args.data_type, args.what_for)
