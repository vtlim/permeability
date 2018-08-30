
# README file for ABF simulation of water permeation through POPC bilayer
Restructured on: Aug 14 2018 (from Jan 25 2017)
Last edited:     Aug 14 2018

Water permeability in POPC is 136e-4 cm/s.
Comer got 60-80e-4 cm/s.

## Procedure
Note: This is from memory based on work done starting summer 2016 with Eric Wong and bits and pieces since then.

1. 

2. 

3. 

### Things to change and check upon starting new continuation runs of a window
Checking these files will only take a few minutes compared to the hours/days these simulations will take to run.

1. `namd.pbs`
    1. job name
    2. input file name
    3. output file name
2. NAMD configuration file
    1. Rename file from base name (`run01.inp`)
    2. coordinates line
    3. outputname line
    4. lastrun block; and don't forget to include directory with filename
    5. firsttimestep
    6. colvarsConfig
    7. colvarsInput

### General parameters that a restart run has and differs from initial run in NAMD
1. Write new output name
2. Write input of previous run
3. Comment out temperature
4. Uncomment binCoordinates, binVelocities, extendedSystem
5. Comment cellBasisVector(3), cellOrigin
6. Set firsttimestep if desired
7. Comment minimize, reinitvels
8. Change "run" amount if needed


## Output of locateWTT.tcl script generating pdbs to start ABF windows.
Bounds are listed in Angstrom, based on WTT:OH2 zCoord - lipid:C21,C31 COM zCoord

Win	| Bounds	| PDB from traj		| Frame		| Distance WTT to center    | Date generated
----|-----------|-------------------|-----------|---------------------------|-----------------------------
01	| [32,44]	| npt_02.dcd	    | 4760		| 38.88967886567116		    | Mon Oct 10 10:33:24 PDT 2016
02	| [24,36]	| npt_02.dcd	    | 4740		| 34.06346872448921		    | Mon Oct 10 10:33:58 PDT 2016
03	| [16,28]	| npt_02.dcd	    | 4660		| 27.486047744750977		| Mon Oct 10 10:34:32 PDT 2016
04	| [8,20]	| npt_02.dcd	    | 1740		| 18.665841072797775		| Mon Oct 10 10:35:06 PDT 2016
05	| [0,12]	| abf.win04.01.dcd	| 14990		| 8.484895877540112		    | Fri Oct 14 17:15:37 PDT 2016
06	| [-8,4]	| abf.win05.01.dcd	| 14980		| 2.450698971748352		    | Wed Oct 19 11:40:39 PDT 2016


## What did come out fine

Basic (nonABF) setup
* Good movement of WTT ("tagged" water of which permeation will be assessed)  
   `/dfs3/pub/limvt/pmf/analysis/01_equil_wrap/wtt.z.npt02.png`
* Equilibrated box  
   `/dfs3/pub/limvt/pmf/analysis/01_equil_wrap/xst-2-5.png`
* Density profile of membrane  
   `/dfs3/pub/limvt/pmf/analysis/02_ndens/grace`

ABF-specific
* PMF looks fine   
   `/dfs3/pub/limvt/pmf/06_abf/win0merge/anti-1.png`


## What did NOT come out fine

* Diffusivity. Using Eric's method on half the data, the results aren't unintelligible, like with diffusivity   
  calculation in umbrella sampling route. Using the last half of the data has better results than using all data.  
  NOTE: I don't actually know how to use this method.
  ```
  cd /dfs2/tw/ericw3/analysis/chipot_limvt/calcPerm
  vi -d half3_freepmf.conf half2_fixpmf.conf run03.conf
  xg -block half3_fixpmf.dat -bxy 1:2 -block half2_fixpmf.dat -bxy 1:2 -block run03.dat -bxy 1:2
  xg -block half3_fixpmf.dat -bxy 1:3 -block half2_fixpmf.dat -bxy 1:3 -block run03.dat -bxy 1:3
  ```
* Calculated permeability by Eric's method came out about 16e-4 cm/s
  - 10x too small and not close enough (60-80 is better).

* Eric applied the DiffusionFusion code. I think the results are not sensible. Can't view his input files.
  ```
  cd /tw/ericw3/analysis/chipot_limvt/calcPermComer
  xg output/xg watermemb.best.force.pmf

  ```

## What to focus on next
* Write out, paper style, the parameters and stuff you used for YOUR ABF to see if things are okay. 
   - Example: how frequently data is collected, positional restraints, etc.
* Figure out if the fractional Smoluchowski model is appropriate here, and why it might be better than standard model.
   - Paper: Subdiffusion in Membrane Permeation of Small Molecules
* Figure out how to use DiffusionFusion, with the fractional Smoluchowski model.
   - This was applied from Eric on whole membrane. But that didn't work out.
   - First do window of bulk water.
   - Then do each window separately. Piece together like Figure S2 of the Subdiffusion paper.
* I think Eric set DiffusionFusion to return both the diffusivity and the PMF. 
  But since the PMF turned out fine from normal ABF, can I not just obtain diffusivity from DiffusionFusion?
  What the Comer et. al do in their papers?


## Notes to self
* *Naming scheme* is something like `abf.win06.08.inp` where the first digit refers to the window identity, and the  
  second number goes to the run (how long the window is extended).
* The *first version* of these windows started each window with minimization, which I think was decided against later.  
  Now each window is started by simply reinitializing velocities based on temp. Old simulations were deleted to save space.
* The *second version* of these windows did not have useConstantRatio turned on, leading the cells to become smushed over time.  
  Enabling that option prevented that problem. Old simulations were deleted to save space.
* The *third and current version* of the ABF attempt is labeled like `win02-constRatio` by directory.
* Editing *abfConfig* file to turn on options for `outputSystemForce` and `outputAppliedForce`. 
  Trying for window 01 first. 8/29/18


## Other relevant files and locations

* Eric Wong diffusivity calculations on my ABF runs  
  `/tw/ericw3/analysis/chipot_limvt`
* PSF file for all these systems
  `/pub/limvt/pmf/00_reference/chipot_box.psf`


