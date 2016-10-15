# Purpose: to find starting pdbs for continuing ABF simulations.
# Date: 9 October 2016 
# Usage: vmdt -e file.tcl



# ============= Things to change before using ============= #

# these variables are changed by bash script. or chg manually.
# win is window number, lowerB & upperB are z dist in Angstrom
set wwin 5
set lowerB 0
set upperB 12
#set trajfile /pub/limvt/pmf/05_prod2/npt_02.dcd
set trajfile /pub/limvt/pmf/06_abf/win04-constRatio/01_run1/abf.win04.01.dcd


#  --------------- Default variables ----------------------- #

set skip 10  ;# for 2 fs/step & 1000 frames/step, each frame = 2 ps.
set dir "/pub/limvt/pmf/06_abf"
set psffile /pub/limvt/pmf/00_reference/chipot_box.psf
set readme /pub/limvt/pmf/06_abf/README

# ========================================================== #

cd $dir

#lappend auto_path /home/victoria/Documents/tempotools/libs
package require tempoUserVMD


# get the window number
if {$wwin <= 10} {
    scan $wwin %d win
    set old 0[expr {$wwin - 1}]
    set win 0$wwin
   } else {
    scan $wwin %d win
    set old [expr {$wwin - 1}]   }


# read in PSF and load/wrap dcd
mol new $psffile
dopbc -file $trajfile -frames 0:$skip:-1

# create selections
set wtt [atomselect top "segname WTT and name OH2"]
set lip [atomselect top "lipid and name C21 C31"]

# loop backwards n-1,...,2,1
set n [expr {[molinfo top get numframes]-1}]
for {set i $n} {$i > 0} {incr i -1} {
    # update frames and selections
    $wtt frame $i
    $lip frame $i

    # subtract z coords: water - center of mass of lipids
    set dist [expr {[$wtt get z] - [lindex [measure center $lip] 2]}]

    # set output filename. write pdb if file doesn't already exist.
    set output ${dir}/win${win}-constRatio/00_ref/abf.win${win}.pdb
    if { $lowerB <= $dist && $dist <= $upperB && ![file exists $output]} {
        puts "=========== WTT distance (Ang): $dist ==========="
        
        # write out pdb of frame i
        animate write pdb $output beg $i end $i skip 1 0

        # variables to print out in README file 
        set bounds "\[$lowerB,$upperB\]"
        set pdb [lindex [split $trajfile /] end]
        set frm [expr {$i * $skip}]
        set timestamp [clock format [clock seconds]]
        set newline "$win\t$bounds\t\t$pdb\t$frm\t\t$dist\t\t$timestamp"

        # append README file with the newest selection
        set f [open $readme a]
        puts $f $newline
        close $f

        exit
    }
}

exit
