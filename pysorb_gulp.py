#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 03.04.16
# 
# program to summarize GULP output
#### ------------------------------------------ ####

import os, sys, os.path
import subprocess as sub
import math

from classes.QEout import *
from classes.GULPout import *
from lib.helper import calc_weight
import lib.IO as IO
import lib.convert
import lib.gulp as gulp



help = '''
------------------------  pysorb qe2gulp  ------------------------------------

Options:
    -h                | display help message
    -gout   Input        | Gulp output file
    -o      Output, Opt  | fit.dat
    -itp    Output, Opt  | potentials.itp (GROMACS topology file)
    -gp     Output, Opt  | potentials.gp (Gnuplot input file)
-----------------------------------------------------------------------------
'''

# INITIAL PARAMETER
# FILES
gout_file  = "fit.gout"
o_file     = "fit.dat"
itp_file   = "potentials.itp"
gp_file    = "potentials.gp"

# OPTIONS
only_negative = False
weight_fit    = -1
output_o      = True
output_itp    = False
output_gp     = False
#use_simplex = False

if len(sys.argv)>1:
 for i in sys.argv:
  if i.startswith('-'):
   option=i.split('-')[1]
   if option=="gout":
     gout_file = sys.argv[sys.argv.index('-gout')+1]
   if option=="o":
     try:
         o_file = sys.argv[sys.argv.index('-o')+1]
     except:
         pass
     output_o = True
   if option=="itp":
     try:
         itp_file = sys.argv[sys.argv.index('-itp')+1]
     except:
         pass
     output_itp = True
   if option=="gp":
     try:
         gp_file = sys.argv[sys.argv.index('-gp')+1]
     except:
         pass
     output_gp = True
   if option=="h":
    print(help)
    sys.exit()
else:
 print(help)
 sys.exit()


# Read Gulp output
gulp_calc = GULPout(gout_file)

# ------------------------------------------------GULP FIT DONE -------------------------------------------------

# write adsorption E from both to one file
if output_o:
    IO.write_e_after_fit_mod(gulp_calc, o_file)
if output_itp:
    IO.write_potentials_GROMACS(gulp_calc, itp_file)
if output_gp:
    IO.write_potentials_gnuplot(gulp_calc, gp_file)
