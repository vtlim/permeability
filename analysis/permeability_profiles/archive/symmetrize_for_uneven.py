#!/usr/bin/env python

"""
Usage: python symmetrize_for_uneven.py -i profile.in [-c weights.dat] [--anti] -o output

Purpose: Symmetrize given data (e.g., diffusivity, PMF) across x-value of zero.
         Takes into account weighted averages, if weights (counts of data at
         each grid point) are input.

Formula: For some profile D(x), weights N(x), and grid point xi:

             D_sym(xi) = [N(xi)*D(xi) + N(-xi)*D(-xi)]
                         -----------------------------
                                N(xi) + N(-xi)

By:         Victoria T. Lim
Version:    Oct 31 2018
Reference:  10.1021/ct400925s

Notes:
- DID NOT RETURN CORRECT MAGNITUDE OF VALUES ON EVEN LENGTH DATA ON
  MEMBRANE DENSITY PROFILES; VERIFY BEFORE USING
- this script was written to handle symmetrization when the RHS data
  was considerably longer than the LHS data
- colvar = collective variable, referring to x-value
- If your input data is the GRADIENT of the PMF, such as from adaptive biasing
  force, make sure to include the --anti flag. This changes the numerator of
  the above formula to [N(xi)*D(xi) - N(-xi)*D(-xi)], because you need to
  ANTIsymmetrize(grad(PMF)) in order to get symmetrized(PMF) after integration.

"""

import os, sys
import numpy as np
from scipy import integrate


def main(**kwargs):

    def initiate_indices(longest_side_length, z0, zero_present):
        """
        Define start and end range for looping through to (anti)symmetrize
        input data. The idea is to start from the profile's zero-value,
        and work out to the end of the profile. This function takes into
        account that the zero-value may not be at the beginning, middle,
        or end of the input data.

        Parameters
        ----------
        longest_side_length : int
            Number of items from zero-value to end of profile.
        z0 : int
            The index for the zero-value in the input data.
        zero_present : Bool
            Is the z0 value the actual center, or is it a skewed
            center? E.g. if input data has ..., -0.10, -0.05, 0.05, 0.10, ...
            True for actual zero value, False otherwise.

        Returns
        -------

        """
        sym_array = np.zeros([longest_side_length], np.float64)
        if zero_present:
            neg_i = z0-1
            pos_i = z0+1
            loopstart = 1
            loopend = longest_side_length
        else:
            neg_i = z0
            pos_i = z0+1
            loopstart = 0
            loopend = longest_side_length - 1
        return sym_array, neg_i, pos_i, loopstart, loopend

    # load data and check that they have the same colvar grid.
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

    # find index where colvar changes sign (symmetrize around this point)
    # z0 is where colvar=0 if present, else will be the negative colvar closest to 0
    zero_present = False
    z0 = np.where(colvar_values <= 0)[0][-1]
    if colvar_values[z0] == 0:
        zero_present = True

    # get the length of data points on the longest side
    longest_side_length = max(z0, length-z0)
    longer = "right"
    if longest_side_length == z0:
        longer = "left"
    longer_by = longest_side_length-z0

    # initiate indices for symmetrization
    sym_grads, neg_i, pos_i, loopstart, loopend = initiate_indices(longest_side_length, z0, zero_present)
    if zero_present:
        sym_grads[0] = grads[z0]

    # loop from zero to max edge, symmetrizing
    for i in range(loopstart, loopend):

        # handle cases that can't be symmetrized: (1) colvar=0, (2) no data on one side
        # zero case can be combined with one of others but written out for clarity
        if neg_i < 0:
            sym_grads[i] = grads[pos_i]
        elif pos_i > len(colvar_values):
            sym_grads[i] = grads[neg_i]
        else:
            if args.anti:
                # based on eq. on p.558 of reference
                top_frac = counts[pos_i]*grads[pos_i] - counts[neg_i]*grads[neg_i]
            else:
                top_frac = counts[pos_i]*grads[pos_i] + counts[neg_i]*grads[neg_i]
            bot_frac = counts[pos_i] + counts[neg_i]
            sym_grads[i] = top_frac / bot_frac

        neg_i -= 1
        pos_i += 1


    # propagate error values if present
    ### TODO: this section is a bit redundant from the one above.
    if with_err:
        sym_stds, neg_i, pos_i, loopstart, loopend = initiate_indices(longest_side_length, z0, zero_present)
        if zero_present:
            sym_stds[0] = stds[z0]
        for i in range(loopstart, loopend):
            if neg_i < 0:
                sym_stds[i] = stds[pos_i]
            elif pos_i > len(colvar_values):
                sym_stds[i] = stds[neg_i]
            else:
                sym_stds[i] = np.sqrt(np.square(stds[pos_i]) + np.square(stds[neg_i]))
            neg_i -= 1
            pos_i += 1

    # extract part of colvar array from zero-value-cv out to longest edge
    if longer == "right":
        half_cvs = colvar_values[z0:] # 0 to 43.9
    else:
        half_cvs = colvar_values[:z0]  # untested

    # integrate the anti-symmetrized gradients
    if args.anti:

        # write out the counts-weighted and ANTI-symmetrized gradients.
        # gradients written out here bc the full gradient is never computed.
        # pmf is computed from what grad data is avail, then is symmetrized.
        gfile = os.path.splitext(args.outfile)[0]+'.grad'
        with open(gfile,'w') as f:
            f.write("# Input profile: {}\n# Input .count file: {}".format(args.infile, args.cfile))
            f.write("\n\n# Anti-symmetrized profile\n")
            np.savetxt(f, np.c_[half_cvs,sym_grads], delimiter='\t', fmt=['%.2f','%.6f'])

        if with_err:
            sys.exit("ERROR: error propagation not yet supported for gradient data")

        # trapezoid rule for integration
        int_pmf = integrate.cumtrapz(sym_grads, half_cvs)

        # take midpoint of all adjacent data points in half_cvs due to integration
        # https://tinyurl.com/ycahltpp
        half_cvs = (half_cvs[1:] + half_cvs[:-1]) / 2
        longest_side_length -= 1

    else:
        int_pmf = sym_grads


    # transform colvar unit from Angstroms to nanometers.
    cv_unit = "A"
#    cv_unit = "nm"
#    half_cvs = 0.1*half_cvs

    # generate the other half by mirroring
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
            if with_err:
                full_std[i] = sym_stds[longest_side_length-1-i]
        else:                         # positive value colvars
            full_cvs[i] = half_cvs[i-longest_side_length]
            full_pmf[i] = int_pmf[i-longest_side_length]
            if with_err:
                full_std[i] = sym_stds[i-longest_side_length]

    # if there is no zero-value colvars, remove the extraneous (-)0.0 value
    # TODO since [only tested for when RHS is longer]
    full_cvs = np.delete(full_cvs,longest_side_length-1)
    full_pmf = np.delete(full_pmf,longest_side_length-1)
    if with_err:
        full_std = np.delete(full_std,longest_side_length-1)
    full_length = len(full_cvs)

    # write out symmetrized profile
    with open(args.outfile,'w') as f:
        f.write("# Input profile: {}\n# Input .count file: {}".format(args.infile, args.cfile))
        f.write("\n# Number of data points: {}\n# Zero-based index of the zero-value colvar: {}".format(length, z0))
        f.write("\n# The {} hand side of the profile is longer by {} data points.".format(longer, longer_by))
        f.write("\n# Number of data points on longer edge: {}".format(longest_side_length))
        f.write("\n\n\n# Symmetrized profile (x units of {}, y units unchanged)\n".format(cv_unit))
        if not with_err:
            #f.write("\n\t{} {}".format(full_cvs[i], full_pmf[i]))
            np.savetxt(f, np.c_[full_cvs,full_pmf], delimiter='\t', fmt=['%.2f','%.15f'])
        else:
            #f.write("\n\t{} {} {}".format(full_cvs[i], full_pmf[i], full_std[i]))
            np.savetxt(f, np.c_[full_cvs,full_pmf,full_std], delimiter='\t', fmt=['%.2f','%.15f','%.15f'])



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile", required=True,
                        help="Filename of data to be symmetrized.")

    parser.add_argument("-c", "--cfile",
                        help="Filename of ABF .count suffix with total number"
                             " of samples collected per grid point.")

    parser.add_argument("-a", "--anti", action="store_true", default=False,
                        help="Anti-symmetrize the input (gradient of pmf) then"
                             " integrate to get PMF.")

    parser.add_argument("-o", "--outfile", required=True,
                        help="Name of the output file.")

    args = parser.parse_args()
    opt = vars(args)
    if os.path.exists(args.outfile):
        sys.exit("ERROR: output file already exists")
    main(**opt)

