#!/usr/bin/env bash

cd /pub/limvt/pmf/07_us/02_analysis/trajfiles

TFILES=$(find -name 'w*' | sort -n)
TFILES=($TFILES)
echo "TOTAL NUMBER OF WINDOWS FOUND: ${#TFILES[@]}"

#LAMBDADIR=${ALLJOBSARRAY[LAMBDA-1]}

