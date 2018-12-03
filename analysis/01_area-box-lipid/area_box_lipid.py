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

def get_areas(inputlist):
    data = [np.loadtxt(f) for f in inputlist]
    data = np.concatenate(data).T
    # multiply the x and y dimensions
    area = data[1]*data[5]
    return area

def calc_lipid_area(area):
    # convert from A^2 to nm^2
    area = area/100
    # get area per lipid by dividing num lipids per leaflet
    area = area/144
    return area

def area_per_lipid(numlipids, inputlist1, inputlist2):

    area1 = get_areas(inputlist1)
    if inputlist2 is not None:
        area2 = get_areas(inputlist2)

    plt.plot(area1)
    if inputlist2 is not None:
        plt.plot(area2)
    plt.show()

    area1 = calc_lipid_area(area1)
    if inputlist2 is not None:
        area2 = calc_lipid_area(area2)

    plt.hist(area1,50,range=(0.64,0.70), alpha=0.5)
    if inputlist2 is not None:
        plt.hist(area2,50,range=(0.64,0.70), alpha=0.5)
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile1", required=True, nargs='+',
                        help="Name of xst file(s) from NAMD. Can list one or more, corresponding to same simulation.")
    parser.add_argument("-j", "--infile2", nargs='+',
                        help="(optional) Name of xst file(s) from NAMD to be compared with infile1. Can list one or more, corresponding to same simulation.")
    parser.add_argument("-n", "--numlipids", type=int,
                        help="Number of lipids per leaflet, to calculate area per lipid.")
#    parser.add_argument("-o", "--output",action="store_true",default=False,
#                        help="Write output as comments at end of file?")

    args = parser.parse_args()
    area_per_lipid(args.numlipids, args.infile1, args.infile2)

