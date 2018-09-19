
# ABF simulations to calculate membrane permeability

Last edited:     Sep 19 2018  
Test system:     TIP3P water molecule through a POPC bilayer  

Water permeability in POPC is 136e-4 cm/s. [TODO add reference]  
Comer got 60-80e-4 cm/s.

## Procedure [TODO]

1. 

2. 

3. 

### Things to change and check upon starting new continuation runs of a window
Checking these files will only take a few minutes compared to the hours/days these simulations will take to run.

1. Job submission file
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


