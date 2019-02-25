

import numpy as np
import numpy_indexed as npi
import sys


if __name__ == '__main__':

    # TODO: ARGPARSE
    temp = 295

    # Boltzmann constant in kcal/(mol K)
    kb = 0.0019872041
    kt = kb*temp

    x_list = []
    leaf_list = []

    for i, g in enumerate(sys.argv[1:]):
        # import data
        # Note: x-axis SHOULD BE same per window. Can be overwritten.
        print("Loading file {}.".format(g))
        x_raw, leaf_raw = np.split(np.loadtxt(g), 2, 1)
        x_list.append(x_raw)
        leaf_list.append(leaf_raw)


    # concatenate list to numpy array
    x = np.concatenate(x_list)
    pmf_raw = np.concatenate(leaf_list)

    # take boltzmann weight of free energies
    pmf_boltz = np.exp(-1*pmf_raw/kt)

    # sum overlapping regions
    # https://stackoverflow.com/questions/41821539/calculate-average-of-y-values-with-different-x-values
    x_unique, pmf_boltz_sum = npi.group_by(x).sum(pmf_boltz)

    # calculate free energies from boltzmann sum
    pmf_final = -1*kt*np.log(pmf_boltz_sum)

    # make sure data are sorted by x in ascending order
    # if you want descending, add [::-1] after arr1inds
    arr1inds = np.concatenate(x_unique).argsort()
    sort_x_unique = x_unique[arr1inds]
    sort_pmf_final = pmf_final[arr1inds]

    import matplotlib.pyplot as plt
    plt.plot(sort_x_unique, sort_pmf_final)
    plt.grid()
    plt.show()


    ## Save data
    #header = "# Input data: {}".format(args.infile, args.cfile))
    header = "# Input data: {}".format(sys.argv[1:])
    fmtf = '%.2f  %.6f'
    np.savetxt('full_pmf.dat', np.hstack([  sort_x_unique, sort_pmf_final ]), header=header, comments='', fmt=fmtf)

