#!/bin/bash
#$ -N top.O1.Au62.d.3.0.phi.0.psi.90        # the name of the job
#$ -q scc
#$ -pe mpi 32
#$ -m eba  # send a mail at end
#$ -l h_rt=168:00:00
#$ -l h_vmem=2G
#$ -l ib

module purge
module load quantumespresso
mpirun -n $NSLOTS pw.x -inp top.O1.Au62.d.3.0.phi.0.psi.90.in
