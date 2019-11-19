# procs from /home/limvt/local/lib/vmd/plugins/noarch/tcl/pbctools2.8/pbcset.tcl
# VTL for use with wrapXY.tcl
############################################################
#
#   This file contains procedures to set and get the VMD unitcell
# parameters.
#
# $Id: pbcset.tcl,v 1.20 2014/09/09 20:00:17 johns Exp $
#


###################################################################
#
# pbc_vmd2namd a b c [ alpha beta gamma ]
#
#   Transforms VMD style unit cell parameters into NAMD unit cell
# vectors.
#
# From molfile_plugin.h:
# Unit cell specification of the form A, B, C, alpha, beta, gamma.
# A, B, and C are the lengths of the vectors.  alpha is angle
# between A and B, beta between A and C, and gamma between B and C.
#
# AUTHORS: Jan
#
proc pbc_vmd2namd { vmdcell } {
if { [ llength $vmdcell ] >= 3 } then {
    set a     [lindex $vmdcell 0]
    set b     [lindex $vmdcell 1]
    set c     [lindex $vmdcell 2]
} else {
    vmdcon -info "usage: pbc_vmd2namd a b c \[ alpha beta gamma \]"
    return
}

if { [ llength $vmdcell ] >= 6 } then {
    set alpha [lindex $vmdcell 3]
    set beta  [lindex $vmdcell 4]
    set gamma [lindex $vmdcell 5]
}

# The following is taken from VMD Timestep.C
# void Timestep::get_transforms(Matrix4 &a, Matrix4 &b, Matrix4 &c)

# A will lie along the positive x axis.
# B will lie in the x-y plane
# The origin will be (0,0,0).

# a, b, c are side lengths of the unit cell
# alpha = angle between b and c
# beta  = angle between a and c
# gamma = angle between a and b

set A {}; set B {}; set C {};

# Note: Between VMD 1.8.2 and 1.8.3 the definition of the unitcell
# parameters changed which is why we have to check the version
if {[string compare "1.8.3" [vmdinfo version]]>0} {
    #vmdcon -info "VMD version <= 1.8.2"
    set alphar [deg2rad $gamma];  # swapped!
    set betar  [deg2rad $beta];
    set gammar [deg2rad $alpha];  # swapped!

    set cosAB  [expr {cos($alphar)}];
    set sinAB  [expr {sin($alphar)}];
    set cosAC  [expr {cos($betar)}];
    set cosBC  [expr {cos($gammar)}];

    set Ax $a
    set Bx [expr {$b*$cosAB}]
    set By [expr {$b*$sinAB}]
    set Cx [expr {$c*$cosAC}]
    set Cy [expr {($b*$c*$cosBC-$Bx*$Cx)/$By}]
    set Cz [expr {sqrt($c*$c-$Cx*$Cx-$Cy*$Cy)}]

    set A  [list $Ax 0.0 0.0]
    set B  [list $Bx $By 0.0]
    set C  [list $Cx $Cy $Cz]

    set phi [vecangle {0 0 1} $C]
    set Cl [expr {$c/cos([deg2rad $phi])}]
    set C [vecscale $Cl [vecnorm $C]]
} else {
    #vmdcon -info "VMD version > 1.8.2 (including 1.8.3aXX)"
    set cosBC [expr {cos([deg2rad $alpha])}]
    set sinBC [expr {sin([deg2rad $alpha])}]
    set cosAC [expr {cos([deg2rad $beta])}]
    set cosAB [expr {cos([deg2rad $gamma])}]
    set sinAB [expr {sin([deg2rad $gamma])}]

    set Ax $a
    set Bx [expr {$b*$cosAB}]
    set By [expr {$b*$sinAB}]

    # If sinAB is zero, then we can't determine C uniquely since it's defined
    # in terms of the angle between A and B.
    if {$sinAB>0} {
	set Cx $cosAC
	set Cy [expr {($cosBC - $cosAC * $cosAB) / $sinAB}]
	set Cz [expr {sqrt(1.0 - $Cx*$Cx - $Cy*$Cy)}]
    } else {
	set Cx 0.0
	set Cy 0.0
	set Cz 0.0
    }

    set A [list $Ax 0.0 0.0]
    set B [list $Bx $By 0.0]
    set C [list $Cx $Cy $Cz]
    set C [vecscale $C $c]
}

return [list $A $B $C]
}

###################################################################
#
# pbc_namd2vmd $a $b $c
#
#   Transforms NAMD unit cell vectors $a, $b and $c into VMD unit cell
# parameters.
# In NAMD, the vector A is not necessarily parallel to the
# x-axis. Therefore, the procedure will also return the rotation
# matrix required to rotate the coordinates so that it is parallel.
#
# AUTHORS: Jan
#
proc pbc_namd2vmd { cell } {
# Defaults
set A [lindex $cell 0]
set B [lindex $cell 1]
set C [lindex $cell 2]
set rot {}

# In molinfo the length of the cell vectors and the angles between
# them are saved. $A is assumed to be parallel with the x-axis.
# If it isn't then we compute the rotation matrix
if {abs([vecdot [vecnorm $A] {1 0 0}]-1.0)>0.000001} {
    # Compute transformation matrix to rotate A into x-axis
    set rot [transvecinv $A]
    set A [coordtrans $rot $A]
    set B [coordtrans $rot $B]
    set C [coordtrans $rot $C]
}

# Note: Between VMD 1.8.2 and 1.8.3 the definition of the unitcell
# parameters changed which is why we have to check the version
if {[string compare "1.8.3" [vmdinfo version]]>0} {
    # vmdcon -info "VMD version <= 1.8.2"
    set gamma [vecangle $B $C]
    set beta  [vecangle $A $C]
    set alpha [vecangle $A $B]
} else {
    # vmdcon -info "VMD version > 1.8.2 (including 1.8.3aXX)"
    set alpha [vecangle $B $C]
    set beta  [vecangle $A $C]
    set gamma [vecangle $A $B]
}

set a [veclength $A]
set b [veclength $B]
set c [veclength $C]

return [list $a $b $c $alpha $beta $gamma $rot]
}


###################################################################
#
# pbc_check_cell
#
#   Test, whether the cell parameters $cell are reasonable,
# i.e. none of the sides has zero length, and none of the angles
# is out of range.
# Returns an error message if anything was out of range, otherwise
# nothing.
#
proc pbc_check_cell { cell } {
foreach { a b c alpha beta gamma } $cell {}
if { $a < 1.0e-10 || $b < 1.0e-10 || $c < 1.0e-10 } then {
    vmdcon -err "Suspicious pbc side length (a=$a b=$b c=$c). Have you forgotten to set the pbc parameters?"
}
if { [expr $alpha < 1.0e-10 || $alpha > 179.999 \
	  || $beta < 1.0e-10 || $beta > 179.999 \
	  || $gamma < 1.0e-10 || $gamma > 179.999 ] } then {
    vmdcon -err "Suspicious pbc angle (alpha=$alpha beta=$beta gamma=$gamma)."
}
return;
}

###################################################################
#
# Internal helper procedures
#
# Computes the angle between two vectors x and y
proc vecangle {x y} {
if {[llength $x] != [llength $y]} {
    error "vecangle needs arrays of the same size: $x : $y"
}
if {[llength $x]==0 || [llength $y]==0} {
    error "vecangle: zero length vector: [llength $x] : [llength $y]"
}
# Compute scalar-produt
set dot 0
foreach t1 $x t2 $y {
    set dot [expr $dot + $t1 * $t2]
}
set rr [rad2deg [expr (acos($dot/([veclength $x] * [veclength $y])))]]

return $rr
}

# Transforms degrees to radians and back
proc deg2rad { deg } {
return [expr ($deg/180.0*3.14159265)]
}

proc rad2deg { rad } {
return [expr ($rad/3.14159265)*180.0]
}


