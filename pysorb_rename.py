#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 29.06.2015
# 
# dieses program ist wohl nicht mehr
# noetig. vlt um die fertigen outs wieder umzubennen
#### ------------------------------------------ ####

import os, sys, os.path, random
import subprocess as sub
import numpy as np


help = '''
-------------------  pysorb rename QE  ---------------
Rename each file in a folder

Options:
    -h    display help message
    -i    directory of QE inputfiles
------------------------------------------------------
'''

if len(sys.argv)>1:
 for i in sys.argv:
  if i.startswith('-'):
   option=i.split('-')[1]
   if option=="i":
     input_dir = sys.argv[sys.argv.index('-i')+1]
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



# get the files and sort out the calculations already done
in_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir,f)) and f.split('.')[-1] == 'in']

r_files = [os.path.join(input_dir, 'run' + str(i) + '.in') for i, x in enumerate(in_files, 1)]

file_names = np.column_stack((in_files, r_files))

np.savetxt(os.path.join(input_dir, 'file_names.dat'), file_names, fmt="%s")

# Start the calcs
for f in file_names:
   input_file = open(f[0], 'r')
   new_file = open(f[1], 'wb')
   content = input_file.readlines()
   for line in content:
      if line.find('prefix') != -1:
          line = "    prefix                  = '" + str(random.randint(100000, 999999)) + "'\n"
      new_file.write(line)
   input_file.close()
   new_file.close()
#   os.rename(f[0], f[1])




