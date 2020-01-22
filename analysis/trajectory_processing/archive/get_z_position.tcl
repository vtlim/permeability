
# Purpose:  Print out z-position of permeant throughout trajectory.
# Usage:    vmd -dispdev none -e get_z_position.tcl -args input.psf input.dcd output.dat
# By:       Victoria T. Lim
# Version:  Dec 3 2018
# TODO:     [1] Change hard-coded variables to command line arguments


package require tempoUserVMD

# ------ User-defined variables -------- # CHECK ME

set maxframe 4999
set skip 10
set tagsel "oxygen and segname WTT"

# -------------------------------------- #

set mypsf [lindex $argv 0]
set mydcd [lindex $argv 1]
set myout [lindex $argv 2]

# load system
mol new $mypsf
dopbc -file $mydcd -frames 0:$skip:$maxframe -sel lipid

# center by carbonyl atoms of lipids
centering -mol top -ref "name C21 C31"

# prepare output file
set sel [atomselect top "$tagsel"]
set idf [open $myout w]
puts $idf "# Input PSF: $mypsf\n# Input DCD, skip $skip: $mydcd\n"
puts $idf "# Tagged selection: $tagsel"

# write out tagged selection's z-positions
set num_steps [molinfo 0 get numframes]
for {set i 0} {$i < $num_steps} {incr i} {
    $sel frame $i
    puts $idf "$i [$sel get z]"
}

