#!/bin/bash
#$ -N top.O1.Au62.d.2.6.phi.45.psi.180        # the name of the job
#$ -q scc
#$ -pe mpi 32
#$ -m eba  # send a mail at end
#$ -l h_rt=168:00:00
#$ -l h_vmem=2G
#$ -l ib
export NUMTHREADS=32
export OMP_NUM_THREADS=1

module load quantumespresso
mpirun -n $NUMTHREADS pw.x -inp top.O1.Au62.d.2.6.phi.45.psi.180.in