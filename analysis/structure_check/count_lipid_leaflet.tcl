
# Purpose: Check lipid residue count in upper and lower leaflets.
# Usage: vmdt -e count_lipid_leaflet.tcl -args inpsf coor1 coor2 coor3 [...]
# Note: change the pbc set line to your actual system dimensions

# load psf and pdb
mol new [lindex $argv 0]
mol addfile [lindex $argv 1]

# load .coor or .pdb frames
for {set i 2} {$i < $argc} {incr i} {
    mol addfile [lindex $argv $i]
}

# wrap to periodic image
pbc set {100 100 90} -all
pbc wrap -molid 0 -compound fragment -center com -centersel "resname POPC" -all

# set vmd selections
set A [atomselect top all]
set sel1 [atomselect top "name C21 C31 and z>0"]
set sel2 [atomselect top "name C21 C31 and z<0"]

# loop over each frame and count lipids
set n [expr {[molinfo top get numframes]}]
for {set i 0} {$i < $n} {incr i} {

    # move system to origin
    # https://www.ks.uiuc.edu/Research/vmd/mailing_list/vmd-l/26636.html
    $A frame $i
    set minus_com [vecsub {0.0 0.0 0.0} [measure center $A]]
    $A moveby $minus_com

    # count and print
    $sel1 frame $i
    $sel2 frame $i
    $sel1 update
    $sel2 update
    puts "Frame $i: [$sel1 num] [$sel2 num]"
}

exit
