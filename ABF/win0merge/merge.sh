ml purge
ml intel/2018.3 openmpi/3.1.2 namd/2.13b1
export SLURM_MPI_TYPE=pmi2
namd2 merge_.inp > merge.out
