#!/usr/bin/python

"""
area_box_lipid.py

Purpose:    For an MD simulation, evaluate
            (1) box area over time,
            (2) histogram of area per lipid.

By:         Victoria T. Lim
Version:    Dec 3 2018

TODO:       [1] let user save dat file and plot if desired
"""

import numpy as np
import matplotlib.pyplot as plt

def get_areas(in_list):

    # parse data in input files
    data = [np.loadtxt(f) for f in in_list]
    data = np.concatenate(data).T

    # multiply the x and y dimensions
    area = data[1]*data[5]
    return area

def calc_lipid_area(area, num_lipids):

    # convert from A^2 to nm^2
    area = area/100

    # get area per lipid by dividing num lipids per leaflet
    area = area/num_lipids

    return area

def area_per_lipid(num_lipids, in_list1, in_list2):

    # parse and calculate box areas from files
    area_1 = get_areas(in_list1)
    if in_list2 is not None:
        area_2 = get_areas(in_list2)

    # plot box area
    plt.plot(area_1)
    if in_list2 is not None:
        plt.plot(area_2)
    plt.xlabel('time step')
    plt.ylabel('box area ($\mathrm{\AA^2}$)')
    plt.savefig('area_box.png', bbox_inches='tight')
    plt.show()

    # calculate area per lipid
    area_1 = calc_lipid_area(area_1, num_lipids)
    if in_list2 is not None:
        area_2 = calc_lipid_area(area_2, num_lipids)

    # plot histogram of area per lipid
    plt.hist(area_1, 50, range=(0.64,0.70), alpha=0.5)
    if in_list2 is not None:
        plt.hist(area_2, 50, range=(0.64,0.70), alpha=0.5)
    plt.xlabel('area per lipid ($\mathrm{nm^2}$)')
    plt.ylabel('count')
    plt.savefig('area_lipid.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infiles1", required=True, nargs='+',
                        help="Name of xst file(s) from NAMD. Can list one or "
                        "more files to be plotted as part of the same line sequentially.")

    parser.add_argument("-j", "--infiles2", nargs='+',
                        help="(optional) Name of xst file(s) from NAMD to be "
                        "compared with infiles1. Can list one or more files to "
                        "be plotted as part of the same line but different "
                        "than that of infiles1.")

    parser.add_argument("-n", "--num_lipids", type=int,
                        help="Number of lipids per leaflet, to calculate area per lipid.")

    args = parser.parse_args()
    area_per_lipid(args.num_lipids, args.infiles1, args.infiles2)

