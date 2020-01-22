#!/usr/bin/env python

"""
THIS SCRIPT IS STILL A WORK IN PROGRESS, STILL TO BE VERIFIED

By:      Victoria T. Lim
Version: Oct 31 2018

Usage:   python pmf_error.py -i file1.grad -j file2.grad -o pmf_error.dat

Purpose: Compute the error of the potential of mean force from adaptive
         biasing force simulations. This script follows the procedure described
         in the SI of the listed reference.

Note:    This script should behave similar to abfCheckRunsError.tcl but takes
         in merged gradient files. Can still use the Tcl script to separate
         first and second halves of each window pre-merging. So the idea
         is: (1) separate in half, (2) merge each half, (3) send to here.
         Shouldn't need pmf_shift.py since only evaluating integral(grad).

Reference: https://www.nature.com/articles/srep35913

"""

import sys
import numpy as np
from scipy import integrate



def main(**kwargs):

    # load data from files
    data1 = np.loadtxt(args.infile1)
    data2 = np.loadtxt(args.infile2)
    x1 = data1[:,0]
    x2 = data2[:,0]
    y1 = data1[:,1]
    y2 = data2[:,1]
    if not np.array_equal(x1,x2):
        sys.exit("ERROR: collective variable grid of both grad files do not match")

    # obtain uncertainty in final gradient by abs(secondHalf-firstHalf)/2
    err_grad = np.abs(y2-y1)/2
#    print(err_grad)

    # integrate square(err_grad), defining bulk water edge to be zero error
    err_grad_sqr = np.square(err_grad)
#    print(err_grad_sqr)
    #err_int = integrate.cumtrapz(np.flipud(err_grad_sqr),x1)
    err_int = integrate.cumtrapz(err_grad_sqr,x1)
#    print(err_int)
    err_final = np.sqrt(err_int)
    err_final = np.flipud(err_final)
#    print(err_final)

    # take midpoint of all adjacent data points in half_cvs due to integration
    # https://tinyurl.com/ycahltpp
    x_final = (x1[1:] + x1[:-1]) / 2

    with open('pmf-sym.err','w') as f:
        np.savetxt(f, np.c_[x_final, err_final], delimiter='\t', fmt=['%.2f','%.15f'])


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile1", required=True,
                        help="File with mean gradients from the FIRST half"
                        " of the simulations.")

    parser.add_argument("-j", "--infile2", required=True,
                        help="File with mean gradients from the SECOND half"
                        " of the simulations.")

    parser.add_argument("-o", "--outfile", default='pmf_error.dat',
                        help="Name of the output file with error in the PMF.")

    args = parser.parse_args()
    opt = vars(args)
    main(**opt)

