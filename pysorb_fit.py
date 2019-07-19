#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 29.04.15
# 
# program to summarize QE outputfiles to a GULP
# fitting run
#### ------------------------------------------ ####

import os, sys, os.path
import subprocess as sub
import math

from classes.QEoutDump import *
from classes.GULPout import *
from lib.helper import calc_weight
import lib.IO as IO
import lib.convert
import lib.gulp as gulp

help = '''
------------------------  pysorb qe2gulp  ------------------------------------

Options:
    -h                | display help message
    -d   Input        | QE dump file from pysorb_dump
    -p   Input        | ff.param
    -o   Output       | fit.gin
    -------------------------------------------------------------------------
    -w                | add Boltzmann weight for fitting
    -t   300          | temperature for Boltzmann weight calculation
-----------------------------------------------------------------------------
'''

# INITIAL PARAMETER
# FILES
dump_file = "dump.qedump"
param_file = "ff.param"
output_file = "fit.gin"
t = 300.0
# param_file = "ff.param"
# o_file     = "fit.dat"
# itp_file   = "potentials.itp"
# gp_file    = "potentials.gp"

# OPTIONS
# only_negative = False
weight_fit = False
# output_o      = False
# output_itp    = False
# output_gp     = False
# use_simplex = False

if len(sys.argv) > 1:
    for i in sys.argv:
        if i.startswith('-'):
            option = i.split('-')[1]
            if option == "d":
                dump_file = sys.argv[sys.argv.index('-d') + 1]
            if option == "p":
                param_file = sys.argv[sys.argv.index('-p') + 1]
            if option == "o":
                output_file = sys.argv[sys.argv.index('-o') + 1]
            # if option=="itp":
            #   try:
            #       itp_file = sys.argv[sys.argv.index('-itp')+1]
            #   except:
            #       pass
            #   output_itp = True
            # if option=="gp":
            #   try:
            #       gp_file = sys.argv[sys.argv.index('-gp')+1]
            #   except:
            #       pass
            #   output_gp = True
            # if option=="negative":
            #   only_negative = True
            #   negative_co = sys.argv[sys.argv.index('-negative')+1]
            if option == "w":
                weight_fit = True
            if option == "t":
                t = float(sys.argv[sys.argv.index('-t') + 1])
            if option == "h":
                print(help)
                sys.exit()
else:
    print(help)
    sys.exit()

try:
    dump_file
except NameError:
    print
    "Dump file not defined. (-d)"
    sys.exit()

try:
    param_file
except NameError:
    print
    "Parameter file not defined. (-p)"
    sys.exit()

# Open dump file and create list of QEoutDump()
qe_calcs = IO.read_dump(dump_file)

# ------------------------------------------------- GULP FIT ---------------------------------------------------------
# @@ in eine eigene funktion umschreiben: gulp_fit() @@
# open gulp files
# gulp_in_file, gulp_out_file = gulp.gulp_run_init(param_file)

gulp_in = file(output_file, 'wb')

# GULP FILE HEADER
gulp_in.write('fit comp noflags \n')

# write QEoutDump to gulp file
for calc in qe_calcs:
    gulp_in.write('cell \n')
    cell = calc.getcell()
    gulp_in.write("%9.6f %9.6f %9.6f %9.6f %9.6f %9.6f \n" % (cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]))
    gulp_in.write('cartesian \n')
    labels = calc.getlabels()
    atoms = calc.getatompositions()
    for a in range(len(labels)):
        atom = atoms[a]
        gulp_in.write("%-2s %9.6f %9.6f %9.6f\n" % (labels[a], atom[0], atom[1], atom[2]))
    gulp_in.write('observable\nenergy ev\n' + str(calc.getenergy()))
    if weight_fit:
        weight = calc_weight(calc.getenergy(), t)
        gulp_in.write(' ' + str(weight))
    gulp_in.write('\nend\n\n')

# LJ paramerers from -p input
ff = open(param_file, 'r')
ff_params = ff.readlines()
ff.close()
for line in ff_params:
    # if "core" in line:
    #    gulp_in.write(" ".join(line.split()[0:7]) + " 1 1\n")
    # else:
    gulp_in.write(line)

# CLOSE INPUT FILE
gulp_in.close()

# # RUN GULP
# sub.call(['/bin/bash',
#                 '-i',
#                 '-c',
#                 "gulp <" + gulp_in_file + " > " + gulp_out_file])
#
# # Read Gulp output
# gulp_calc = GULPout(gulp_out_file)
#
# # ------------------------------------------------GULP FIT DONE -------------------------------------------------
#
# # write adsorption E from both to one file
# if output_o:
#     IO.write_e_after_fit(qe_calcs, gulp_calc, ff_params, o_file)
# if output_itp:
#     IO.write_potentials_GROMACS(gulp_calc, itp_file)
# if output_gp:
#     IO.write_potentials_gnuplot(gulp_calc, gp_file)
