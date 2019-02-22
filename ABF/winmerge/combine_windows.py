

import numpy as np
import numpy_indexed as npi
from scipy import integrate
import sys


if __name__ == '__main__':

    ## Data Import
    xlist = []
    gradlist = []
    zgradlist = []
    countlist = []
    zcountlist = []

    for i, g in enumerate(sys.argv[1:]):
        print("Loading file {}.".format(g))

        # import data
        x_raw, grad_raw = np.split(np.loadtxt(g), 2, 1)

        # store this window's data to larger list
        xlist.append(x_raw)
        gradlist.append(grad_raw)

    ## Averaging
    # https://stackoverflow.com/questions/41821539/calculate-average-of-y-values-with-different-x-values

    # concatenate list to numpy array
    x = np.concatenate(xlist)
    grad = np.concatenate(gradlist)

    # average the values having same x gridpoint
    x_unique, grad_mean =   npi.group_by(x).sum(grad)

    # make sure data are sorted by x in ascending order
    # if you want descending, add [::-1] after arr1inds
    arr1inds = np.concatenate(x_unique).argsort()
    sort_x_unique = x_unique[arr1inds]
    sort_grad_mean = grad_mean[arr1inds]

    ## Integrating
    y_pmf = integrate.cumtrapz(sort_grad_mean.flatten(), sort_x_unique.flatten())
    # take midpoint of all adjacent data points in half_cvs due to integration
    # https://tinyurl.com/ycahltpp
    x_pmf = (sort_x_unique[1:] + sort_x_unique[:-1]) / 2
    x_pmf = x_pmf.flatten()

    ## Save data
    fmtf = '%.2f  %.6f'
    fmtd = '%.2f  %d'


    # save averaged grad and pmf
    header = '# Input files: {}\n'.format(sys.argv[1:])
    np.savetxt('averaged.czar.grad', np.hstack([ sort_x_unique, sort_grad_mean  ]), header=header, comments='', fmt=fmtf)
    np.savetxt('averaged.pmf',       np.vstack(( x_pmf, y_pmf )).T,                   header=header, comments='', fmt=fmtf)

