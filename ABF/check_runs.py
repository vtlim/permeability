#!/usr/bin/env python

# Usage:    python check_runs.py
# By:       Victoria T. Lim
# Version:  Dec 7 2018


import glob
import subprocess
import numpy as np

for filename in sorted(glob.iglob('win*/**/a*.out')):
    namd_done = False
    job_success = False

    # not memory efficient for large output files
    lines = list(reversed(open(filename).readlines()))[:5]

    try:
        a = lines[0]
    except IndexError:
        print("error with {}".format(filename))
    if "End of program" in lines[0]:
        namd_done = True
    if "WRITING VELOCITIES" in lines[4]:
        job_success = True

    print("{}\t\tNAMD done: {}\t\tJob success: {}".format(filename, namd_done, job_success))

quit()
for k in range(11):
    win_id = str(k).zfill(2)
    count_files = sorted(glob.iglob('win*/czar_fix/win{}.**.abf1.count'.format(win_id)))

    for f in count_files:
        x, y = np.loadtxt(f, unpack=True)
        print("{}\t\t{}\t\t{}".format(f, min(x), min(y)))
        g = f.replace('count','zcount')
        x, y = np.loadtxt(g, unpack=True)
        print("{}\t\t{}\t\t{}".format(g, min(x), min(y)))

