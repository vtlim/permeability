
# Scripts for analyzing position of permeant

## Contents

## Example instructions

1. Print out locations using Tcl script for VMD. Finds WTT z-coordinate, relative to center of mass of (C21, C31) of POPC.
   * `vmd -dispdev none -e printWTT.tcl -args input.psf input.dcd output.dat`

2. View with xmgrace.
   * `xmgrace output.dat &`


