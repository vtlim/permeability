#!/bin/bash

# This script edits periodic cell of *inp files.
# Usage: while loop: "./file.sh list.txt"
#        for   loop: "./file.sh"

cd /pub/limvt/pmf/07_us/windows/

for d in */; do
  echo $d
  cd $d
  EDITF="us.win${d%/}.inp"
  cp /pub/limvt/pmf/07_us/us.winbase.inp $EDITF

  # get dimensions of box from pdb file
  line=($(head -n 1 us.win${d%/}.pdb))
  xbox=${line[1]}
  ybox=${line[2]}
  zbox=${line[3]}
  xline="cellBasisVector1 ${xbox} 0. 0."
  yline="cellBasisVector2 0. ${ybox} 0."
  zline="cellBasisVector3 0. 0. ${zbox}"
  
  #    use those values to edit configuration file
  sed -i "/cellBasisVector1/c $xline" $EDITF 
  sed -i "/cellBasisVector2/c $yline" $EDITF 
  sed -i "/cellBasisVector3/c $zline" $EDITF 

  # num for each window
  sed -i "1s/^/set num ${d%/}\n/" $EDITF

  cd ../

done
