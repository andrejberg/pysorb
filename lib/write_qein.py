#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 23.06.15
# 
# definitions to write a QE inputfile
#### ------------------------------------------ ####

import numpy as np
import os, random

def write_conf_to_file(confs, slab, qe_input, qe_inputdir, prefix):

   for conf in confs:
      index_mol = str(np.where(conf.ads)[0][0] +1)
      label_mol = str(conf.labels[conf.ads][0])
      title = prefix + "." + label_mol + index_mol + "." + conf.slabatom + ".d." + conf.dist + ".phi." + conf.phi + ".psi." + conf.psi
      filename = title + ".in"

      # check if file exists and backup
      if os.path.isfile(qe_inputdir + "/" + filename):
         os.rename(qe_inputdir + "/" + filename, qe_inputdir + "/#" + filename + "#")

      # open files
      qe = file(qe_input, "r")
      f = file(qe_inputdir + "/" + filename, "wb")

      # transcript content from qe to f, change quantum espresso prefix, change title
      content = qe.readlines()
      qe.close()
      for line in content:
         if line.find('prefix') != -1:
            line = "    prefix                  = '" + str(random.randint(1000000, 9999999)) + "'\n"
         if line.find('title') != -1:
            line = "    title                   = '" + title + "'\n"
         f.write(line)

      # write atomic positions to qe      
      f.write("\n\nATOMIC_POSITIONS (angstrom) \n")
      write_positions(conf, f)
      write_slab_positions(slab, f)

      f.close()

def write_positions(obj, f):
   for i in range(len(obj.labels)):
     atom = obj.positions[i,:]
     f.write("%-2s %12.9f %12.9f %12.9f\n" % (obj.labels[i], atom[0], atom[1], atom[2]))
     
def write_slab_positions(obj, f):
   for i in obj.positions:
     f.write("%-2s %12.9f %12.9f %12.9f\n" % (i['label'], i['x'], i['y'], i['z']))

def write_submit_script(confs, qe_inputdir, prefix):
   submit_file_names = []
   for conf in confs:
      index_mol = str(np.where(conf.ads)[0][0] +1)
      label_mol = str(conf.labels[conf.ads][0])
      title = prefix + "." + label_mol + index_mol + "." + conf.slabatom + ".d." + conf.dist + ".phi." + conf.phi + ".psi." + conf.psi
      input_file = title + ".in"
      submit_file = title + ".sh"


      # check if file exists and backup
      if os.path.isfile(qe_inputdir + "/" + submit_file):
         os.rename(qe_inputdir + "/" + submit_file, qe_inputdir + "/#" + submit_file + "#")

      # open file
      submit = file(qe_inputdir + "/" + submit_file, "wb")
      content = '''#!/bin/bash
#$ -N ''' + title + '''        # the name of the job
#$ -q scc
#$ -pe mpi 32
#$ -m e  # send a mail
#$ -l h_rt=24:00:00
#$ -l h_vmem=2G
#$ -l ib
export NUMTHREADS=32
module purge
module load quantumespresso/5.1.2-intel
mpirun -n $NUMTHREADS pw.x -inp ''' + input_file

      submit.write(content)
      submit.close()

      submit_file_names.append(submit_file)
   
   # create submit file to submit submit files ;)
   sleeptime = '2h'
   sub_submit_file = os.path.join(qe_inputdir, 'submit.sh')
   sub_submit = file(sub_submit_file, 'wb')
   sub_submit.write('#!/bin/bash\n')
   sub_submit.write('sleeptime=' + sleeptime + '\n')
   for name in submit_file_names:
      sub_submit.write('qsub ' + name + '\n')
      sub_submit.write('sleep $sleeptime\n')
   sub_submit.close()



