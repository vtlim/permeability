#!/usr/bin/env python

"""
Usage:   python matchX.py -i file1.in -j file2.in -r file1.in

Purpose: Match two sets of XY data based on most similar X-values.
         This can be used for when data comes from different sources,
         but there needs to be a 1:1 correspondence for further calculations.
Assumes:
- No repeated x in either dataset.
- Data sets are sorted by x-value.
- The first x-value should be INSIDE the range of file2 x-values.

TODO:
- add argument parsing
- read in third file if desired

"""

import numpy as np


infile1 = "source/water_1.csv"
infile2 = "source/water_2.csv"
reffile = infile1
# TODO check that reference file is one of the input files

data1 = np.genfromtxt(infile1, delimiter=',')
data2 = np.genfromtxt(infile2, delimiter=',')
x1 = data1[:,0]
x2 = data2[:,0]
y1 = data1[:,1]
y2 = data2[:,1]

# assign which is reference and which is other
refx = x1
otrx = x2
refy = y1
otry = y2
if reffile == infile2:
    refx = x2
    otrx = x1
    refy = y2
    otry = y1

print("The reference file has {} x-values, and the other file has {} x-values.".format(len(refx),len(otrx)))





def find_nearest(array, value):
    """
    https://tinyurl.com/yc7twjx8

    Returns five indices for matching values from "array" to "value",
    sorted from best match to worst match.

    """
    array = np.asarray(array)
    idxs = np.argsort(np.abs(array - value))[0]
    return idxs

def list_duplicates(seq):
    """
    https://tinyurl.com/y8vb2bzq
    """
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set( x for x in seq if x in seen or seen_add(x) )
    # turn the set into a list (as requested)
    return list( seen_twice )


def find_matches(refx, otrx, verbose=False):

    otr_inds_to_keep = [] # matching file2 index for each file1 x-value

    # get the closest element in file2 that matches file1
    for i, a in enumerate(refx):
        otr_inds_to_keep.append(find_nearest(otrx, a))

    # get the indices that were reported more than once
    dups = list_duplicates(otr_inds_to_keep)

    #
    for d in dups:
        locs = list(i for i,value in enumerate(otr_inds_to_keep) if value == d)
        vals = [refx[i] for i in locs]
        refotr = otrx[d]
        if verbose: print(d, refotr, vals)
        vals = np.abs(np.array(vals)-refotr)
        best_dup = locs[np.argmin(vals)]
        for l in locs:
            if l != best_dup:
                otr_inds_to_keep[l] = None

    return otr_inds_to_keep



otr_inds_to_keep = find_matches(refx,otrx)
leftover = otr_inds_to_keep.count(None)
print("Found {} matches. {} x-values of file1 unmatched.".format(len(otr_inds_to_keep),leftover))

# get indices of none, and remove from original refx
nones = list(i for i,value in enumerate(otr_inds_to_keep) if value is None)
newrefx = [i for j,i in enumerate(refx) if j not in nones]
newrefy = [i for j,i in enumerate(refy) if j not in nones]
otr_inds_to_keep = [i for j,i in enumerate(otr_inds_to_keep) if j not in nones]

# get the values of the matching otrx
newotrx = [otrx[i] for i in otr_inds_to_keep]
newotry = [otry[i] for i in otr_inds_to_keep]

# average the newrefx and newotrx to get roughly unified x values
unifyx = np.average(np.array([newrefx,newotrx]), axis=0)

# save files of matched data points
np.savetxt("source/water_1_short.csv", np.c_[newrefx,newrefy], delimiter=",", fmt='%f')
np.savetxt("source/water_2_short.csv", np.c_[newotrx,newotry], delimiter=",", fmt='%f')

# save files with unified xs and convert xs from nm --> Angstrom
# convert diffusivity ys from nm2/ns --> Angstrom2/ns
np.savetxt("source/water_1_samex_angstrom.csv", np.c_[np.asarray(unifyx)*10.,newrefy], delimiter=",", fmt='%f')
np.savetxt("source/water_2_samex_angstrom.csv", np.c_[np.asarray(unifyx)*10.,np.asarray(newotry)*100.], delimiter=",", fmt='%f')


