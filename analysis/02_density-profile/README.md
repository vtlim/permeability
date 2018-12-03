
# Scripts for calculating membrane density profile 
Last updated: Dec 3 2018

The purpose of this analysis is to calculate the number density profile for a lipid bilayer. 
Use this to analyze relative positions of water molecules and lipid sections (headgroup, carbonyl carbons, chains).

This analysis requires tempotools package for VMD (by J. Alfredo Freites).

## Contents
* `analysisInp.tcl`

## Example instructions
1. Open the `analysisInp.tcl` file, and specify the following options inside:
    * `dataDir` - gets prepended to both psf and dcd's; should end with forward slash
    * `workDir`- optional, leave as "" if you want to work in the current directory
    * psf file
    * step size to read in trajectory
    * trajectory file names
    * calculation settings
    * output settings
2. `vmd -dispdev none -e /your_path_to_tempotools/tempotools/libs/analysisMain.tcl -args analysisInp.tcl`

## References
1. Interleaflet mixing and coupling in liquid-disordered phospholipid bilayers (Biochimica et Biophysica Acta, 2016)
2. Update of the CHARMM All-Atom Additive Force Field for Lipids: Validation on Six Lipid Types (J Phys Chem B, 2010)
3. Acyl-Chain Methyl Distributions of Liquid-Ordered and -Disordered Membranes (Biophysical Journal, 2011)

