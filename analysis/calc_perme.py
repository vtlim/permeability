#!/usr/bin/env python

"""
Usage: python calc_perme.py -p pmf.dat -d diffuse.dat -t 295.0 > output.dat

Purpose: Compute membrane permeability from potential of mean force and
         diffusivity data.
_________________________________________________________________________

Formula: For potential of mean force w(z), diffusivity D(z), box size L:

                             1              L/2       exp[+beta w(z)]
         resistivity = --------------  int   |   dz  -----------------
                        permeability       -L/2            D(z)

_________________________________________________________________________

By:         Victoria T. Lim
Version:    Sep 20 2018
Reference:  10.1021/ct400925s

TODO:
- be able to carry out error propagation

"""

import sys
import numpy as np

def main(**kwargs):

    ### Load data and check that they have the same colvar grid.
    file_pmf  = np.loadtxt(args.pmf)
    file_dif  = np.loadtxt(args.dif)
    pmf =  file_pmf[:,1]
    dif =  file_dif[:,1]
    colvar_values =  file_pmf[:,0]
    colvar_values1 = file_dif[:,0]
    if not np.array_equal(colvar_values,colvar_values1):
        sys.exit("ERROR: collective variable grid of .count and .grad files do not match")

    ### Calculate thermodynamic beta.
    kb = 0.0019872041     # units of kcal/(mol.K), https://tinyurl.com/y8f7sse7
    beta = 1./(kb*args.temp)

    ### Compute the permeability.
    beta_pmf = beta*pmf
    exp_pmf = np.exp(beta_pmf)
    quotient = exp_pmf / dif
    #resist = np.sum(quotient)
    resist = np.trapz(quotient, colvar_values)
    perme = 1./resist
    print("\n\tPermeability = {} Angstrom/ns".format(perme))
    print("\n\tFor ref, water is = 1.36E-3 Angstrom/ns".format(perme))



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--pmf",
                        help="Filename of potential of mean force across full "
                             "membrane. Units should be in kcal/mol.")

    parser.add_argument("-d", "--dif",
                        help="Filename of diffusivity across full membrane. "
                             "Units should be in Angstrom^2/ns.")

    parser.add_argument("-t", "--temp", type=float,
                        help="Temperature in Kelvin")


    args = parser.parse_args()
    opt = vars(args)
    main(**opt)

