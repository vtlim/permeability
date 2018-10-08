#!/usr/bin/env python

"""
By:      Victoria T. Lim
Version: Oct 03 2018

Usage:   python pmf_shift.py -i pmf-sym.dat -a 40.0 -b 42.0 -o pmf-sym-shift.dat

Purpose: Shift the potential of mean force input data. Do this by calculating
         the mean between two provided x-values, and defining this as zero point.

"""

import numpy as np
import sys

def main(**kwargs):

    # load data from files
    data = np.genfromtxt(args.infile)
    xdata = data[:,0]
    ydata = data[:,1]

    # get indices of the a and b values
    try:
        a_index = np.where(xdata==args.a)[0][0]
        b_index = np.where(xdata==args.b)[0][0]
    except IndexError:
        sys.exit("ERROR: one of the input x-values was either not found or found more than once")

    # calculate the mean of the region
    origmean = np.mean(ydata[min(a_index,b_index):max(a_index,b_index)+1])
    print("The original mean of the region from {} to {} is {}.".format(args.a, args.b, origmean))

    # shift the y-data
    ydata = ydata-origmean

    # write out shifted profile
    np.savetxt(args.outfile, np.c_[xdata,ydata], fmt=['%.2f','%.13f'])


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile", required=True,
                        help="Input data set whose y-values should be shifted")

    parser.add_argument("-a", required=True, type=float,
                        help="One of the x-values to set the zero region")

    parser.add_argument("-b", required=True, type=float,
                        help="The second x-value to set the zero region")

    parser.add_argument("-o", "--outfile", default='shifted.dat',
                        help="Name of output file")

    args = parser.parse_args()
    opt = vars(args)
    main(**opt)

