#!/usr/bin/env python

# Usage:    python check_runs.py
# By:       Victoria T. Lim
# Version:  Dec 7 2018


import glob
import subprocess

for filename in sorted(glob.iglob('win*/**/a*.out')):
    namd_done = False
    job_success = False

    # not memory efficient for large output files
    lines = list(reversed(open(filename).readlines()))[:5]

    if "End of program" in lines[0]:
        namd_done = True
    if "WRITING VELOCITIES" in lines[4]:
        job_success = True

    print("{}\t\tNAMD done: {}\t\tJob success: {}".format(filename, namd_done, job_success))

