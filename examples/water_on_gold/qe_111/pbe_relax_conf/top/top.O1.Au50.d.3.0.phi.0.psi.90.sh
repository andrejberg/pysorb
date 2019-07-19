#!/bin/bash
#$ -N topEM        # the name of the job
#$ -q scc
#$ -pe mpi-12 48
#$ -m eba  # send a mail at end
#$ -l h_rt=72:00:00
#$ -l h_vmem=8G
#$ -l ib
#export NUMTHREADS=32
#export OMP_NUM_THREADS=1

module purge
module load quantumespresso
mpirun -n $NSLOTS  pw.x -nk 12 -i top.O1.Au50.d.3.0.phi.0.psi.90.in
