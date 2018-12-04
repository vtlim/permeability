#!/bin/bash

# Purpose:  Script to generate new window directory and run subdirectories. 
#           Run this in the main ABF directory containing the windows.
# Usage:    file.sh win lower upper
# Example:  file.sh 6 -8 4
# Version:  Dec 4 2018
# By:       Victoria T. Lim


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
# ======================================================= #

# specify directory name for this window
if [ $win -lt 10 ]; then
   dir=win0$win
else
   dir=win$win
fi

# create directory and subdirectories
mkdir $dir
mkdir $dir/00_ref
mkdir $dir/01
mkdir $dir/02

# copy over NAMD configuration files
cp 01_prep/abf.${dir}.pdb       $dir/00_ref/
cp 01_prep/abfConfig.win00.inp  $dir/00_ref/abfConfig.${dir}.inp
cp 01_prep/abf.win00.01.inp     $dir/01/abf.${dir}.01.inp
cp 01_prep/abf.win00.02.inp     $dir/02/abf.${dir}.02.inp


# ======================= PART TWO ====================== #
#              Part 2: edit input/qsub files
# ======================================================= #

### abf colvars input file
sed -i "s/lowerBoundary XX/lowerBoundary ${lower}.0/g" $dir/00_ref/abfConfig.${dir}.inp
sed -i "s/upperBoundary XX/upperBoundary ${upper}.0/g" $dir/00_ref/abfConfig.${dir}.inp


### namd file for run 01
sed -i "s/XX.pdb/abf.${dir}.pdb/g"                      $dir/01/abf.${dir}.01.inp
sed -i "/outputName/c outputName         ${dir}.01" $dir/01/abf.${dir}.01.inp
sed -i "s/abfConfig.-----.inp/abfConfig.${dir}.inp/g"   $dir/01/abf.${dir}.01.inp

# get dimensions of box from pdb file -- ASSUMES origin is at (0,0,0)
line=($(head -n 1 $dir/00_ref/abf.${dir}.pdb))
xbox=${line[1]}
ybox=${line[2]}
zbox=${line[3]}
xline="cellBasisVector1 ${xbox} 0. 0."
yline="cellBasisVector2 0. ${ybox} 0."
zline="cellBasisVector3 0. 0. ${zbox}"

# use those values to edit configuration file
sed -i "/cellBasisVector1/c $xline" $dir/01/abf.${dir}.01.inp
sed -i "/cellBasisVector2/c $yline" $dir/01/abf.${dir}.01.inp
sed -i "/cellBasisVector3/c $zline" $dir/01/abf.${dir}.01.inp


### namd file for run 02: input- pdb, output, restart, timestep, config
sed -i "s/XX.pdb/abf.${dir}.pdb/g"                      $dir/02/abf.${dir}.02.inp
sed -i "/outputName/c outputName         ${dir}.02"     $dir/02/abf.${dir}.02.inp
sed -i "s/restartXX/${dir}.01/g"                        $dir/02/abf.${dir}.02.inp
sed -i "/firsttimestep/c firsttimestep      10000000"   $dir/02/abf.${dir}.02.inp
sed -i "s/abfConfig.-----.inp/abfConfig.${dir}.inp/g"   $dir/02/abf.${dir}.02.inp

