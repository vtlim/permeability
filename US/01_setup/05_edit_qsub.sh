# Edit job name, input, output for qsub file.
# Usage: from anywhere, run this bash script

qsub=/pub/limvt/pmf/07_us/namd.pbs
cd /pub/limvt/pmf/07_us/windows/

#for d in 00/ 01/ 02/ 03/ 04/ 05/ 06/ 07/
for d in */
do
    echo $d

    # name each job by directory, no slashes, start with letter
    #sed -i "/#$ -N/c #$ -N us.win${d%/}.min" $qsub
    #sed -i "/#$ -q/c #$ -q tw,pub64,free64" $qsub
    #sed -i "/namd2/c namd2 +p\$CORES us.win${d%/}.min.inp > us.win${d%/}.min.out" $qsub
    #cp $qsub $d/01_min/

    sed -i "/#$ -N/c #$ -N us.win${d%/}" $qsub
    #sed -i "/#$ -q/c #$ -q tw,pub64" $qsub
    sed -i "/namd2/c namd2 +p\$CORES us.win${d%/}.inp > us.win${d%/}.out" $qsub
    cp $qsub $d/

    # ======== submit qsub =======
    #qsub namd-multicore.sh

done
