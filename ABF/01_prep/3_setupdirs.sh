#!/bin/bash

# Script to generate new window directory and run subdirectories.
# Usage:    file.sh win# 
# Example:  file.sh 6 -8 4
# Version:  Dec 3 2018


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
mkdir $dir/03
mkdir $dir/04
mkdir $dir/05
mkdir $dir/06

# copy over NAMD configuration files
cp 01_prep/abfConfig.win00.inp  $dir/00_ref/abfConfig.${dir}.inp
cp 01_prep/abf.win00.01.inp     $dir/01/abf.${dir}.01.inp
cp 01_prep/abf.win00.02.inp     $dir/02/abf.${dir}.02.inp


# ======================= PART TWO ==================== #
#              Part 2: edit input/qsub files

### abf colvars input file
sed -i "s/lowerboundary 24.0/lowerboundary ${lower}.0/g" $dir/00_ref/abfConfig.${dir}.inp
sed -i "s/upperboundary 36.0/upperboundary ${upper}.0/g" $dir/00_ref/abfConfig.${dir}.inp


### namd file for run 01
sed -i "s/run01.pdb/abf.${dir}.pdb/g" $dir/01_run1/abf.${dir}.01.inp
sed -i "/outputName/c outputName         abf.${dir}.01" $dir/01_run1/abf.${dir}.01.inp
sed -i "s/abfConfig.-----.inp/abfConfig.${dir}.inp/g" $dir/01_run1/abf.${dir}.01.inp

# get dimensions of box from pdb file
line=($(head -n 1 $dir/00_ref/abf.${dir}.pdb))
xbox=${line[1]}
ybox=${line[2]}
zbox=${line[3]}
xline="cellBasisVector1 ${xbox} 0. 0."
yline="cellBasisVector2 0. ${ybox} 0."
zline="cellBasisVector3 0. 0. ${zbox}"

# use those values to edit configuration file
sed -i "/cellBasisVector1/c $xline" $dir/01_run1/abf.${dir}.01.inp
sed -i "/cellBasisVector2/c $yline" $dir/01_run1/abf.${dir}.01.inp
sed -i "/cellBasisVector3/c $zline" $dir/01_run1/abf.${dir}.01.inp


### namd file for run 02: input- coord, output, restart, config
sed -i "s/run02.pdb/abf.${dir}.pdb/g" $dir/02_run2/abf.${dir}.02.inp
sed -i "/outputName/c outputName         abf.${dir}.02" $dir/02_run2/abf.${dir}.02.inp
sed -i "/firsttimestep/c firsttimestep      15000000" $dir/02_run2/abf.${dir}.02.inp
sed -i "s/abfConfig.-----.inp/abfConfig.${dir}.inp/g" $dir/02_run2/abf.${dir}.02.inp

# copy this run02 file into subsequent run directories
cp $dir/02_run2/abf.${dir}.02.inp $dir/03_run3/abf.${dir}.03.inp
cp $dir/02_run2/abf.${dir}.02.inp $dir/04_run4/abf.${dir}.04.inp
cp $dir/02_run2/abf.${dir}.02.inp $dir/05_run5/abf.${dir}.05.inp
cp $dir/02_run2/abf.${dir}.02.inp $dir/06_run6/abf.${dir}.06.inp
sed -i "/outputName/c outputName         abf.${dir}.03" $dir/03_run3/abf.${dir}.03.inp
sed -i "/outputName/c outputName         abf.${dir}.04" $dir/04_run4/abf.${dir}.04.inp
sed -i "/outputName/c outputName         abf.${dir}.05" $dir/05_run5/abf.${dir}.05.inp
sed -i "/outputName/c outputName         abf.${dir}.06" $dir/06_run6/abf.${dir}.06.inp
sed -i "/firsttimestep/c firsttimestep      30000000" $dir/03_run3/abf.${dir}.03.inp
sed -i "/firsttimestep/c firsttimestep      45000000" $dir/04_run4/abf.${dir}.04.inp
sed -i "/firsttimestep/c firsttimestep      60000000" $dir/05_run5/abf.${dir}.05.inp
sed -i "/firsttimestep/c firsttimestep      75000000" $dir/06_run6/abf.${dir}.06.inp
