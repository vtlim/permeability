#!/bin/sh

# Purpose: Copy all the *.traj files from NAMD US simulations.
#   If there are multiple files per window, combine these into 1 file/window.
#   These files are needed for MBAR and WHAM.
# Usage: ./file.sh

cd /pub/limvt/pmf/07_us
MAX=52

### Copy files
#cp windows/1*/*traj 02_analysis/trajfiles/
cd /pub/limvt/pmf/07_us/02_analysis/trajfiles

### Remove comment 'step' line. May be unnecessary.
#sed -i '/step/d' trajfiles/*traj


n=0;
while [ "$n" -le "$MAX" ]; do

  ### Get value of window number
  if [ $n -lt 10 ]; then
    WNUM=0$n
  else
    WNUM=$n
  fi

  ### if restart files present, combine all into one traj file
  if [ $(ls -l us.win$WNUM* | wc -l) -eq 2 ]; then
    head -n -1 us.win${WNUM}.colvars.traj > win${WNUM}.traj
    cat us.win${WNUM}-RS.colvars.traj >> win${WNUM}.traj
    # if there's 1 file and 2 restarts (3 files), manually do like "cat us.win10* > win10.traj"
  else
    mv us.win${WNUM}.colvars.traj win${WNUM}.traj
  fi
  
  n=`expr "$n" + 1`;

done

