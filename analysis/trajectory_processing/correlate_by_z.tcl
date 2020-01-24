
# ============================================================== #
# correlate_by_z.tcl
#
# By:       Victoria T. Lim
# Purpose:  Correlate center of mass z-position of permeant with its
#           (1) orientation and (2) number of hydrogen bonds.
#
# Usage:
#  1. [load trajectory with analyzeDCD.tcl]
#  2. source correlate_by_z.tcl
#
# Last updated: Jan 22 2020
# ============================================================== #

#set homedir "../../.."
set homedir "/home/limvt/connect/hpc/goto-tw/08_permeate"
set homedir "/dfs2/tw/limvt/08_permeate"

set permeant "gbi2"     ;# this should correspond with one of the vmd macros

# ============================================================== #

# load macros for lipid-based selections
#source /dfs2/tw/limvt/08_permeate/vmd_macros.txt
source ${homedir}/vmd_macros.txt

# wrap box
source ${homedir}/github/analysis/trajectory_processing/wrapXY.tcl
wrap_only 0 "resname POPC"

# delete frame 0 of the pdb -- may be missing pbc parameters
animate delete  beg 0 end 0 skip 0 0

# wrap around permeant
wrap_in_xy $permeant

# get z position
get_com_z $permeant

# calculate permeant orientation
if {$permeant == "gbi1"} {
    calc_sel_orient "resname GBI1 and name C5"  "resname GBI1 and name N2"
} elseif {$permeant == "gbi2"} {
    calc_sel_orient "resname GBI2 and name C12" "resname GBI2 and name N6"
} elseif {$permeant == "gbic"} {
    calc_sel_orient "resname GBIC and name C5"  "resname GBIC and name N3"
} elseif {$permeant == "gbin"} {
    calc_sel_orient "resname GBIN and name C3"  "resname GBIN and name N3"
} elseif {$permeant == "gbcn"} {
    calc_sel_orient "resname GBCN and name C5"  "resname GBCN and name N3"
}

# calculate hbonds
count_hbonds $permeant "phosphate" "hbonds_phosphate"
count_hbonds $permeant "carbonyl"  "hbonds_carbonyl"

# wrap system around permeant to account for periodic box edges
wrap_only 0 $permeant
count_hbonds $permeant "water"     "hbonds_water"

