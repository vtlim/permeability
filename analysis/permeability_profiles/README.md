## `permeability_profiles`

* Calculate the PMF from stratified adaptive biasing force simulations in NAMD.
    * Script: `abf_pmf_processor.py`
    * Example usage:  
        `python abf_pmf_processor.py -0 [win01.grad win02.grad win03.grad] -1 [win04.grad win05.grad win06.grad]`

* Compute permeability from the PMF and diffusivity profiles.
    * Script: `calc_perme.py`
    * Example usage:  
        `python calc_perme.py -p gbi2.pmf -d gbi2.dif -t 295`

* Match x-axis data between two different profiles.
    * Script: `matchX.py`
    * Example usage:  
        `python matchX.py -i water_1.csv -j water_2.csv -r water_1.csv > output.dat`

* Plot 1D profiles together.
    * Script: `plot_permeate.py`
    * Example usage:  
        `python plot_permeate.py -i GBI1.dat GBI2.dat GBIC.dat GBIN.dat GBCN.dat -d pmf`

* Symmetrize 1D profiles.
    * Script: `symmetrize.py`
    * Example usage:  
        `python symmetrize.py -i input.dat -o output.dat -c 1`
    * Note: This script is a standalone version of the same function is used in `abf_pmf_processor.py` with the exception that this script doesn't (yet) compute the error difference of the profiles before and after symmetrization.

### Contents

```
.
├── abf_pmf_processor.py
├── archive
│   ├── combine_leaflets.py
│   ├── combine_windows.py
│   ├── pmf_error.py
│   ├── pmf_shift.py
│   └── symmetrize_for_uneven.py
├── calc_perme.py
├── examples
│   ├── abf_pmf_processor
│   │   ├── output.dat
│   │   ├── output.png
│   │   ├── pmf0.dat
│   │   ├── pmf1.dat
│   │   ├── pmf.dat
│   │   ├── README
│   │   ├── win01.03.grad
│   │   ├── win02.04.grad
│   │   ├── win03.07.grad
│   │   ├── win04.07.grad
│   │   ├── win05.02.grad
│   │   ├── win06.03.grad
│   │   ├── win06-top.03.grad
│   │   ├── win07.03.grad
│   │   ├── win08.04.grad
│   │   ├── win09.04.grad
│   │   ├── win10.04.grad
│   │   └── win11.02.grad
│   ├── calc_perme
│   │   ├── output.dat
│   │   └── README.md
│   ├── example.md
│   └── matchX
│       ├── output.dat
│       ├── README.md
│       ├── water_1.csv
│       ├── water_1_samex_angstrom.csv
│       ├── water_1_short.csv
│       ├── water_2.csv
│       ├── water_2_samex_angstrom.csv
│       ├── water_2_short.csv
│       └── water.jpeg
├── matchX.py
├── plot_permeate.py
├── README.md
└── symmetrize.py

5 directories, 41 files
```
