#!/bin/sh
# Edit job name, input, output for qsub file.
# Usage: from anywhere, "file.sh list.txt"

cd /pub/limvt/pmf/07_us/windows/

while read -r d
do
    echo $d
    cd ${d}/01_min/
    qsub namd.pbs
    cd ../../

done < "$1"
