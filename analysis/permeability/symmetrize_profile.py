#!/usr/bin/env python

"""
Usage: python symmetrize_profile.py -i profile.in [-c weights.dat] [--anti] > profile.out

Purpose: Symmetrize given data (e.g., diffusivity, PMF) across x-value of zero.
         Takes into account weighted averages, if weights (counts of data at
         each grid point) are input.

Formula: For some profile D(x), weights N(x), and grid point xi:

             D_sym(xi) = [N(xi)*D(xi) + N(-xi)*D(-xi)]
                         -----------------------------
                                N(xi) + N(-xi)

By:         Victoria T. Lim
Version:    Sep 20 2018
Reference:  10.1021/ct400925s

Notes:
- colvar = collective variable, referring to x-value
- If your input data is the GRADIENT of the PMF, such as from adaptive biasing
  force, make sure to include the --anti flag. This changes the numerator of
  the above formula to [N(xi)*D(xi) - N(-xi)*D(-xi)], because you need to use
  antisymmetrize(grad(PMF)) in order to get symmetrize(PMF) after integration.

"""

import os, sys
import numpy as np
from scipy import integrate


def main(**kwargs):

    ### Load data and check that they have the same colvar grid.
    file_grad  = np.loadtxt(args.infile)
    colvar_values = file_grad[:,0]
    length = len(colvar_values)
    grads =  file_grad[:,1]
    try:
        stds = file_grad[:,2]
        with_err = True
    except IndexError:
        with_err = False

    if args.cfile is not None:
        file_count = np.loadtxt(args.cfile)
        colvar_values1 = file_count[:,0]
        counts = file_count[:,1]
        if not np.array_equal(colvar_values,colvar_values1):
            sys.exit("ERROR: collective variable grid of .count and .grad files do not match")
    else:
        counts = np.ones(length)

    ### Find index where colvar changes sign (symmetrize around this point)
    ### z0 is where colvar=0 if present, else will be the negative colvar closest to 0
    zero_present = False
    z0 = np.where(colvar_values <= 0)[0][-1]
    if colvar_values[z0] == 0:
        zero_present = True

    ### get the length of data points on the longest side
    longest_side_length = max(z0, length-z0)
    longer = "right"
    if longest_side_length == z0:
        longer = "left"
    longer_by = longest_side_length-z0
    print("# Input profile: {}\n# Input .count file: {}".format(args.infile, args.cfile))
    print("# Number of data points: {}\n# Zero-based index of the zero-value colvar: {}".format(length, z0))
    print("# The {} hand side of the profile is longer by {} data points.".format(longer, longer_by))
    print("# Number of data points on longer edge: {}".format(longest_side_length))

    ### Initiate indices for symmetrization
    sym_grads = np.zeros([longest_side_length], np.float64)   # anti-symm gradients
    if zero_present:
        neg_i = z0-1
        pos_i = z0+1
        loopstart = 1
        loopend = longest_side_length
        sym_grads[0] = grads[z0]
    else:
        neg_i = z0
        pos_i = z0+1
        loopstart = 0
        loopend = longest_side_length - 1

    ### loop from zero to max edge, symmetrizing
    for i in range(loopstart, loopend):

        # handle cases that can't be symmetrized: (1) colvar=0, (2) no data on one side
        # zero case can be combined with one of others but written out for clarity
        if neg_i < 0:
            sym_grads[i] = grads[pos_i]
        elif pos_i > len(colvar_values):
            sym_grads[i] = grads[neg_i]
        else:
            if args.anti:
                top_frac = counts[pos_i]*grads[pos_i] - counts[neg_i]*grads[neg_i]
            else:
                top_frac = counts[pos_i]*grads[pos_i] + counts[neg_i]*grads[neg_i]
            bot_frac = counts[pos_i] + counts[neg_i]
            sym_grads[i] = top_frac / bot_frac
            #print(i, top_frac, bot_frac)
            #print(pos_i, counts[pos_i], grads[pos_i], counts[neg_i], grads[neg_i])

        neg_i -= 1
        pos_i += 1

    ### Propagate error values if present
    ### TODO: this section is a bit redundant from the one above.
    if with_err:
        sym_stds = np.zeros([longest_side_length], np.float64)
        if zero_present:
            neg_i = z0-1
            pos_i = z0+1
            loopstart = 1
            sym_stds[0] = stds[z0]
        else:

            neg_i = z0
            pos_i = z0+1
            loopstart = 0
        for i in range(loopstart, loopend):
            if neg_i < 0:
                sym_stds[i] = stds[pos_i]
            elif pos_i > len(colvar_values):
                sym_stds[i] = stds[neg_i]
            else:
                sym_stds[i] = np.sqrt(np.square(stds[pos_i]) + np.square(stds[neg_i]))
            neg_i -= 1
            pos_i += 1

    ### Extract part of colvar array from zero-value-cv out to longest edge
    if longer == "right":
        half_cvs = colvar_values[z0:] # 0 to 43.9
    else:
        half_cvs = colvar_values[:z0]  # untested

    ### Integrate the anti-symmetrized gradients. Trapezoid rule.
    if args.anti:
        if with_err:
            sys.exit("ERROR: error propagation not yet supported for gradient data")
        # reverse list before & after integration bc want zero reference at bulk water
        # whole pmf gets shifted up by around the amount of barrier
        int_pmf = integrate.cumtrapz(sym_grads[::-1], half_cvs[::-1])
        int_pmf = int_pmf[::-1]
        # now readjust half_cvs due to integration by taking midpoints
        # https://tinyurl.com/ycahltpp
        half_cvs = (half_cvs[1:] + half_cvs[:-1]) / 2
        longest_side_length -= 1
    else:
        int_pmf = sym_grads

    ### Transform colvar unit from Angstroms to nanometers.
    cv_unit = "A"
#    cv_unit = "nm"
#    half_cvs = 0.1*half_cvs

    ### Generate the other half by mirroring
    ### TODO: around cv-zero is weird, may repeat a z-value
    full_cvs = np.zeros([2*longest_side_length], np.float64)
    full_pmf = np.zeros([2*longest_side_length], np.float64)
    full_std = np.zeros([2*longest_side_length], np.float64)
    full_length = len(full_cvs)

    for i in range(full_length):
        if not zero_present and i==longest_side_length-1:
            continue
        elif i < longest_side_length: # negative value colvars
            full_cvs[i] = -1*half_cvs[longest_side_length-1-i]
            full_pmf[i] = int_pmf[longest_side_length-1-i]
            if with_err: full_std[i] = sym_stds[longest_side_length-1-i]
        else:                       # positive value colvars
            full_cvs[i] = half_cvs[i-longest_side_length]
            full_pmf[i] = int_pmf[i-longest_side_length]
            if with_err: full_std[i] = sym_stds[i-longest_side_length]

    if not zero_present:
        full_cvs = np.delete(full_cvs,longest_side_length-1)
        full_pmf = np.delete(full_pmf,longest_side_length-1)
        full_length = len(full_cvs)

    ### Write out symmetrized profile
    print("\n\n# Symmetrized profile (x units of {}, y units unchanged)".format(cv_unit))
    for i in range(full_length):
        if not with_err:
            print("\t{} {}".format(full_cvs[i], full_pmf[i]))
        else:
            print("\t{} {} {}".format(full_cvs[i], full_pmf[i], full_std[i]))



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile",required=True,
                        help="Filename of data to be symmetrized.")

    parser.add_argument("-c", "--cfile",
                        help="Filename of ABF .count suffix with total number"
                             " of samples collected per grid point.")

    parser.add_argument("-a", "--anti", action="store_true", default=False,
                        help="Anti-symmetrize the input (gradient of pmf) then"
                             " integrate to get PMF.")

    args = parser.parse_args()
    opt = vars(args)
    main(**opt)

