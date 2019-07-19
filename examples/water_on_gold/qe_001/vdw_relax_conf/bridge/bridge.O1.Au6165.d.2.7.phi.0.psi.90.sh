#!/bin/bash
#$ -N bridge.O1.Au6165.d.2.7.phi.0.psi.90        # the name of the job
#$ -q scc
#$ -pe mpi 40
#$ -m eba  # send a mail at end
#$ -l h_rt=48:00:00
#$ -l h_vmem=2G
#$ -l ib

module purge
module load quantumespresso
mpirun -n $NSLOTS pw.x -inp bridge.O1.Au6165.d.2.7.phi.0.psi.90.in
