

import numpy as np
import numpy_indexed as npi
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

        # prepare names of other files
        zgradfile = g.replace(".grad",".zgrad")
        countfile = g.replace(".grad",".count")
        zcountfile = g.replace(".grad",".zcount")

        # import data
        # Note: x-axis always same per window. Can be overwritten.
        x_raw, grad_raw = np.split(np.loadtxt(g), 2, 1)
        x_raw, zgrad_raw = np.split(np.loadtxt(zgradfile), 2, 1)
        x_raw, count_raw = np.split(np.loadtxt(countfile), 2, 1)
        x_raw, zcount_raw = np.split(np.loadtxt(zcountfile), 2, 1)

        # store this window's data to larger list
        xlist.append(x_raw)
        gradlist.append(grad_raw)
        zgradlist.append(zgrad_raw)
        countlist.append(count_raw)
        zcountlist.append(zcount_raw)


    ## Averaging
    # https://stackoverflow.com/questions/41821539/calculate-average-of-y-values-with-different-x-values

    # concatenate list to numpy array
    x = np.concatenate(xlist)
    grad = np.concatenate(gradlist)
    zgrad = np.concatenate(zgradlist)
    count = np.concatenate(countlist)
    zcount = np.concatenate(zcountlist)

    # weight grad and zgrad by count and zcount respectively
    weight_grad = np.multiply(grad, count)
    weight_zgrad = np.multiply(zgrad, zcount)

    # average the values having same x gridpoint
    x_unique, grad_mean =   npi.group_by(x).sum(weight_grad)
    x_unique, zgrad_mean =  npi.group_by(x).sum(weight_zgrad)
    x_unique, count_mean =  npi.group_by(x).mean(count)
    x_unique, zcount_mean = npi.group_by(x).mean(zcount)

    # divide by numcounts to complete weighted avg for .grad and .zgrad
    x_unique, count_sum =  npi.group_by(x).sum(count)
    x_unique, zcount_sum = npi.group_by(x).sum(zcount)
    grad_mean = grad_mean/count_sum
    zgrad_mean = zgrad_mean/zcount_sum

    # make sure data are sorted by x in ascending order
    # if you want descending, add [::-1] after arr1inds
    arr1inds = np.concatenate(x_unique).argsort()
    sort_x_unique = x_unique[arr1inds]
    sort_grad_mean = grad_mean[arr1inds]
    sort_zgrad_mean = zgrad_mean[arr1inds]
    sort_count_mean = count_mean[arr1inds]
    sort_zcount_mean = zcount_mean[arr1inds]

    ## Save data
    header = '# 1\n#    -40    0.1    440    0\n'
    fmtf = '%.2f  %.6f'
    fmtd = '%.2f  %d'
    np.savetxt('averaged.grad', np.hstack([  sort_x_unique, sort_grad_mean  ]), header=header, comments='', fmt=fmtf)
    np.savetxt('averaged.zgrad', np.hstack([ sort_x_unique, sort_zgrad_mean ]), header=header, comments='', fmt=fmtf)
    np.savetxt('averaged.count', np.hstack([ sort_x_unique, sort_count_mean ]), header=header, comments='', fmt=fmtd)
    np.savetxt('averaged.zcount', np.hstack([sort_x_unique, sort_zcount_mean]), header=header, comments='', fmt=fmtd)

