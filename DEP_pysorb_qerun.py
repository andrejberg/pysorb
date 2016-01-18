#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 16.04.15
# 
# program to run QE calculations
# in this version calculations are only started if
# they are not alredy done in the output dir.
# 
# DEPRECATED 
# I use submit scripts by now
#### ------------------------------------------ ####

import os, sys, os.path
import subprocess as sub


help = '''
---------------------  pysorb run QE  ----------------
Run a QE calculation for each QE inputfile in a given
directory

Options:
    -h    display help message
    -i    directory of QE inputfiles
    -o    directory of QE outputfiles
    -c    comand to run
------------------------------------------------------
'''

if len(sys.argv)>1:
 for i in sys.argv:
  if i.startswith('-'):
   option=i.split('-')[1]
   if option=="i":
     input_dir = sys.argv[sys.argv.index('-i')+1]
   if option=="o":
     output_dir = sys.argv[sys.argv.index('-o')+1]
   if option=="c":
     pwcomand = sys.argv[sys.argv.index('-c')+1]
   if option=="h":
    print(help)
    sys.exit()
else:
 print(help)
 sys.exit()

try:
  input_dir
except NameError:
  print "Input directory not defined. (-i)"
  sys.exit()

try:
  output_dir
except NameError:
  print "Output directory not defined. (-o)"
  sys.exit()


# check directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# get the files and sort out the calculations already done
in_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir,f))]
out_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir,f))]

files = [f for f in in_files if f.split(".")[:-1] not in [g.split('.')[:-1] for g in out_files]]


# Start the calcs
for f in files:
   input_file = f
   output_file = ".".join(f.split(".")[:-1]) + ".out"
   sub.call(['/bin/bash',
                '-i',
                '-c',
                pwcomand + " <" + input_dir + "/" + input_file + " | tee " + output_dir + "/" + output_file])




#   print pwcomand + " <" + input_dir + "/" + input_file + " | tee " + output_dir + "/" + output_file


# run pw.x on input files
#if calc:
#   qe_outputdir = "qe_outputfiles"

#   e_sys = []

#   if not os.path.exists(qe_outputdir):
#       os.makedirs(qe_outputdir)
"""
   for i in np.arange(len(confs)):
      print "Starting QE calculation " + str(i+1) + " of " + str(len(confs)) + "\n"

      filename = "conf"+str(i)
      if os.path.isfile(qe_outputdir + "/" + filename + ".out"):
         os.rename(qe_outputdir + "/" + filename + ".out",
                   qe_outputdir + "/#" + filename + ".out#")

      print "Call: " + pwcomand + " <" + qe_inputdir + "/" + filename + ".in | tee " + qe_outputdir + "/" + filename + ".out"
      sub.call(['/bin/bash',
                '-i',
                '-c',
                pwcomand + " <" + qe_inputdir + "/" + filename + ".in | tee " + qe_outputdir + "/" + filename + ".out"])
      e_sys.append(ads.getefromfile(qe_outputdir + "/" + filename + ".out"))

   e_ads = []
   for e in e_sys:
      e_ads.append((e_molecule+e_slab)-e)

   ef = file(qe_outputdir + "/" + "e.dat", "wb")
   i  = 0
   for e in e_ads:
      ef.write("conf" + str(i) + "\t" + e + "\n")
      i += 1
   ef.close()

   print '''
------------------------------------------------------
Result is:
E_sys: ''' + str(e_sys) + '''
E_ads: ''' + str(e_ads) + '''
------------------------------------------------------
   '''
"""
