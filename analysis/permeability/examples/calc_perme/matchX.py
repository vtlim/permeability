#!/usr/bin/env python

"""
Usage:   python matchX.py -i file1.in -j file2.in -r file1.in

Purpose: Match two sets of XY data based on most similar X-values.
         This can be used for when data comes from different sources,
         but there needs to be a 1:1 correspondence for further calculations.
Assumes:
- No repeated x in either dataset.

"""

import numpy as np


infile1 = "source/water_1.csv"
infile2 = "source/water_2.csv"
reffile = infile1
# check that reference file is one of the input files
# TODO read in a third reference file if desired

data1 = np.genfromtxt(infile1, delimiter=',')
data2 = np.genfromtxt(infile2, delimiter=',')
x1 = data1[:,0]
x2 = data2[:,0]
y1 = data1[:,1]
y2 = data2[:,1]

# assign which is reference and which is other
refx = x1
otrx = x2
if reffile == infile2:
    refx = x2
    otrx = x1

print("The reference file has {} x-values, and the other file has {} x-values.".format(len(refx),len(otrx)))





def find_nearest(array, value):
    """
    https://tinyurl.com/yc7twjx8

    Returns five indices for matching values from "array" to "value",
    sorted from best match to worst match.

    """
    array = np.asarray(array)
    idxs = np.argsort(np.abs(array - value))[:5]
    return idxs

def find_match(refx, otrx, otr_inds_to_keep):
    refx_to_redo = []
    for a in refx:
        idxs = find_nearest(otrx, a)
        print(idxs)

        i = 0
        while i < 5:
            idx_in_question = idxs[i]
            # if index isn't already there, we can append skip the while loop
            if idxs[i] not in otr_inds_to_keep:
                break
            # compare which x-value is closer
            ref_x = a
            now_x = otrx[idx_in_question]
            old_x = otrx[otr_inds_to_keep.index(idx_in_question)]

            # if the old x value is further, then new x index stays
            # remove old x's index spot and mark the old one to redo
            if old_x-ref_x > now_x-ref_x:
                refx_to_redo.append(old_x)
                otr_inds_to_keep.remove(idx_in_question)
                break
            # but if old x is closer, try again to match new x
            print("trying again...")
            i+=1

        print("adding match for {} and {} as index {}\n".format(a,otrx[idx_in_question],idxs[i]))
        otr_inds_to_keep.append(idxs[i])
    return otr_inds_to_keep, refx_to_redo


otr_inds_to_keep = []
final_answer = [] # 2D list
refx_to_do = refx
k = 0

while len(refx_to_do) > 0:
    otr_inds_to_keep, refx_to_do = find_match(refx_to_do,otrx,otr_inds_to_keep)
    final_answer.append(otr_inds_to_keep)
    print("Iteration {} found {} matches. {} x-values left to match.".format(k, len(final_answer[k]), len(refx_to_do)))

print(final_answer)


