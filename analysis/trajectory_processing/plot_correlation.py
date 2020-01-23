#!/usr/bin/env python

"""

plot_correlation.py

Purpose: Bin and plot data for permeant orientation or hbond count as a
    function of permeant position (z coordinate).

Examples:
- python plot_correlation.py -x z_com.dat -h hbonds_carbonyl.dat hbonds_phosphate.dat hbonds_water.dat
- python plot_correlation.py -x z_com.dat -o selorient.dat -w 'paper'

By: Victoria T. Lim
Version: Jan 23 2020

"""

import os
import numpy as np
import matplotlib.pyplot as plt


def bin_stats(data, binned_inds, funcs):
    """
    Modified from:
    https://stackoverflow.com/a/36460256/8397754
    """
    # get unique indices
    uniq_binned_inds = np.sort(np.unique(binned_inds))

    statistics = []
    for bin_idx in uniq_binned_inds:

        # get locations of all of bin_idx
        all_bin_idx = [i for i, x in enumerate(binned_inds) if x==bin_idx]

        # group data into this bin index
        bin_arr = data[all_bin_idx]

        # calculate the specified stats
        statistics.append([f(bin_arr) for f in funcs])

    return statistics, uniq_binned_inds


def plot_from_bins(bin_midpoints, stats, label=''):

    means = [i[0] for i in stats]
    stds =  [i[1] for i in stats]
    lens =  [i[2] for i in stats]

    plt.errorbar(bin_midpoints, means, yerr=stds, label=label)

    return means, stds, lens


def plot_correlation(com_file, hbond_list, orient_file, n_bins=50, what_for='talk', verbose=False):

    def call_bin_stats(ydata):
        stats, bin_number = bin_stats(ydata, binned_com_inds,
            [np.mean, np.std, len])
        return stats, bin_number

    if what_for == 'talk':
        pass
    else:
        pass

    # load the position data
    com_time, com_data = np.loadtxt(com_file, unpack=True)

    # define bins based on range of positions
    com_min = np.min(com_data)
    com_max = np.max(com_data)

    # add offset to com_max so that com_max doesn't get a bin by itself
    # see example for right=False (default) on np.digitize docs
    bins = np.linspace(com_min, com_max+.00001, n_bins+1)
    print(f"\nData will be grouped into {n_bins} bins spanning a range from "
          f"{com_min:.2f} to {com_max:.2f}. Bin edges:\n{bins}\n")

    # bin the data to be grouped by position
    binned_com_inds = np.digitize(com_data, bins)
    bin_midpoints = (bins[1:] + bins[:-1]) / 2

    # bin the hbonds and orientation data wrt binned position data
    if hbond_list is not None:

        # generate labels from filename(s)
        labels = [os.path.splitext(os.path.basename(x))[0] for x in hbond_list]
        labels = [i.split('_')[1] for i in labels]

        # load hbonds data
        hb_array = []
        for f in hbond_list:
            hb_time, hb_data = np.loadtxt(f, unpack=True)
            hb_array.append(hb_data)

        # group data to bins and calculate stats of each bin
        for l, hb_data in zip(labels, hb_array):
            stats, bin_number = call_bin_stats(hb_data)

            # add data to plot
            means, stds, lens = plot_from_bins(bin_midpoints, stats, l)

        y_label = 'hydrogen bond count'
        fig_name = 'plot_hbonds.png'
        plt.legend()


    if orient_file is not None:

        # load the orientation data
        ori_time, ori_data = np.loadtxt(orient_file, unpack=True)

        # group data to bins and calculate stats of each bin
        stats, bin_number = call_bin_stats(ori_data)

        # add data to plot
        means, stds, lens = plot_from_bins(bin_midpoints, stats)
        y_label = 'orientation'
        fig_name = 'plot_orientation.png'

        # print out details
        if verbose:
            print("bin\tmidpt\t mean\tstdev\tcount")
            for i, n in enumerate(bin_number):
                print(f"{n}\t{bin_midpoints[i]:.2f}\t{means[i]:5.2f}\t"
                      f"{stds[i]:.2f}\t{lens[i]}")


    # fancify the plot
    plt.xlabel('distance from membrane center ($\mathrm{\AA}$)')
    plt.ylabel(y_label)
    plt.savefig(fig_name, bbox_inches='tight')
    plt.show()





if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-x", "--com",
                        help="Center of mass data used as the independent "
                        "variable. Formatted as two columns: time and com")

    parser.add_argument("-n", "--nbins", type=int, default=50,
                        help="Number of bins across the x-data into which"
                        " the y-data will be grouped.")

    parser.add_argument("-b", "--hbond", nargs='+',
                        help="One or more files for number of hbonds "
                        "(e.g., phosphate, carbonyl, water). Each should "
                        "be formatted in two columns of: time and count")

    parser.add_argument("-o", "--orient",
                        help="Permeant orientation data. Formatted as two "
                        "columns: time and orientation")

    parser.add_argument("-w", "--what_for", default='talk',
                        help="Format plot for either 'talk' or 'paper'.")

    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Print out information on bin midpoints, "
                        "means, stdevs, and counts per bin.")

    args = parser.parse_args()
    opt = vars(args)

    plot_correlation(args.com, args.hbond, args.orient, args.nbins, args.what_for, args.verbose)
