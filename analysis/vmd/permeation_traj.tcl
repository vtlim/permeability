
# ____________________________________________________________________________________
#
# permeation_traj.tcl
#
# Purpose:  Extract permeant z-position frames from input trajectories, then wrap output simulation in XY plane around permeant.
# Usage  :  vmdt -e permeation_traj.tcl -args inpsf skip dcd1 dcd2 ...
# Example:  vmdt -e permeation_traj.tcl -args 00_reference/popc_tneut.psf 50 win01/01/win01.01.dcd win02/01/win02.01.dcd
#           vmdt here stands for "vmd -dispdev none"
#
# Dependencies
#  1. pbctools VMD package
#  2. move_atoms.tcl
#  3. wrapXY.tcl
#      4. pbchelper.tcl
#
# Assumptions
#  - Only works on rectangular boxes
#  - Grid spacing can only be as fine as single decimal place
#  - Single decimal space also used to locate frames (must be consistent for dict keys)
#  - Wrap system around POPC center of mass
#  - Can create and delete tempwrapfiles subdirectory
#
# By:      Victoria T. Lim
# Version: Nov 9 2018
# ____________________________________________________________________________________

# check these variables before using script

# import wrapXY.tcl
set sourcedir /dfs3/pub/limvt/gitmisc/vmd
set sourcedir ~/connect/hpc/goto-tw/gitmisc/vmd

source $sourcedir/move_atoms.tcl
source $sourcedir/wrapXY.tcl

# define the range (inclusive) for collective variable distance
set maxZ 40
set minZ -41
set spacing 1.0

# define solute atomselection for VMD
set seltxt "resname GBIN"
set high_to_low 1

# ____________________________________________________________________________________


# parse command line arguments
set inpsf  [lindex $argv 0]
set inskip [lindex $argv 1]

set index 2
while {$index < [llength $argv]} {
    lappend dcdlist [lindex $argv $index]
    incr index 1
}

# translate system
proc sys_to_zero {all} {
    set to_be_moved [measure center $all]
    set to_be_moved [vecinvert $to_be_moved]
    moveby $all $to_be_moved
}

# define the grid in a dictionary where keys are grid point, values are if snapshot was found
# https://stackoverflow.com/questions/38435707/how-to-generate-sequence-of-numbers-in-tcl
for {set i 0} true {incr i} {
    set x [expr {$i*$spacing + $minZ}]
    if {$x > $maxZ} break
    set printable [format "%.1f" $x]
    dict set grid $printable 0
}
puts $grid

# read in system
mol new $inpsf
foreach mydcd $dcdlist {
    mol addfile $mydcd first 0 last -1 step $inskip waitfor all molid top
}

# wrap system around bilayer
package require pbctools
pbc wrap -centersel "resname POPC" -center com -compound res -all

# set selections
set sel [atomselect top $seltxt]
set lip [atomselect top "lipid and name C21 C31"]
set all [atomselect top "all"]

# take notes
set outDataFile [open snapshots.wrap w]
puts $outDataFile "# Input PSF: $inpsf\n# Input DCD, skip $inskip: $dcdlist"
puts $outDataFile "# Snapshots from $minZ to $maxZ in increments of $spacing Angstrom\n"
puts $outDataFile "# Distance (A) | Frame"
mkdir tempwrapfiles

# loop through frames to find snapshots of when solute has values at z-grid
set n [expr {[molinfo top get numframes]-1}]
for {set i 0} {$i < $n} {incr i} {

    # update frames and selections
    $sel frame $i
    $lip frame $i
    $all frame $i

    # subtract z coords: (selection) - (center of mass of lipids)
    set dist [expr {[lindex [measure center $sel] 2] - [lindex [measure center $lip] 2]}]

    # pseudo-round by formatting to single decimal place
    set dist [format "%.1f" $dist]

    # see if that dist is one of the grid points
    if { [dict exists $grid $dist] && ![dict get $grid $dist] } {
        puts "=========== Writing out distance: $dist ==========="

        # note where this frame came from
        puts $outDataFile "$dist $i"

        # shift center of mass of system to origin
        sys_to_zero $all

        # write out temporary pdb file
        animate write pdb tempwrapfiles/$dist.pdb beg $i end $i skip 1 0

        # mark this grid as complete
        dict set grid $dist 1
    }
}

# delete trajectory (mol 0) now that we're done, and reload psf (mol 1)
mol delete 0
mol new $inpsf
set molid 1
# probably can make this part a fx bc repeated 2x
set sel [atomselect $molid $seltxt]
set all [atomselect $molid "all"]

if {$high_to_low} {
    # reverse order the dictionary keys
    foreach k [lsort -real -decreasing [dict keys $grid]] {
        if {[dict get $grid $k]==1} {
            puts "=========== Reading in distance: $k ==========="
            mol addfile tempwrapfiles/$k.pdb waitfor all
        }
    }
} else {
    # read all frames back, in order that keys were added
    dict for {k v} $grid {
        if {$v==1} {
            puts "=========== Reading in distance: $k ==========="
            mol addfile tempwrapfiles/$k.pdb waitfor all
        }
    }
}

# wrap in XY direction, save, and exit
wrap_in_xy $seltxt $molid
animate write dcd test.dcd waitfor all 1

rm -r tempwrapfiles
close $outDataFile

exit

