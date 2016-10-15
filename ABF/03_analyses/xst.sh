#!/usr/bin/env bash

cd ../
echo '# step | area | height' > analysis/xst2_win05_2-8.dat
awk 'BEGIN{i=1} $1 !~ /^#|^0/{print $1,$2*$6,$10;i++}' 02_run2/abf.win05.02.xst 03_run3/abf.win05.03.xst 04_run4/abf.win05.04.xst 05_run5/abf.win05.05.xst 06_run6/abf.win05.06.xst 07_run7/abf.win05.07.xst 08_run8/abf.win05.08.xst >> analysis/xst2_win05_2-8.dat

echo '# step | x | y | z' > analysis/xst1_win05_2-8.dat
awk 'BEGIN{i=1} $1 !~ /^#|^0/{print $1,$2,$6,$10;i++}' 02_run2/abf.win05.02.xst 03_run3/abf.win05.03.xst 04_run4/abf.win05.04.xst 05_run5/abf.win05.05.xst 06_run6/abf.win05.06.xst 07_run7/abf.win05.07.xst 08_run8/abf.win05.08.xst >> analysis/xst1_win05_2-8.dat
