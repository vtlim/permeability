# To label reference atoms to use in ABF simulations.
# Usage: 
#    vmd -dispdev none chipot_box.pdb
#    source labelref.tcl


set selALL [atomselect top all]
$selALL set beta 0.0
set sel [atomselect top "name C21 or name C31"]
$sel set beta 2.0
$selALL writepdb wtt.ref.pdb
