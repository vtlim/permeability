
# Analysis scripts for MD simulations
See description and usage in the subdirectories' README files or in the Python script headers.

Another handy script is `drawBox.tcl`, located on another repository [here](https://github.com/vtlim/Hv1/blob/master/04_fep/02_analysis/fixChg/scripts/drawBox.tcl).

## Short xmgrace primer

- Plot just first column: `xmgrace xst_win05_2-8.dat`
- Plot all columns: `xmgrace -nxy xst_win05_2-8.dat`
- Plot column 3 as a function of column 1: `xmgrace -block xst_win05_2-8.dat -bxy 1:3`

