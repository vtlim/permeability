
# ABF simulations to calculate membrane permeability

Last edited:     Sep 28 2018   
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

4. Evaluate convergence, using .grad files.

5. Stitch together PMF from the different windows.

6. Calculate diffusivity using .traj files with DiffusionFusion.


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

* Check convergence: `tclsh abfConvergence.tcl ../../08_run8/abf.win01.08.grad 30 1 ../../01_run1/abf.win01.01.grad ../../02_run2/abf.win01.02.grad ../../03_run3/abf.win01.03.grad output`
  * where 30 should be replaced with time between hist frames, with units of ??? [TODO]
  * where 1 can be changed for desired stride

* Calculate statistical uncertainty of PMF: `tclsh abfCheckRunsError.tcl 32 32 ../../01_run1/abf.win01.01.grad ../../02_run2/abf.win01.02.grad ../../03_run3/abf.win01.03.grad  output`


