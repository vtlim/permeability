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


def plot_correlation(com_file, hbond_list, orient_file, n_bins=50,
    symmetry=False, what_for='talk', verbose=False):
    """
    symmetry : Boolean
        apply membrane symmetry by treating bins with abs(z)=0,
        for example, treating z=-30 together with z=30, such as
        finding the mean number of hydrogen bonds at that position
    """

    def call_bin_stats(ydata):
        # request mean/std/len for each bin given pre-defined bins
        stats, bin_number = bin_stats(ydata, binned_com_inds,
            [np.mean, np.std, len])
        return stats, bin_number

    def write_to_file(means, stds, fname):
        means = np.array(means).T
        stds = np.array(stds).T
        data_write = np.column_stack((bin_midpoints, means, stds))
        np.savetxt(fname, data_write, fmt='%10.4f', delimiter='\t')

    # load the position data
    com_time, com_data = np.loadtxt(com_file, unpack=True)
    if symmetry:
        com_data = np.abs(com_data)
    com_min = np.min(com_data)
    com_max = np.max(com_data)

    # separate the center of mass position data into bins based on min/max
    # add offset to com_max so that com_max doesn't get a bin by itself
    # see np.digitize docs for example for right=False (default)
    bins = np.linspace(com_min, com_max+.00001, n_bins+1)
    bin_midpoints = (bins[1:] + bins[:-1]) / 2
    print(f"\nData will be grouped into {n_bins} bins spanning a range from "
          f"{com_min:.2f} to {com_max:.2f}. Bin edges:\n{bins}\n")

    # bin the center of mass data (x-axis) for bin_stats function
    binned_com_inds = np.digitize(com_data, bins)

    # initialize figure
    fig = plt.figure()
    ax = fig.gca()

    if what_for == 'talk':
        fig.set_size_inches(8, 6)
        small_font = 16
        large_font = 20
    else:
        fig.set_size_inches(3.5, 2.5)
        small_font = 10
        large_font = 12

    # process and plot hbonds data
    if hbond_list is not None:

        # generate labels from filename(s)
        labels = [os.path.splitext(os.path.basename(x))[0] for x in hbond_list]
        labels = [i.split('_')[-1] for i in labels]

        # load hbonds data
        hb_array = []
        for f in hbond_list:
            hb_time, hb_data = np.loadtxt(f, unpack=True)
            hb_array.append(hb_data)

        # group hbonds data to bins and calculate stats of each bin
        for l, hb_data in zip(labels, hb_array):
            stats, bin_number = call_bin_stats(hb_data)

            # add data to plot
            means, stds, lens = plot_from_bins(bin_midpoints, stats, l)

            # write information to file
            write_to_file(means, stds, f'com_hbonds_{l}.dat')

        # refine plot details
        y_label = 'hydrogen bond count'
        fig_name = 'plot_hbonds.svg'
        plt.legend(fontsize=small_font-2, loc='upper left')
        plt.xlim(0, 40)
        plt.ylim(-0.8, 11)
        plt.grid()


    # process and plot orientation data
    if orient_file is not None:

        # load the orientation data
        ori_time, ori_data = np.loadtxt(orient_file, unpack=True)

        # group data to bins and calculate stats of each bin
        stats, bin_number = call_bin_stats(ori_data)

        # add data to plot
        means, stds, lens = plot_from_bins(bin_midpoints, stats)
        plt.grid()
        y_label = 'orientation'
        fig_name = 'plot_orientation.png'

        # write information to file
        write_to_file(means, stds, f'com_orient.dat')

        # print out details
        if verbose:
            print("bin\tmidpt\t mean\tstdev\tcount")
            for i, n in enumerate(bin_number):
                print(f"{n}\t{bin_midpoints[i]:.2f}\t{means[i]:5.2f}\t"
                      f"{stds[i]:.2f}\t{lens[i]}")


    # fancify final plot (in common for hbonds and orientation plots)
    plt.xlabel('distance from membrane center ($\mathrm{\AA}$)', fontsize=small_font)
    plt.ylabel(y_label, fontsize=large_font)
    plt.xticks(fontsize=small_font)
    plt.yticks(fontsize=small_font)
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

    parser.add_argument("-s", "--symmetry", action="store_true", default=False,
                        help="Apply symmetry across the membrane such that "
                        "the reported value for bin z=30 to 35 A represents "
                        "the mean of data at z=30-35 A and at -z=30=35 A")

    parser.add_argument("-w", "--what_for", default='talk',
                        help="Format plot for either 'talk' or 'paper'.")

    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Print out information on bin midpoints, "
                        "means, stdevs, and counts per bin.")

    args = parser.parse_args()
    opt = vars(args)

    plot_correlation(args.com, args.hbond, args.orient, args.nbins,
        args.symmetry, args.what_for, args.verbose)
