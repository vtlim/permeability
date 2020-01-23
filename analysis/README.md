# Script for analyzing MD simulations for calculating membrane permeability

## `permeability_profiles`

* Calculate the PMF from stratified adaptive biasing force simulations in NAMD.
* Symmetrize 1D profiles.
* Plot 1D profiles together.
* Match x-axis data between two different profiles.
* Compute permeability from the PMF and diffusivity profiles.

## `structure_check`

* Evaluate box area over time and/or evaluate area per lipid over time.
* Calculate the number density profile for a lipid bilayer to  analyze relative positions of water and lipid sections (headgroup, carbonyl, tail).

## `trajectory_processing`

## Other useful scripts not in this repo

* [`drawBox.tcl`](https://github.com/vtlim/misc/blob/master/vmd/drawBox.tcl)

-----

## Short xmgrace primer

- Plot just first column: `xmgrace xst_win05_2-8.dat`
- Plot all columns: `xmgrace -nxy xst_win05_2-8.dat`
- Plot column 3 as a function of column 1: `xmgrace -block xst_win05_2-8.dat -bxy 1:3`

