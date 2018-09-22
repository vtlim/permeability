#!/usr/bin/env python

"""
Example:    python calc_diffuse_blockavg.py -w 5 -i win05.traj -t 0.002

Purpose:    Calculate the correlation time of some time series from the variance
            of the mean as well as the interval of the time series. This applies
            Hummer's derivation based on overdamped Langevin dynamics
            (aka using harmonically restrained positions from umbrella sampling).

References:
 1. This approach was referenced in a Rowley paper:     10.1016/j.bbamem.2015.12.014
 2. The method was presented by Zhu and Hummer:         10.1021/ct2009279
 3. The method makes use of block averaging:            10.1063/1.457480
 4. The block averaging code is from: https://github.com/manoharan-lab/flyvbjerg-std-err

Version:    Sep 20 2018
By:         Victoria T. Lim

Example of full membrane calculation:
 * for k in {-08..-01}; do i=`expr $k - 44`; j=$((-1 * $i)); echo $j; python calc_diffuse_blockavg.py -w $k -i /pub/limvt/pmf/07_us/02_analysis/trajfiles-26ns/win$j.traj -t 0.002 >> diffuse_26ns.dat; done
 * for k in {00..44}; do echo $k; python calc_diffuse_blockavg.py -w $k -i /pub/limvt/pmf/07_us/02_analysis/trajfiles-26ns/win$k.traj -t 0.002 >> diffuse_26ns.dat; done


"""

import numpy as np
from flyvbjerg_petersen_std_err import fp_stderr

data = np.random.randn(1000)
err = fp_stderr(data)

def main(**kwargs):
    data = np.loadtxt(args.infile)
    colvars = data[:,0]
    positions = data[:,1]

    # calculate variance of data
    var = np.var(positions)

    # calculate variance of the mean
    varbar = fp_stderr(positions)

    # calculate tau (eq. 20 of ref 1)
    n = len(positions)
    term1 = (n*varbar/var)-1
    term2 = args.dt/2
    tau = term1 * term2

    # calculate diffusivity (eq. 17 of ref 1)
    dif = var**2./tau

    # output results
#    print("# Diffusivities, using estimate of correlation time from block averaging")
#    print("\n# Window\tDiffusivity")
    print("\t{}\t{}".format(args.window, dif))


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--window",
                        help="Location of the collective variable (z-position) "
                             "in units of Angstroms. For labeling only.")
    parser.add_argument("-i", "--infile",required=True,
                        help="Filename with the timeseries of harmonically "
                             "restrained positions in units of Angstroms.")
    parser.add_argument("-t", "--dt", type=float,required=True,
                        help="Interval of time series data points in units of "
                             "nanoseconds.")

    args = parser.parse_args()
    opt = vars(args)
    main(**opt)


