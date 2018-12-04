/* vim: set filetype=markdown : */

# (Plain) ABF calculations on membrane permeation

Last edited:    Dec 4 2018   
System:         TIP3P water permeation through POPC bilayer

Water permeability in POPC is 136e-4 cm/s.  
Comer got 60-80e-4 cm/s.  
See references in Comer paper in the main README file of this repository.  


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


