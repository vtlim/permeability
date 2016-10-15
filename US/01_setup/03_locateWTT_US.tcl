# Purpose: to find last frame of dcd when WTT is in [lowerB, upperB].
# Modified from ABF script for use with US (loop range, tolerance, xsc, etc.)
# Usage: Update settings, then "vmdt -e file.tcl"
# Note: Script loops over trajectory 1x, and for each frame, sees where it can
#       write out a matching pdb for coords. 


# ============= Things to change before using ============= #

# max and minimum distance of the permeant to the center (A)
# KEEP THIS CONSTANT for all windows in A SET of US simulations.
# DON'T FORGET TO MANUALLY CHG BOUNDARIES IN USCONFIG FILE
set max 44
set min -8
set tol 0.25      ;# find WTT, +- this distance (A)

### Input files 
#set trjfile /pub/limvt/pmf/05_prod2/npt_02.dcd
set trjfile /pub/limvt/pmf/06_abf/win06-noMin/01_run1/abf.win06.01.dcd
#set trjlimit 0
set trjlimit 5000   ;# minimum frame to start (x ns * 500) (0;5000)

# skip every nth frame reading in for dopbc
# for 2 fs/step with 1000 frames/step, that's 2 ps/frame
set skip 1

set psffile /pub/limvt/pmf/00_reference/chipot_box.psf
set readme /pub/limvt/pmf/07_us/README
cd /pub/limvt/pmf/07_us/windows

# ========================================================== #

#lappend auto_path /home/victoria/Documents/tempotools/libs
package require tempoUserVMD
set ldist {} ;# for exploration/debugging purposes

# read in PSF (yes needed)
# don't "animate read dcd" with "dopbc" else will have both dcds
mol new $psffile
dopbc -file $trjfile -frames $trjlimit:$skip:-1

# create selections
set wtt [atomselect top "segname WTT and name OH2"]
set lip [atomselect top "lipid and name C21 C31"]

# loop over frames backwards n-1,...,2,1
set n [expr {[molinfo top get numframes]-1}]
for {set i $n} {$i > 0} {incr i -1} {

    # update frames and selections
    $wtt frame $i
    $lip frame $i

    # subtract z coords: water - center of mass of lipids
    set dist [expr {[$wtt get z] - [lindex [measure center $lip] 2]}]
    #lappend ldist [format "%.3f" $dist]

    for {set j $max} {$j >= $min} {incr j -1} {

        # sort the written out pdbs into their respective folders (+/-)
        if {$j >= 0 && $j < 10} {
            set dirj 0$j
        } elseif {$j >= 0 && $j >= 10} {
            set dirj $j 
        } else { 
            set dirj [expr { abs($j)+ $max }] ;# may need to chg $max
        }

        set output ${dirj}/us.win${dirj}.pdb

        # loop over all desired windows, and write out the match
        if {[expr abs($dist - $j) < $tol] && ![file exists $output]} {

            puts "$j    [format "%.3f" $dist]"            
            animate write pdb ${dirj}/us.win${dirj}.pdb beg $i end $i skip 1 0
            
            # variables to print out in README file
            set pdb [lindex [split $trjfile /] end]
            set frm [expr $i * $skip + $trjlimit]
            set timestamp [clock format [clock seconds]]        
            set newline "$dirj\t$pdb\t\t$frm\t\t$dist\t\t$timestamp"
            
            # append README file with the newest selection
            set f [open $readme a]
            puts $f $newline
            close $f

        }
    }
}
#puts $ldist
exit ;# this exit means go through ALL frames then exit...
