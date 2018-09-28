# README.md
Original cell dimensions in `PDB: 51.313   68.416  116.890`

## Checking equilibration from box size

1. Awk-process NAMD xst files to obtain cell area and height.
   * `awk 'BEGIN{i=1} $1 !~ /^#|^0/{print i,$2*$6,$10;i++}' file1.xst [file2.xst] > output.xst`
   * `./xst.sh` for automating and working with multiple input/output files

2. View with xmgrace.
   * `xmgrace -nxy output.xst &`

3. Generate a nicer plot with `plot_overTraj.py`.
   * Change variables inside script.
   * `python plot_overTraj.py`
    


## Check location of the tagged water molecule
1. Print out locations using Tcl script for VMD. Finds WTT z-coordinate, relative to center of mass of (C21, C31) of POPC.
   * `vmd -dispdev none -e printWTT.tcl -args input.psf input.dcd output.dat`

2. View with xmgrace.
   * `xmgrace output.dat &`


