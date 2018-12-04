
# Purpose:      Obtain initial coordinates from equil simulations for starting new ABF windows.
# By:           Victoria T. Lim
# Version:      Dec 4 2018
# Usage:        vmdt -e 2_locateWTT.tcl -args file.psf file.dcd windownumber lowerbound upperbound
#               - windownumber should be a positive integer (0 prefix is added by script if the number < 10)
#               - lowerbound/upperbound represents range (Angstrom) of where to find permeant, relative to reference
# Notes:
# [1] Can specify a smaller range (e.g., higher low bound, and lower high bound). Since snapshot is determined
#     from center of mass of permeant, which means that part of the permeant may still be outside the range.


# =============================================================== #
#             Hard-coded variables for multiple use
# =============================================================== #

set skip 10  ;# skip 10 means every 2 ps, given (2 fs/step) and (1000 frames/step)
set outDataFile /dfs2/tw/limvt/08_permeate/taut2/01_prep/pdb_sources.dat

set permeant_text "resname GBI2"
set reference_text "lipid and name C21 C31"

# ========================== Variables ========================= #

set inpsf   [lindex $argv 0]
set indcd   [lindex $argv 1]
set win_num [lindex $argv 2]
set lowerB  [lindex $argv 3]
set upperB  [lindex $argv 4]

# =============================================================== #

package require tempoUserVMD

# get the window number
if {$win_num <= 10} {
    scan $win_num %d win
    set old 0[expr {$win_num - 1}]
    set win 0$win_num
   } else {
    scan $win_num %d win
    set old [expr {$win_num - 1}]   }

# read in PSF and load/wrap dcd
mol new $inpsf
dopbc -file $indcd -frames 0:$skip:-1

# create selections
set permeant [atomselect top $permeant_text]
set refsel [atomselect top $reference_text]

# loop backwards n-1,...,2,1
set n [expr {[molinfo top get numframes]-1}]
for {set i $n} {$i > 0} {incr i -1} {

    # update frames and selections
    $permeant frame $i
    $refsel frame $i

    # subtract z coords: (center of mass of permeant) minus (center of mass of lipids)
    set dist [expr {[lindex [measure center $permeant] 2] - [lindex [measure center $refsel] 2]}]

    # if permeant is in range, write pdb if it doesn't already exist
    set output abf.win${win}.pdb
    if { $lowerB <= $dist && $dist <= $upperB && ![file exists $output]} {
        puts "=========== Permeant distance (Ang): $dist ==========="

        # write out pdb of frame i
        animate write pdb $output beg $i end $i skip 1 0

        # variables to print out in README file
        set bounds "\[$lowerB,$upperB\]"
        set pdb [lindex [split $indcd /] end]
        set frm [expr {$i * $skip}]
        set timestamp [clock format [clock seconds]]
        set dist [format "%5.3f" $dist]
        set newline "$win\t$bounds\t\t$pdb\t$frm (skip $skip)\t\t$dist\t\t$timestamp"

        # append README file with the newest selection
        set f [open $outDataFile a]
        puts $f $newline
        close $f

        exit
    }
}

puts "no coordinates found with the given conditions, or else pdb file already exists"
exit
