
# Calculation of membrane permabilities using molecular dynamics simulations

This repository contains scripts for preparing and analyzing molecular dynamics simulations to calculate 
membrane permeabilities via three approaches: (1) umbrella sampling, (2) adaptive biasing force, and 
(3) a variant of adaptive biasing force called meta-eABF. Simulations are run using the NAMD software package.

References:
1. [Calculation of Lipid-Bilayer Permeabilities Using an Average Force](http://pubs.acs.org/doi/pdf/10.1021/ct400925s)
2. [Simulation-Based Approaches for Determining Membrane Permeability of Small Compounds](http://pubs.acs.org/doi/pdf/10.1021/acs.jcim.6b00022)
3. [NAMD user guide for version 2.13b1](https://www.ks.uiuc.edu/Research/namd/2.13b1/ug.pdf)

-------------------------------------------------------------------------------------------------------

## Directory tree

```
.
├── ABF
│   ├── 01_setup
│   ├── 02_filesCopy
│   └── 03_analyses
├── US
│   ├── 01_setup
│   ├── 02_analysis
│   │   ├── 01_area
│   │   ├── 02_overlap
│   │   ├── 03_wham
│   │   └── 04_mbar
│   └── diffusivity
└── waterbox
```

## TODO
1. update ABF inputs/scripts
2. update US inputs/scripts
3. add meta-eABF inputs/scripts


