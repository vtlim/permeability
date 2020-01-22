# Script for analyzing MD simulations for calculating membrane permeability

## `structure_check`

* Evaluate box area over time and/or evaluate area per lipid over time.
    * Last updated: Dec 3 2018
    * Scripts: `area_box_lipid.py`
    * Example usage:
        * Plot just one file:  
            `python area_box_lipid.py -i npt01.xst -n 144`
        * Plot one file compared to another:  
            `python area_box_lipid.py -i /loc/of/sim1/npt01.xst -j /loc/of/sim2/npt01.xst -n 144`
        * Plot one file compared to another, with multiple simulations each:  
            `python area_box_lipid.py -i /loc/of/sim1/npt01.xst /loc/of/sim1/npt02.xst -j /loc/of/sim2/npt01.xst /loc/of/sim2/npt02.xst -n 144`

* Calculate the number density profile for a lipid bilayer to  analyze relative positions of water and lipid sections (headgroup, carbonyl, tail).
    * Last updated: Dec 3 2018
    * Scripts: `analysisInp.tcl` and `plot_wdensc.py`
    * Requirements: `tempotools` package by J. Alfredo Freites
    * Example usage: see section below

## Other useful scripts not in this repo

* [`drawBox.tcl`](https://github.com/vtlim/misc/blob/master/vmd/drawBox.tcl)

-----

## Short xmgrace primer

- Plot just first column: `xmgrace xst_win05_2-8.dat`
- Plot all columns: `xmgrace -nxy xst_win05_2-8.dat`
- Plot column 3 as a function of column 1: `xmgrace -block xst_win05_2-8.dat -bxy 1:3`

## Calculating the membrane density profile

1. Open the `analysisInp.tcl` file, and specify the following options inside:
    * `dataDir` - gets prepended to both psf and dcd's; should end with forward slash
    * `workDir`- optional, leave as "" if you want to work in the current directory
    * psf file
    * step size to read in trajectory
    * trajectory file names
    * calculation settings
    * output settings

2. `vmd -dispdev none -e /your_path_to_tempotools/tempotools/libs/analysisMain.tcl -args analysisInp.tcl`

3. Comment out the header line to view in Grace or other processing.
    * `for k in *dat; do echo $k; sed -i -e 's/nframes/#nframes/' $k; done`

### References
1. Interleaflet mixing and coupling in liquid-disordered phospholipid bilayers (Biochimica et Biophysica Acta, 2016)
2. Update of the CHARMM All-Atom Additive Force Field for Lipids: Validation on Six Lipid Types (J Phys Chem B, 2010)
3. Acyl-Chain Methyl Distributions of Liquid-Ordered and -Disordered Membranes (Biophysical Journal, 2011)


### Notes
* Not sure if it's possible to include custom parameters such as for ligand. Triggered by error:  
  `key "NG2P1" not known in dictionary` so then only the first configuration get analyzed.
* tempotools is expected to be located in `~/` directory else will get error:  
  `couldn't load file "~/tempotools/libs/wdensC/updateWhist.so": ~/tempotools/libs/wdensC/updateWhist.so: cannot open shared object file: No such file or directory`
  This is from the `[root]/tempotools/libs/wdensC/wdensC.tcl` file.
* Run on hpc else will get error:  
  `couldn't open "/data/users/jfreites/tempotools/libs/tempoUtils/charmm_atom_types": no such file or directory`

