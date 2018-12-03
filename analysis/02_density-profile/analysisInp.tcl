#
# Victoria Lim, 16 June 2016
# input file for trajectory analysis using VMD
#
# J. Alfredo Freites
# The TEMPO group @ UCI
# jfreites@uci.edu
#

#Add here the path for the TEMPO analysis libraries
lappend auto_path /data/users/limvt/tempotools/libs

# Add your own Libraries here
#source
#load

# Analysis name
set myAnalysis wdensC

# System/Trajectory parameters
#------------------------------------------------------------------------
# dataDir: this is concatenated to the myPSF and file names in theFiles and myReference
# workDir: this is concatenated to the output files
# myPSF: your topology file
# trajFileType: file type for your trajectory file
# step: step length used when reading the trajectory files

set dataDir /dfs2/tw/limvt/08_permeate/bilayer/step7b_equil-gpu-stoch/taut1_charged/
set workDir ""
set myPSF ../../step6_ligAndIon/taut1_charged/popc_t1pos.psf
set trajFileType dcd
set step 10


# theFiles:
# Provide a TCL list of trajectory file names or use your TCL skills to build it

set theFiles [list npt01.dcd npt02.dcd]
# for {set i 2} {$i <= 6} {incr i} {
#	lappend theFiles npt0${i}.dcd }


# theFileRange:
# Provide a TCL list with the first and last frame number to be analyzed in each
# trajectory file.
# Leave theFileRange empty (set to "") if you want all the frames of all the files
# to be analyzed.

#set theFileRange [list first1 last1 first2 last2 ...]
#set theFileRange [list 500 1499 0 -1 0 -1 0 -1 0 -1]
set theFileRange ""


#------------------------------------------------------------------------


# Selections list
#------------------------------------------------------------------------
# mySelections:
# Provide a TCL list of VMD selection sentences or use your TCL skills to build it

#set mySelections [list "selectionSentence1"  "selectionSentence2" ...]
#set mySelections [list {selectionSentence1}  {selectionSentence2} ...]

set mySelections [list water protein phosphate carbonyl choline lipid glycerol "resname GBI1"]

#------------------------------------------------------------------------


# Output file names list
#------------------------------------------------------------------------
# Output file names are built by compounding three strings:
# outFilePrefix, outFile, and outFileSuffix
# outFile is any element of theOutFiles list

# theOutfiles:
# Provide a TCL list of unique ids ONE for each SELECTION
# or use your TCL skills to build it
# Leave theOutfiles empty (set to "") to use the selection sentences in mySelections
# as unique ids


set theOutFiles ""
set outFilePrefix ndens_taut1_
set outFileSuffix .dat

#------------------------------------------------------------------------


# Additional parameters
#------------------------------------------------------------------------
# Set only what you need for your particular analysis the rest will be ignored

# Evolution parameters
#
# set the correct scale for the time axis in any observable vs. time analysis
#
# used in: any script name somethingEvol
#
# tinit: initial time
# tstep: time step

#set tinit 0
#set tstep 0.2

# _____ Reference Parameters _____
# set configuration file name or selection sentences to be used as reference
#
# used in: myreference -- rmsdEvol axisEvol
#	   selref -- ndens hbondPathCyl comEvol contactsEvol
#
# myreference: file name for a single configuration
#	       dataDir is appended to the file name
# selref: a valid VMD selection sentence

#set myreference lacy-new-325p-pope.pdb
set selref carbonyl

# _____ Histogram Parameters _____
# used when constructing histograms
#
# used in: ndens gofr
#
# hmin, hmax, rmax: histogram min/max values
# dh,dr: bin width
# weightType: hist weight n x none
# labelSelections: valid vmd selection sentences to modify atomtypes
# labelFractions: as many <= 1.0 as label selections
set hmin -65.0
set hmax 65.0
set dh 0.2
set weightType none
# set dr 0.2
# set rmax 12.0

# _____ Cutoff Parameters ______
# set distance and angle cuttof for the VMD commands
# "measure hbonds" and "measure contacts"
#
# used in: hbondsEvol hbondPath hbondPathCyl
#
# distanceCutoff: a distance value in A
# angleCutoff: an angle value in deg

#set distanceCutoff 3.5
#set angleCutoff 40.0

# ______ Cylindrical Region Parameters ______
# defines a cylindrical ROI by specifying the position of the
# bases and the square of the radius
# in addition there is also a width for axial positions
#
# used in: hbondPathCyl
#
# bottomCyl: axial position of the bottom base
# topCyl:  axial position of the top base
# widthZ: axial position width
# the cylinder goes from z= bottomCyl-widthZ to z= topCyl+widthZ
# radiusCyl2: the square of the radius

#set bottomCyl -11
#set topCyl 18
#set widthZ 1.4
#set radiusCyl2 100

# Hbond network parameters
#
# set some properties of the Hbond network
#
# used in: directedGraph -- hbondPath hbondPathCyl
#	   pathEndsSel -- hbondPath
#
# directedGraph: "yes" if the network has D->A links only
# pathEndsSel: A valid VMD selection sentence containing atoms in two residues only.

#set directedGraph no
#set pathEndsSel "(protein and resid 269 and sidechain) or (protein and resid 144 and sidechain)"

# _____ Cartesian Parameters _____
# coordinates and vectors
#
# used in: axisEvol
#
# axisTM: a VMD 3D vector (a Tcl list of three numbers)

#set axisTM {0 0 1}
#------------------------------------------------------------------------
