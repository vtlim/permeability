#!/usr/bin/env python

import sys
import numpy as np

"""
Usage:   python calc_pmf_partition.py -i pmf.dat --z1 '35' --z2 '-35' -t 295

Purpose: Obtain partition coefficients and partition free energies from
         an input potential of mean force for membrane permeation.

Method:  Given a one-dimensional potential of mean force W(z) and two
         specified points in bulk water on opposite sizes of the membrane
         z1 and z2, compute the water-membrane partitioning coefficients as:
                                         _
                                 1      | z2
            K(wat --> mem) =  -------   |     exp [-beta * (W(z) - W(z1))] dz
                              z2 - z1  _| z1

         Then compute the partitioning free energy from wat --> mem as

               dG(wat --> mem) = -kT ln K(wat --> mem)

Version: May 1 2020

By:      Victoria T. Lim

References:
1. Equation from Vorobyov et al.
   - https://pubs.acs.org/doi/10.1021/ct200417p
2. This script was modified from pmf2free.py by Lim et al. See zip file of SI at:
   - https://pubs.acs.org/doi/10.1021/acs.jcim.8b00835
3. Some parts of the script also came from:
   - https://github.com/vtlim/permeability/blob/master/analysis/permeability_profiles/calc_perme.py
4. Useful error propagation guide:
   - https://terpconnect.umd.edu/~toh/models/ErrorPropagation.pdf
5. Python package for uncertainty propagation
   - https://pythonhosted.org/uncertainties/
   - https://kitchingroup.cheme.cmu.edu/pycse/pycse.html

Notes:
- This script does not take into account different dx steps. It assumes that
  the x increment is the same for all (equally spaced windows/bins). To take
  this into account, would have to multiply bin size (deltaX) of each of the
  component exp(-beta*E_i) before summing to do more of a true integral. If
  all dx the same, they would cancel out on numerator/denominator.

"""

def calc_pmf_partition(infile, z1, z2, temperature):
    """
    Parameters
    ----------
    infile : string
        name of input file with potential of mean force (sorted by z)
    z1 : float
        z-coordinate of a point on one side of aqueous solution;
        z1 should be less than z2
    z2 : float
        z-coordinate of a point on other side of aqueous solution;
        should be on opposite side of membrane from z1;
        z2 should be greater than z1
    temperature : float
        used to calculate k_B * T

    """

    # calculate thermodynamic beta
    kb = 0.0019872041     # units of kcal/(mol.K), https://tinyurl.com/y8f7sse7
    beta = 1./(kb*temperature)

    # read in file
    data = np.loadtxt(infile).T
    z_crd = data[0]
    pmf = data[1]
    num_cols = data.shape[0]

    # column with error bars is present (otherwise 2 columns)
    calc_uncert = False
    if num_cols == 3:
        err_bars = data[2]
        calc_uncert = True

    # get the index of the z1 and z2 values
    # result looks like: (array([49]),)
    z1_idx = np.where(np.isclose(z_crd, z1))[0][0]
    z2_idx = np.where(np.isclose(z_crd, z2))[0][0]
    print(f"\nComputing results for PMF in {infile}")
    print(f"Indices within which to calculate PMF: {z1_idx} {z2_idx}\n")

    # truncate pmf to calculate within this range only
    # assumes that input is formatted such that z1 < z2
    # and that input pmf is ordered from low z to high z
    trunc_pmf = pmf[z1_idx : (z2_idx+1)]
    trunc_z = z_crd[z1_idx : (z2_idx+1)]

    # take relative pmf to the z1 value, W(z) - W(z1)
    rel_pmf = trunc_pmf - trunc_pmf[0]

    # scale the relative pmf by -1/kT = -1*beta
    scale_pmf = -1 * rel_pmf * beta

    # take exponent of each value
    exp_pmf = np.exp(scale_pmf)

    # integrate
    integrated = np.trapz(exp_pmf, trunc_z)

    # calculate partition coefficient by scaling by difference of z2 - z1
    denom = (z2 - z1)
    partcoeff = integrated / denom

    # calculate partition free energy from partition coefficient
    # np.log is ln, np.log10 is base 10 log
    dg = (-1/beta) * np.log(partcoeff)

    print(f"partition coefficient  K(wat --> mem) = {partcoeff:.3E}")
    print(f"partition free energy dG(wat --> mem) = {dg:.3E}")

    # NOTE/TODO: this section repeats above section if uncerts are present
    # can add control statements to do one or other only

    if calc_uncert == True:
        import uncertainties as u
        from uncertainties import unumpy

#        # initial attempt at error propagation; was stuck at integral
#
#        def root_sum_sq(err1, err2):
#            # https://stackoverflow.com/a/51077781/8397754
#            return (err1*err1 + err2*err2) ** 0.5
#
#        # (1) calculate root sum square from taking pmf relative to z1
#        first_err = trunc_err[0]
#        rel_pmf_err = np.apply_along_axis(root_sum_sq, 0, trunc_err, first_err)
#
#        # (2) multiplicative constant: ERR_PROP = abs(constant) * err_orig
#        scale_pmf_err = rel_pmf_err * abs(beta)
#
#        # (3) exponential: ERR_PROP = exp(ydata) * err_orig
#        exp_pmf_err = exp_pmf * scale_pmf_err
#
#        # (4) integration: let's have that handled by uncertainties package
#        # example: https://kitchingroup.cheme.cmu.edu/pycse/pycse.html
#        templist = []
#        for v, w in zip(exp_pmf, exp_pmf_err):
#            templist.append( u.ufloat((v, w)) )
#        exp_pmf_with_err = np.array(templist)
#        integrated_u = np.trapz(exp_pmf_with_err, trunc_z)
#
#        # (5) multiplicative constant, scale by denominator
#        partcoeff_u = integrated_u / denom
#
#        # (6) natural log: ERR_PROP = err_orig / ydata
#        dg_u = (-1/beta) * unumpy.log(partcoeff_u)



        # truncate error bars in same way pmf was truncated
        trunc_err = err_bars[z1_idx : (z2_idx+1)]
        templist = []

        # combine data with its uncertainties
        for v, w in zip(trunc_pmf, trunc_err):
            templist.append( u.ufloat((v, w)) )
        trunc_pmf_with_err = np.array(templist)

        # take relative pmf to the z1 value, W(z) - W(z1)
        rel_pmf_with_err = trunc_pmf_with_err - trunc_pmf_with_err[0]

        # scale the relative pmf by -1/kT = -1*beta
        scale_pmf_with_err = -1 * rel_pmf_with_err * beta

        # take exponent of each value
        exp_pmf_with_err = unumpy.exp(scale_pmf_with_err)

        # integrate
        integrated_u = np.trapz(exp_pmf_with_err, trunc_z)

        # calculate partition coefficient by scaling by difference of z2 - z1
        partcoeff_u = integrated_u / denom

        # calculate partition free energy from partition coefficient
        dg_u = (-1/beta) * unumpy.log(partcoeff_u)

        print(f"partition coefficient  K(wat --> mem) = {partcoeff_u}")
        print(f"partition free energy dG(wat --> mem) = {dg_u}\n\n")


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infile", required=True,
                        help="Name of input file with data in columns. First "
                              "column should be z coordinates in order from "
                              "low to high values, second column "
                              "should have pmf values (kcal/mol), and third "
                              "column (optionaly) should have error bars.")

    parser.add_argument("-1", "--z1", type=float,
                        help="Z-coordinate of reference point in aqueous "
                             "solution. PMF is taken relative to this point.")

    parser.add_argument("-2", "--z2", type=float,
                        help="Z-coordinate of reference point in aqueous "
                             "solution on opposite side of membrane from z1. "
                             "Assign z2 such that z1 < z2.")

    parser.add_argument("-t", "--temperature", type=float, default=295.0,
                        help="Temperature (K) to calculate thermodynamic beta."
                             " Default is 295 K.")

    args = parser.parse_args()

    calc_pmf_partition(args.infile, args.z1, args.z2, args.temperature)

