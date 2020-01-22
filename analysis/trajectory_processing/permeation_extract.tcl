
# ____________________________________________________________________________________
#
# permeation_extract.tcl
#
# Purpose:  Extract frames where permeant is at a specified z-position, then wrap output simulation in XY plane around permeant.
# Usage  :  vmdt -e permeation_extract.tcl -args inpsf skip z-value dcd1 dcd2 ...
# Example:  vmdt -e permeation_extract.tcl -args 00_reference/popc_tneut.psf 50 30 win01/01/win01.01.dcd win02/01/win02.01.dcd
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
# Version: Nov 19 2019
# ____________________________________________________________________________________

# check these variables before using script
#lappend auto_path /...../tempotools/libs
package require tempoUserVMD

# import wrapXY.tcl
set sourcedir /dfs2/tw/limvt/08_permeate/github/analysis/trajectory_processing
#set sourcedir /home/limvt/Documents/gitperm/analysis/trajectory_processing
source $sourcedir/move_atoms.tcl
source $sourcedir/wrapXY.tcl

# define start and end frames common to all trajectories
set start 0
set end 9999

# define solute atomselection for VMD
set seltxt "resname GBI2"

# set tolerance to find permeant at z+-tol
set tol 1.0

# ____________________________________________________________________________________


# parse command line arguments
set inpsf  [lindex $argv 0]
set inskip [lindex $argv 1]
set zval   [lindex $argv 2]
set index 3
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

# read in system, wrapping with dopbc from tempotools
mol new $inpsf
foreach mydcd $dcdlist {
    dopbc -file $mydcd -frames $start:$inskip:$end
}

# set selections for updating frames
set sel [atomselect top $seltxt]
set all [atomselect top "all"]
set lip [atomselect top "lipid and name C21 C31"]

# set lower and upper bounds
set lower [expr $zval - $tol]
set upper [expr $zval + $tol]

# take notes
set outDataFile [open snapshots.extract a]
puts $outDataFile "# Input PSF: $inpsf\n# Input DCD, skip $inskip: $dcdlist"
puts $outDataFile "# Output trajectory with permeant at z=$zval"
puts $outDataFile "# Distance (A) | Frame"
mkdir tempwrapfiles

# loop through frames to find snapshots of when solute has values at specified z-value
puts "=========== Looking for frames ==========="
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

    # see if the dist is in the region we want
    if { $dist > $lower && $dist < $upper } {

        # note where this frame came from
        puts $outDataFile "$dist $i"

        # shift center of mass of system to origin
        sys_to_zero $all

        # write out temporary pdb file
        animate write pdb tempwrapfiles/$i.pdb beg $i end $i skip 1 0
    }
}
puts $outDataFile "\n"
close $outDataFile

# delete trajectory (mol 0) now that we're done, and reload psf (mol 1)
mol delete 0
mol new $inpsf
set molid 1

# read all frames back in
# glob tempwrapfiles pdbs
puts "=========== Generating summary dcd ==========="
set infiles [glob -directory "tempwrapfiles" -- "*.pdb"]
foreach f $infiles {
    mol addfile $f waitfor all
}

# wrap in XY direction, save, and exit
wrap_in_xy $seltxt $molid
animate write dcd test.dcd waitfor all 1

rm -r tempwrapfiles

exit

