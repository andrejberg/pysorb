#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 10.04.15
# 
# program to create QE input files for set of scf
# calculations
#### ------------------------------------------ ####

import sys, ConfigParser, os
import numpy as np

from classes.System import *
from classes.Slab import *
from classes.Molecule import *
from lib.configurations import obtainconfigurations, filterconfigurations
import lib.write_qein as wqi


help = '''
---------------------  pysorb2qe  -------------------- 
Calculate adsorbtion energies of a 
molecule on a surface in Quantum Espresso.

Options:
    -h    display help message
    -i    input file with parameters for calculation
    -scc  create submit scripts for cluster
------------------------------------------------------
'''
# INITIAL PARAMETER
scc = False

if len(sys.argv)>1:
 for i in sys.argv:
  if i.startswith('-'):
   option=i.split('-')[1]
   if option=="i":
     pysorb_input = sys.argv[sys.argv.index('-i')+1]
   if option=="scc":
     scc = True
   if option=="h":
    print(help)
    sys.exit()
else:
 print(help)
 sys.exit()

try:
  pysorb_input
except NameError:
  print "Input file not defined. (-i)"
  sys.exit()

# get path of inputfile
path = "/".join(pysorb_input.split("/")[:-1])

# read variables from pysorb input file
config = ConfigParser.ConfigParser()
config.read(pysorb_input)

# [files] section
source_molecule = os.path.join(path, config.get("files", "molecule"))
source_slab = os.path.join(path, config.get("files", "slab"))
qe_input = os.path.join(path, config.get("files", "qe"))

# [control] section
axis = int(config.get("control", "axis"))
alat = float(config.get("control", "alat"))

dist = config.get("control", "dist")
dist = [float(s) for s in dist.split(',')]

phi = config.get("control", "phi")
phi = [float(s) for s in phi.split(',')]

psi = config.get("control", "psi")
psi = [float(s) for s in psi.split(',')]

# [filter] section
if config.has_section('filter'):
   rules = config.items("filter")
   filterrules = []
   for rule in rules:
      r = rule[1].split()
      filterrules.append((r[0], r[1], float(r[2])))

if filterrules != []:
   dofilter = True
else:
   dofilter = False

# [output] section
qe_inputdir = config.get("output", "dir")
prefix      = config.get("output", "prefix")


print(help)

print '''
------------------------------------------------------
Input is:
Axis:      ''' + str(axis) + '''
ALAT:      ''' + str(alat) + '''
Distances: ''' + str(dist) + '''
Phi:       ''' + str(phi) +  '''
Psi:       ''' + str(psi) +  '''
------------------------------------------------------
'''

# 1 CREATE CLASSES FOR
# system
system = MySystem(axis, alat, dist, phi, psi)
# surface
slab = MySlab(source_slab)
# molecule
mol = MyMolecule(source_molecule)


# create conformations
confs = obtainconfigurations(system, mol, slab)

if dofilter:
   for rule in filterrules:
      confs = filterconfigurations(confs, slab, rule)

# write conformations to QE input files for calculation
if not os.path.exists(qe_inputdir):
    os.makedirs(qe_inputdir)

wqi.write_conf_to_file(confs, slab, qe_input, qe_inputdir, prefix)

if scc:
   wqi.write_submit_script(confs, qe_inputdir, prefix)

print str(len(confs)) + " configurations created."
print '''
------------------------------------------------------
'''

