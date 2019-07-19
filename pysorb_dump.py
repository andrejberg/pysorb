#! /usr/bin/python

#### ------------------------------------------ ####
# edit 11.08.15
#
# program to dump QE outputfiles
#
#### ------------------------------------------ ####

import os, sys, os.path

from classes.QEout import *
import lib.convert as convert
from lib.helper import water_mol_orientation

help = '''
--------------------  pysorb qe2gulp  ---------------

Options:
    -h      display help message
    -qe     directory of QE outputfiles
    -e_ref  default 0.0
            reference energy (Ry units) which is subtracted 
            from each energy calculated by EQ
    -o      default: pysorb.qedump 
------------------------------------------------------
'''

#INITIAL PARAMS
dump_file="pysorb.qedump"
ref_file="e.ref"
e_ref = 0.0

if len(sys.argv)>1:
 for i in sys.argv:
  if i.startswith('-'):
   option=i.split('-')[1]
   if option=="qe":
     output_dir = sys.argv[sys.argv.index('-qe')+1]
   if option=="e_ref":
     e_ref = float(sys.argv[sys.argv.index('-e_ref')+1])
   if option=="o":
     dump_file = sys.argv[sys.argv.index('-o')+1]
   if option=="h":
    print(help)
    sys.exit()
else:
 print(help)
 sys.exit()


try:
  output_dir
except NameError:
  print "WE output directory not defined. (-qe)"
  sys.exit()
  
# convert reference energy from Ry to eV
e_ref = convert.ry2ev(float(e_ref))

# get the file names
out_file_names = [f for f in sorted(os.listdir(output_dir)) if os.path.isfile(os.path.join(output_dir,f))]

# make list of QEout
out_files = [QEout(os.path.join(output_dir,f), f) for f in out_file_names]

# write dumpfile
dump = open(dump_file, "wb")

for calc in out_files:
    dump.write("START\n")
    # dump.write("PREFIX " + calc.prefix + "\n")
    # dump.write("MATM " + calc.matom + "\n")
    # dump.write("SATM " + calc.satom + "\n")
    # dump.write("DIST " + calc.dist + "\n")
    # dump.write("PHI_IN " + calc.phi + "\n")
    # dump.write("PSI_IN " + calc.psi + "\n")
    # dump.write("ADSORBED " + calc.getadsorbedatom()[0] + "\n")
    # dump.write("D_ADS " + str(calc.getadsorbedatom()[1]) + "\n")
    # # added 24.01.17
    # dump.write("D_OXY " + str(calc.getadsorbeddistance()[1]) + "\n")
    # phi,  psi = water_mol_orientation(calc.getatompositions()[:3],  [0, 0, 1])
    # dump.write("PHI_REAL " + str(phi) + "\n")
    # dump.write("PSI_REAL " + str(psi) + "\n")
    # added 24.01.17
    cell = calc.makecellparams()
    dump.write("CELL %9.6f %9.6f %9.6f %9.6f %9.6f %9.6f\n" % (cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]))
    labels = calc.getlabels()
    atoms  = calc.getatompositions()
    for a in range(len(labels)):
        atom = atoms[a,:]
        dump.write("ATOM %-2s %9.6f %9.6f %9.6f\n" % (labels[a], atom[0], atom[1], atom[2]))
    dump.write('EADS ' +str(convert.ry2ev(float(calc.getenergy()))-e_ref) + '\n')
    dump.write("END\n")
