
#
# Usage: 
#    ./file.sh win# NEWrun# lasttimestep   |   Ex.   ./file.sh 01 03 75000000
#
# Purpose: Set up new directory/files to continue some window of a stratified simulation.
# Example directory layout: ./win01/01 ./win01/02 ./win02/01 ./win02/02, etc.
#
# By:       Victoria T. Lim
# Version:  Dec 6 2018
#
# Notes:
#   [1] Run this script in the directory containing the ABF windows.
#   [2] Reference input file is copied from run 02 so if this input file
#   was modified, be careful.
#   [3] This script does not handle special cases where
#   the result of the previous output is not in format "abf.win02.03"
#   such as continuing from restart files. In that case, fix the
#   lastrun name of the previous window.
#



# set variables from command line
win=$1
run=$2
firststep=$3


# get the last run number
if [ $run -lt 10 ]; then
   lastrun=0$((10#$run-1)) # use 10#$ to specify base 10 not octal
else
   lastrun=$((run-1))
fi
echo "Setting up files for window $1 from run $lastrun to $run ..."


# check that it's not the first round to continuation
if [ "$run" = "02" ]
 then echo "This script doesn't support continuation from window 01 to window 02. Do manually."
 exit 1
fi


# make sure subdirectory does not exist then create
cd win${win}
if [ -d "$run" ]; then
  echo "The directory $run already exists! Exiting."
  exit 1
fi
mkdir ${run}
cd $run

# copy input file
cp ../02/abf.win${win}.02.inp abf.win${win}.${run}.inp

# update run number in input file for output and restart input
sed -i "s/win${win}.02/win${win}.${run}/g" abf.win${win}.${run}.inp
sed -i 's|'../01/win${win}.01'|'../${lastrun}/win${win}.${lastrun}'|g' abf.win${win}.${run}.inp

# update lasttimestep
sed -i "/firsttimestep/c firsttimestep      $firststep" abf.win${win}.${run}.inp

echo "Done."

