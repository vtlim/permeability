#!/usr/bin/env python

# Purpose: generate WHAM input file for use in Grossfield WHAM.
#   This is pseudo-command-line script. Change base parameters from US
#   US simulations and for WHAM parameters. Then use command line
#   inputs to specify whether to use subset of data and start / end time (ns). 
# Usage, for subset:    python file.py --portion True --begin 0 --end 13
# Usage, for all data:  python file.py --portion False --begin 0 --end <largesttime>

import os
import glob


# ==================================================

### Parameters from US simulations
winstart = 0
winend = 52
minZ = -8.0
maxZ = 44.0
spring = 1.5


### WHAM parameters
numbins = 180
tolerance = 0.0001
temp = 308.0
padding = 0


os.chdir('/pub/limvt/pmf/07_us/02_analysis/trajfiles')

# ==================================================

def GenInput(usePortion, startns, stopns, shortprefix):
    if startns != 0:
        time1 = (1000*startns/2)+1
    else:
        time1 = startns
    time2 = (1000*stopns/2)

    ### Output file names
    wham = "WHAM-INPUT_%d-%dns" % (startns, stopns)
    pmf = "US_%d-%dns.pmf" % (startns, stopns)
    
    ### open and read traj files 
    for f in glob.glob('win*traj'):
        inf = open(f, 'r')
        lines = inf.readlines()
        inf.close()
    
        ### write out subset of each traj file
        if usePortion: 
            trajout = "%d-%dns_%s.traj" % (startns, stopns, f.split('.')[0])
            if not os.path.exists(trajout):
                outf = open(trajout, 'w')
                subset = lines[time1:time2]
                for i in subset:
                    outf.write(str(i))
                outf.close()
    
    ### open and write WHAM input file header
    fname = os.path.join('../03_wham',wham)
    if not os.path.exists(fname):
        whamf = open(fname, 'w')
    else:
        print("WHAM input file already exists: %s" % fname)
        quit()
    whamf.write("### wham %f %f %d %f %f %f %s %s" % (minZ, maxZ, numbins, tolerance, temp, padding, wham, pmf))
    whamf.write("\n### /path/to/timeseries/file loc_win_min spring [correl time] [temp]")
    whamf.write("\n###")
    
    i = winstart
    while i <= winend:
        ### set values for window number and wtt center
        if i < maxZ and i < 10:
            win = '0'+str(i)
            cent = str(i)
        elif i <= maxZ and i >= 10:
            win = str(i)
            cent = str(i)
        else:
            win = str(i)
            cent = str(maxZ-i)
    
        if usePortion:
            trajout = '%d-%dns_win%s.traj' % (startns, stopns, win)
    
            ### use prespecified files for some windows that ran for less time
            if os.stat(trajout).st_size == 0:
                trajout = '%s_win%s.traj' % (shortprefix, win)
                if os.stat(trajout).st_size == 0:
                    print("ALERT: %s in WHAM input is an empty file" % trajout)
        else:
            trajout = 'win%s.traj' % win   
        print trajout
    
        ### don't write to WHAM if the window didn't finish
        if not os.path.exists(trajout):
            print "No *.traj output for WHAM for %s" % (trajout)
            i += 1
            continue
    
        whamf.write("\n../trajfiles/%s %s %f" % (trajout, cent, spring))
        i += 1
    whamf.close()

# ------------------------- Parse Command Line Inputs ----------------------- #
if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option('-p', '--portion',
            help = "Do you want to only use part of the data? E.g. to plot evolution of PMF over successive times.",
            default = False,
            #type = "string", # can't use type boolean in parser (?)
            dest = 'usePortion')

    parser.add_option('-b','--begin',
            help = "Integer start time in nanoseconds. Assumes step*2 / 1e6 = time ns.",
            default = 0,
            type = "int",
            dest = 'startns')

    parser.add_option('-e', '--end',
            help = "Integer stop time in nanoseconds. Assumes step*2 / 1e6 = time ns.",
            default = 10000000000000000,
            type = "int",
            dest = 'stopns')

    parser.add_option('-x', '--prefix',
            help = "If you want subset of data, but data subset file is empty, \
write this prefix data file to WHAM input instead. \
Look for warning msgs if this is empty too.",
            default = None,
            type = "string",
            dest = 'shortprefix')

    (opt, args) = parser.parse_args()
    #usePortion = opt.usePortion.lower() in ("true", "True", "TRUE")
    GenInput(opt.usePortion, opt.startns, opt.stopns, opt.shortprefix)
