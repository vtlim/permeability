
# ____________________________________________________________________________________
#
# wrapXY.tcl
#
# Purpose:  Wrap trajectory in XY plane around selection.
# Usage  :  vmdt -e permeation_traj.tcl -args inpsf skip dcd1 dcd2 ...
# Usage: while in VMD --
#    [1] wrap your trajectory to box beforehand (VTL unsure)
#    [2] in vmd:  source wrapXY.tcl
#    [3] in vmd:  wrap_in_xy "your vmd selection"
#
# Dependencies
#  1. move_atoms.tcl
#  2. pbchelper.tcl
#
# Assumptions
#  - Only works on rectangular boxes
#
# By:      Victoria T. Lim
# Version: Mar 12 2019
# ____________________________________________________________________________________


# import move_atoms.tcl and pbchelp.tcl
set sourcedir /dfs3/pub/limvt/gitmisc/vmd
set sourcedir ~/connect/hpc/goto-tw/gitmisc/vmd

source $sourcedir/move_atoms.tcl
source $sourcedir/pbchelp.tcl

# ____________________________________________________________________________________


# translate system
proc sys_to_zero {all} {
    set to_be_moved [measure center $all]
    set to_be_moved [vecinvert $to_be_moved]
    moveby $all $to_be_moved
}

proc wrap_in_xy {seltxt {molid 0}} {
    puts "wrapping around $seltxt..."

    set sel [atomselect top $seltxt]
    set all [atomselect top "all"]

    # loop over all frames to do wrapping
    set n [expr {[molinfo $molid get numframes]}]
    for {set i 0} {$i < $n} {incr i} {
        # print frame number periodically
        if {[expr $i % 100 == 0]} {puts $i}

        # update frame to get accurate selections/unit cell
        animate goto $i
        $sel frame $i
        $all frame $i

        # get unit cell info
        # inspired by https://github.com/frobnitzem/pbctools/blob/master/pbcwrap.tcl
        # using procs from /home/limvt/local/lib/vmd/plugins/noarch/tcl/pbctools2.8/pbcset.tcl
        # (can't source pbcset directly)
        set cell [molinfo $molid get { a b c alpha beta gamma }]
        pbc_check_cell $cell
        set cell [pbc_vmd2namd $cell]
        set A [lindex $cell 0]
        set B [lindex $cell 1]
        set C [lindex $cell 2]
        set Ax [lindex $A 0]
        set By [lindex $B 1]
        set Cz [lindex $C 2]

        # compute coordinates for origin
        set origin {0 0 0}
        set com [measure center $sel]
        set origin [vecadd $origin $com]
        # don't move the z origin (aka wrap in xy direction only)
        lset origin 2 0

        # wrap
        set wrapsel "all and (same residue as (%s))"
        set halfcell [vecscale 0.5 [list $Ax $By $Cz]]
        #puts "CENTER COORDS: $origin"
        #puts "half cell: $halfcell"
        set maxy [expr [lindex $origin 1] + [lindex $halfcell 1]]
        set miny [expr [lindex $origin 1] - [lindex $halfcell 1]]
        set maxx [expr [lindex $origin 0] + [lindex $halfcell 0]]
        set minx [expr [lindex $origin 0] - [lindex $halfcell 0]]

        moveby [atomselect $molid [format $wrapsel "y>=$maxy"] frame $i] [vecinvert $B]
        moveby [atomselect $molid [format $wrapsel "y<$miny"]  frame $i] $B
        moveby [atomselect $molid [format $wrapsel "x>=$maxx"] frame $i] [vecinvert $A]
        moveby [atomselect $molid [format $wrapsel "x<$minx"]  frame $i] $A

        sys_to_zero $all
    }

}
