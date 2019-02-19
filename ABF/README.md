
# ABF simulations to calculate membrane permeability
Last edited:     Dec 5 2018   

## TODO

* clean code, add contents/documentation for `combine_leaflets.py`
* clean code, add contents/documentation for `combine_windows.py`
* update namd configuration files

## Contents

```
.
├── 01_prep
│   ├── 1_labelpdb.tcl              Script to label PDB file for colvars reference atoms.
│   ├── 2_locateWTT.tcl             Script to extract coordinates from trajectory for permeant in specified z-range.
│   ├── 3_setupdirs.sh              Script to set up new window directory and configuration files.
│   ├── abfConfig.win00.inp         colvars meta-eABF configuration file.
│   ├── abf.win00.01.inp            NAMD configuration file.
│   ├── abf.win00.01RS.inp          NAMD configuration file for runs that need to be restarted.
│   ├── abf.win00.02.inp            NAMD configuration file for continuation runs.
│   ├── executor.sh
│   └── plain_abf_files             Plain (not extended, not metadynamics) ABF configuration files.
│       ├── abfConfig.win00.inp
│       ├── abf.win00.01.inp
│       ├── abf.win00.01RS.inp
│       └── abf.win00.02.inp
├── 02_analysis
│   ├── abfCheckRunsError.tcl
│   └── abfConvergence.tcl
├── check_run_done.sh               Script to make sure ABF run completed successfully.
├── job_scripts
│   ├── namd_abf_neh.slurm          Greenplanet (Slurm) job script for NAMD, cpu, version 2.13b
│   ├── namd_gpu.sge                HPC (Sun Grid Engine) job script for NAMD, gpu, version 2.13
│   └── namd.pbs                    HPC (Sun Grid Engine) job script for NAMD, cpu, version 2.9 
├── new_abf_run.sh                  Script to set up new run for some ABF window.
├── README.md
├── water_toy_system.md             Details on toy system of TIP3P permeation through POPC bilayer.
└── winmerge                        Scripts used to facilitate merging of windows for full PMF profile.
    ├── mergeColvars.inp
    ├── merge_.inp
    ├── merge.sh
    ├── prep.sh
    └── README.md

```

## Procedure

1. Prepare and equilibrate system.

2. Generate labeled reference PDB for colvars.
    * Load system in PDB, then `source 1_labelpdb.tcl` 

3. Prepare starting coordinates (pdb files) for each window.
Here these coordinates come from neighboring windows but can come from other sources (pre-equilibration, steered MD, etc.).
Example commands:
    1. `vmdt -e 2_locateWTT.tcl -args npt02.dcd 1 36 40`
    2. `3_setupdirs.sh 1 32 44`

3. Run ABF calculations.
    1. The simulations obtain N number of samples per bin before applying the biasing force.  
       This isn't a separate calculation but is specified by the `fullSamples` parameter.
    2. Run and extend each window as necessary, periodically checking *convergence* of `.hist.grad` files
    3. Extend each window with `updateBias` off. (vtl did not run)  
       This wasn't done in the referenced paper bc wasn't introduced until later (subdiffusion paper?)

4. Stitch together PMF from the different windows.
    1. Generate symbolic links for every window's last .count and .grad files in your working directory.
    2. Prepare namd input file. No MD steps are run, but it's just to call namd.
    3. Prepare colvars input file. Specify the files from step (a) for the `inputPrefix` line.  
       Note that the namd user guide says the grid definition (min, max, width) can be changed.  
    4. Run the namd job: `namd merge.inp > merge.out`

5. Calculate diffusivity using .traj files with DiffusionFusion.


### Things to change and check upon starting new continuation runs of a window
Checking these files will only take a few minutes compared to the hours/days these simulations will take to run.

1. NAMD configuration file  
    *. Copy namd configuration file to new file.
    1. Define new `outputName`.
    2. Specify the input name from the previous run, for restart files (coor, vel, xsc).
    3. Set `firsttimestep` if desired.
    4. [if cont from run1] Comment temperature.
    5. [if cont from run1] Comment cellBasisVector(3), cellOrigin.
    6. [if cont from run1] Specify colvars restart file for `colvarsInput`.
    7. [if cont from run1] Comment `minimize` and `reinitvels`
    8. Change `run` amount if need be.

2. Job submission file
    1. job name
    2. input file name
    3. output file name

Note: A separate colvars configuration file does not need to be applied for treatment of fullSamples.   
The number of samples for `fullSamples` is saved and read from restart files, so when starting from   
a simulation with sufficient sampling, the bias is applied immediately. [see q&a from namd mailing list](https://tinyurl.com/ya2qlttm)


## Analysis specific to ABF calculations

Examples use the grad files of three runs but can take less/more than three.  
Directory organized like: `project/win01/analysis/check_convergence`  

* Check convergence by evaluating RMSD of the gradients with respect to the last frame
  * `tclsh abfConvergence.tcl reference_not_hist.grad delTime stride file1.hist.grad file2.hist.grad file3.hist.grad`
  * `delTime` is the actual time between frames in the `.hist` files. For example, with 2 fs time step and 1000 for `Colvarstrajfrequency` the `delTime` would be 0.002 (ns).
  * `stride` is for taking every Nth frame of the `.hist.grad` files

* Calculate statistical uncertainty of PMF:
  * `tclsh abfCheckRunsError.tcl 32 32 ../../01_run1/abf.win01.01.grad ../../02_run2/abf.win01.02.grad ../../03_run3/abf.win01.03.grad  output`

* Prep files for combining PMF of separate windows
  * `for k in {01..06}; do echo $k; ln -s /pub/limvt/pmf/06_abf/win$k-constRatio/06*/abf.win$k.06.count .; done`
  * `for k in {01..06}; do echo $k; ln -s /pub/limvt/pmf/06_abf/win$k-constRatio/06*/abf.win$k.06.grad  .; done`

* Run NAMD to combine PMF:
  * `module load NAMD-multicore/2.9; namd2 merge_.inp > merge.out`


