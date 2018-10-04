
# ABF simulations to calculate membrane permeability

Last edited:     Oct 1 2018   
Test system:     TIP3P water molecule through a POPC bilayer   

Water permeability in POPC is 136e-4 cm/s.  
Comer got 60-80e-4 cm/s.  
See references in Comer paper in the main README file of this repository.  

## Procedure

1. Equilibrate system.

2. Prepare starting coordinates (pdb files) for windows.
   - From steered MD?
   - From neighboring windows?

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
    2. Specify the restart file names (coor, vel, xsc).
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


## Output of locateWTT.tcl script generating pdbs to start ABF windows.

Bounds are listed in Angstrom, referring to the expression:   
(z-coordinate of tagged water oxygen) minus (z-coordinate of center of mass of all lipid carbonyl atoms (C21, C31))

Win	| Bounds	| PDB from traj		| Frame		| Distance WTT to center    | Date generated
----|-----------|-------------------|-----------|---------------------------|-----------------------------
01	| [32,44]	| npt_02.dcd	    | 4760		| 38.88967886567116		    | Mon Oct 10 10:33:24 PDT 2016
02	| [24,36]	| npt_02.dcd	    | 4740		| 34.06346872448921		    | Mon Oct 10 10:33:58 PDT 2016
03	| [16,28]	| npt_02.dcd	    | 4660		| 27.486047744750977		| Mon Oct 10 10:34:32 PDT 2016
04	| [8,20]	| npt_02.dcd	    | 1740		| 18.665841072797775		| Mon Oct 10 10:35:06 PDT 2016
05	| [0,12]	| abf.win04.01.dcd	| 14990		| 8.484895877540112		    | Fri Oct 14 17:15:37 PDT 2016
06	| [-8,4]	| abf.win05.01.dcd	| 14980		| 2.450698971748352		    | Wed Oct 19 11:40:39 PDT 2016


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


