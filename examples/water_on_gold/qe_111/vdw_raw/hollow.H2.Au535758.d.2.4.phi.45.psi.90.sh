#!/bin/bash
#$ -N hollow.H2.Au535758.d.2.4.phi.45.psi.90        # the name of the job
#$ -q scc
#$ -pe mpi 32
#$ -m eba  # send a mail at end
#$ -l h_rt=168:00:00
#$ -l h_vmem=2G
#$ -l ib
export NUMTHREADS=32
export OMP_NUM_THREADS=1

module load quantumespresso
mpirun -n $NUMTHREADS pw.x -inp hollow.H2.Au535758.d.2.4.phi.45.psi.90.in