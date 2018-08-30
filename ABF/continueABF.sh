

# Usage: 
#    ./file.sh win# NEWrun# lasttimestep   |   Ex.   ./file.sh 01 03 75000000

# Purpose: to continue windows for ABF simulations.
#  - Creates subdir, copies and edits input files.

# Warning: this script does not handle special cases where
#   the result of the previous output is not in format "abf.win02.03"
#   such as continuing from restart files. In that case, fix the
#   lastrun name of the previous window.




cd /pub/limvt/pmf/06_abf/


# set variables from command line
win=$1
run=$2
firststep=$3

# get the last run number
if [ $win -lt 10 ]; then
   lastrun=0$((10#$run-1)) # use 10#$ to specify base 10 not octal
else
   lastrun=$((run-1))
fi
echo "Setting up files for window $1 from run $lastrun to $run ..."

# check that it's not the first round to continuation
if [ "$run" = "02" ]
 then echo "This script doesn't (yet) support continuation from window 01 to window 02. Do manually."
 exit 1
fi

# make sure subdirectory does not exist then create
cd win${win}-constRatio
if [ -d "$run" ]; then
  echo "The directory $run already exists! Exiting."
  exit 1
fi
mkdir ${run}
cd $run

# copy input and qsub files
cp ../02_run2/namd.pbs .
cp ../02_run2/abf.win${win}.02.inp abf.win${win}.${run}.inp

# update run number in input and qsub files
sed -i "s/win${win}.02/win${win}.${run}/g" namd.pbs
sed -i "s/win${win}.02/win${win}.${run}/g" abf.win${win}.${run}.inp
sed -i 's|'../01_run1/abf.win${win}.01'|'../${lastrun}/abf.win${win}.${lastrun}'|g' abf.win${win}.${run}.inp

# update lasttimestep
sed -i "/firsttimestep/c firsttimestep      $firststep" abf.win${win}.${run}.inp

echo "Done."
