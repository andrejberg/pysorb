#!/bin/bash
#$ -N hollow.O1.Au5859.d.0.0.phi.0.psi.90        # the name of the job
#$ -q scc
#$ -pe mpi-12 48
#$ -m eba  # send a mail at end
#$ -l h_rt=72:00:00
#$ -l h_vmem=8G
#$ -l ib

module purge
module load quantumespresso
mpirun -n $NSLOTS  pw.x -nk 6 -i hollow.O1.Au5859.d.0.0.phi.0.psi.90.in
