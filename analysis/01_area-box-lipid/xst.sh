#!/usr/bin/env bash

cd /pub/limvt/pmf/06_abf/win04-constRatio

DIRS=(01_run1 02_run2 03_run3 04_run4 05_run5 06_run6)
FILES=(abf.win04.01.xst abf.win04.02.xst abf.win04.03.xst abf.win04.04.xst) 
OUTF1=xst1_win04_1-3.dat
OUTF2=xst2_win04_1-3.dat

mkdir analysis

echo '# step | x | y | z' > analysis/$OUTF1
awk 'BEGIN{i=1} $1 !~ /^#|^0/{print $1,$2,$6,$10;i++}' ${DIRS[0]}/${FILES[0]} ${DIRS[1]}/${FILES[1]} ${DIRS[2]}/${FILES[2]} >> analysis/$OUTF1

echo '# step | area | height' > analysis/$OUTF2
awk 'BEGIN{i=1} $1 !~ /^#|^0/{print $1,$2*$6,$10;i++}' ${DIRS[0]}/${FILES[0]} ${DIRS[1]}/${FILES[1]} ${DIRS[2]}/${FILES[2]} >> analysis/$OUTF2
