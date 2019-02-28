
# Calculation of membrane permabilities using molecular dynamics simulations

This repository contains scripts for preparing and analyzing molecular dynamics simulations to calculate 
membrane permeabilities via three approaches: (1) umbrella sampling, (2) adaptive biasing force, and 
(3) a variant of adaptive biasing force called meta-eABF. Simulations are run using the NAMD software package.  

This document last updated: Feb 28 2019

Selected references:
1. [Calculation of Lipid-Bilayer Permeabilities Using an Average Force](http://pubs.acs.org/doi/pdf/10.1021/ct400925s)
2. [Simulation-Based Approaches for Determining Membrane Permeability of Small Compounds](http://pubs.acs.org/doi/pdf/10.1021/acs.jcim.6b00022)
3. [NAMD user guide for version 2.13](https://www.ks.uiuc.edu/Research/namd/2.13/ug.pdf)
4. [Smoothed Biasing Forces Yield Unbiased Free Energies with the Extended-System Adaptive Biasing Force Method](https://pubs.acs.org/doi/abs/10.1021/acs.jpcb.6b10055)
5. [Zooming across the Free-Energy Landscape: Shaving Barriers, and Flooding Valleys](https://pubs.acs.org/doi/10.1021/acs.jpclett.8b01994)

-------------------------------------------------------------------------------------------------------

## Notes

* There is a Python module here called [`abf_pmf_processor.py`](analysis/permeability/abf_pmf_processor.py) which processes NAMD ABF PMFs. Functions include:
    * Averaging overlapping gradients from separate windows
    * Combining PMFs from separate leaflets
    * Setting average bulk water region of PMF to zero
    * Symmetrizing PMF (for symmetrization by anti-symmetrization of weighted gradients see [here](analysis/permeability/abf_pmf_processor.py))
    * Computing error by deviation from unsymmetrized PMF
    * Calculating pKa shift profile given two PMFs
* See examples located [here](analysis/permeability/examples/) (feel free to contact me for more)
* The scripts for ABF are more up-to-date than the umbrella sampling ones, though all should be fully functional.  


## Directory tree

```
.
├── ABF
│   ├── 01_prep
│   │   └── plain_abf_files
│   ├── job_scripts
│   └── winmerge
├── analysis
│   ├── 01_area-box-lipid
│   ├── 02_density-profile
│   │   └── example
│   ├── 03_permeant-position
│   └── permeability
│       ├── archive
│       └── examples
│           ├── abf_pmf_processor
│           ├── calc_perme
│           └── matchX
├── US
│   ├── 01_setup
│   ├── 02_analysis
│   │   ├── 01_area
│   │   ├── 02_overlap
│   │   ├── 03_wham
│   │   └── 04_mbar
│   └── diffusivity
│       ├── 1_fromSI
│       └── 2_fblockavg
└── waterbox

27 directories
```
