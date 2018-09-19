# README.md

## Checking equilibration from box size

1. Awk-process NAMD xst files to obtain cell area and height.
   * `awk 'BEGIN{i=1} $1 !~ /^#|^0/{print i,$2*$6,$10;i++}' file1.xst [file2.xst] > output.xst`

2. View with xmgrace.
   * `xmgrace -nxy output.xst &`


## Check location of the tagged water molecule
1. Print out locations using Tcl script for VMD.
   * `vmd -dispdev none -e printWTT.tcl -args input.psf input.dcd output.dat`

2. View with xmgrace.
   * `xmgrace output.dat &`


