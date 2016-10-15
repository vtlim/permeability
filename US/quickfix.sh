# Edit job name, input, output for qsub file.
# Usage: from anywhere, run this bash script

cd /pub/limvt/pmf/07_us/windows/

for d in */
do
    echo $d
    cd $d

    # change queues to use free
    #sed -i "/#$ -q/c #$ -q free64,tw,pub64" namd.pbs
    #sed -i "/#$ -N/c #$ -N win${d%/}-RSa" namd.pbs
    #sed -i "/namd2/c namd2 +p\$CORES us.win${d%/}-RSa.inp > us.win${d%/}-RSa.out" namd.pbs

    # remove hold jobid line
    #sed -i "/hold_jid/d" namd.pbs

    # change Colvarsrestartfrequency
    #sed -i "/Colvarsrestartfrequency/c Colvarsrestartfrequency 10000" usConfig.win${d%/}.inp

    # change the pdb in config file
    #sed -i "/coordinates/c coordinates        01_min/us.win\${num}.pdb" us.win${d%/}.inp
    
    #cp *-RS.inp us.win${d%/}-RSa.inp
    sed -i "/outputName/c outputName         us.win\${num}-RSa" us.win${d%/}-RSa.inp
    sed -i "/firsttimestep/c firsttimestep      13000000" us.win${d%/}-RSa.inp


    cd ../

    # change the output name in min file
    #cd ${d}01_min/
    #sed -i "/outputName/c outputName         us.win\${num}.min" us.win${d%/}.min.inp
    #cd ../../

    # move files out of min directory
    #mv ${d}01_min/* ${d}
    #rm ${d}*min.inp

    

done
