#!/bin/bash

# Script to generate new directories and initial files for new windows.
#   Run this in the 06_abf directory that houses the windows.
#   Don't forget to edit the Tcl script before this, if using diff. trajectory.
# Usage:    file.sh win# lower# upper#
# Example:  file.sh 6 -8 4
# Version:  9 October 2016


# check that the lower bound is < upper bound
if [ "$3" -le "$2" ]; then
  echo "The upper bound argument '$3' should be greater than the lower bound argument '$2'."
  exit 1
fi

win=$1
lower=$2
upper=$3

# ======================= PART ONE ====================== #
#                 Part 1: setup directories

wdir=/pub/limvt/pmf/06_abf
cd $wdir

# specify directory name for this window
if [ $win -lt 10 ]; then
   dir=win0$win
else
   dir=win$win
fi

# make sure the directory does not exist
if [ -d "$dir" ]; then
  echo "The directory $dir already exists! Exiting."
  exit 1
fi

# create directory and subdirectories
mkdir $dir-constRatio
xdir=$wdir/$dir-constRatio
mkdir $xdir/00_ref
mkdir $xdir/01_run1
mkdir $xdir/02_run2
mkdir $xdir/03_run3
mkdir $xdir/04_run4
mkdir $xdir/05_run5
mkdir $xdir/06_run6

# copy over NAMD configuration files
cp 02_filesCopy/abfConfig.inp $xdir/00_ref/abfConfig.${dir}.inp
cp 02_filesCopy/run01.inp     $xdir/01_run1/abf.${dir}.01.inp
cp 02_filesCopy/run02.inp     $xdir/02_run2/abf.${dir}.02.inp

# copy over qsub files
cp 02_filesCopy/namd.pbs $xdir/01_run1/namd.pbs
cp 02_filesCopy/namd.pbs $xdir/02_run2/namd.pbs
cp 02_filesCopy/namd.pbs $xdir/03_run3/namd.pbs
cp 02_filesCopy/namd.pbs $xdir/04_run4/namd.pbs
cp 02_filesCopy/namd.pbs $xdir/05_run5/namd.pbs
cp 02_filesCopy/namd.pbs $xdir/06_run6/namd.pbs


# ======================= PART TWO ====================== #
#                 Part 2: get starting pdb

sed -i "/set wwin/c set wwin ${win}"         01_setup/3_locateWTT.tcl
sed -i "/set lowerB/c set lowerB ${lower}" 01_setup/3_locateWTT.tcl
sed -i "/set upperB/c set upperB ${upper}" 01_setup/3_locateWTT.tcl

module load vmd
vmd -dispdev none -e 01_setup/3_locateWTT.tcl

# ======================= PART THREE ==================== #
#              Part 3: edit input/qsub files

### abf colvars input file
sed -i "s/lowerboundary 24.0/lowerboundary ${lower}.0/g" $xdir/00_ref/abfConfig.${dir}.inp
sed -i "s/upperboundary 36.0/upperboundary ${upper}.0/g" $xdir/00_ref/abfConfig.${dir}.inp

### namd qsub file
sed -i "s/win05.08/${dir}.01/g" $xdir/01_run1/namd.pbs
sed -i "s/win05.08/${dir}.02/g" $xdir/02_run2/namd.pbs
sed -i "s/win05.08/${dir}.03/g" $xdir/03_run3/namd.pbs
sed -i "s/win05.08/${dir}.04/g" $xdir/04_run4/namd.pbs
sed -i "s/win05.08/${dir}.05/g" $xdir/05_run5/namd.pbs
sed -i "s/win05.08/${dir}.06/g" $xdir/06_run6/namd.pbs

### namd file for run 01
sed -i "s/run01.pdb/abf.${dir}.pdb/g" $xdir/01_run1/abf.${dir}.01.inp
sed -i "/outputName/c outputName         abf.${dir}.01" $xdir/01_run1/abf.${dir}.01.inp
sed -i "s/abfConfig.-----.inp/abfConfig.${dir}.inp/g" $xdir/01_run1/abf.${dir}.01.inp

# get dimensions of box from pdb file
line=($(head -n 1 $xdir/00_ref/abf.${dir}.pdb))
xbox=${line[1]}
ybox=${line[2]}
zbox=${line[3]}
xline="cellBasisVector1 ${xbox} 0. 0."
yline="cellBasisVector2 0. ${ybox} 0."
zline="cellBasisVector3 0. 0. ${zbox}"

# use those values to edit configuration file
sed -i "/cellBasisVector1/c $xline" $xdir/01_run1/abf.${dir}.01.inp
sed -i "/cellBasisVector2/c $yline" $xdir/01_run1/abf.${dir}.01.inp
sed -i "/cellBasisVector3/c $zline" $xdir/01_run1/abf.${dir}.01.inp


### namd file for run 02: input- coord, output, restart, config
sed -i "s/run02.pdb/abf.${dir}.pdb/g" $xdir/02_run2/abf.${dir}.02.inp
sed -i "/outputName/c outputName         abf.${dir}.02" $xdir/02_run2/abf.${dir}.02.inp
sed -i "/firsttimestep/c firsttimestep      15000000" $xdir/02_run2/abf.${dir}.02.inp
sed -i "s/abfConfig.-----.inp/abfConfig.${dir}.inp/g" $xdir/02_run2/abf.${dir}.02.inp

# copy this run02 file into subsequent run directories
cp $xdir/02_run2/abf.${dir}.02.inp $xdir/03_run3/abf.${dir}.03.inp
cp $xdir/02_run2/abf.${dir}.02.inp $xdir/04_run4/abf.${dir}.04.inp
cp $xdir/02_run2/abf.${dir}.02.inp $xdir/05_run5/abf.${dir}.05.inp
cp $xdir/02_run2/abf.${dir}.02.inp $xdir/06_run6/abf.${dir}.06.inp
sed -i "/outputName/c outputName         abf.${dir}.03" $xdir/03_run3/abf.${dir}.03.inp
sed -i "/outputName/c outputName         abf.${dir}.04" $xdir/04_run4/abf.${dir}.04.inp
sed -i "/outputName/c outputName         abf.${dir}.05" $xdir/05_run5/abf.${dir}.05.inp
sed -i "/outputName/c outputName         abf.${dir}.06" $xdir/06_run6/abf.${dir}.06.inp
sed -i "/firsttimestep/c firsttimestep      30000000" $xdir/03_run3/abf.${dir}.03.inp
sed -i "/firsttimestep/c firsttimestep      45000000" $xdir/04_run4/abf.${dir}.04.inp
sed -i "/firsttimestep/c firsttimestep      60000000" $xdir/05_run5/abf.${dir}.05.inp
sed -i "/firsttimestep/c firsttimestep      75000000" $xdir/06_run6/abf.${dir}.06.inp
