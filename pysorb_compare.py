#! /usr/bin/python

#### ------------------------------------------ ####
# edit: 29.04.15
# 
# program to summarize QE outputfiles to a GULP
# energy calculation
# 
# edit 11.08.15
# input is now a dump file
# add options:
# -negative
#### ------------------------------------------ ####

import os, sys, os.path
# import subprocess as sub
import math

from classes.QEout import *
import lib.IO as IO
import lib.convert as convert
import lib.gulp as gulp

help = '''
--------------------  pysorb qe2gulp  ---------------

Options:
    -h               display help message
    -d  Input        QE dump file from pysorb_dump
    -p  Input        ff.param 
    -o  Output       compare.gin
------------------------------------------------------
'''

# INITIAL PARAMETER
# FILES
dump_file = "dump.qedump"
param_file = "ff.param"
output_file = "compare.gin"
#
# qe_E_ads_file = "qe_E_ads.dat"
# calss_E_ads_file = "class_E_ads.dat"
# qe_vs_class_E_ads_file = "qe_vs_class_E_ads.dat"
# qe_E_ads_geo_file = "qe_E_ads_geo.dat"

# OPTIONS
# do_gulp = False
# only_negative = False
# output_o = False
# output_oc = False
# output_op = False
# output_og = False

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

            # if option == "oc":
            #     try:
            #         calss_E_ads_file = sys.argv[sys.argv.index('-oc') + 1]
            #     except:
            #         pass
            #     output_oc = True
            #     do_gulp = True
            # if option == "op":
            #     try:
            #         qe_vs_class_E_ads_file = sys.argv[sys.argv.index('-op') + 1]
            #     except:
            #         pass
            #     output_op = True
            #     do_gulp = True
            # if option == "negative":
            #     only_negative = True
            #     negative_co = sys.argv[sys.argv.index('-negative') + 1]
            # if option == "og":
            #     try:
            #         qe_E_ads_geo_file = sys.argv[sys.argv.index('-og') + 1]
            #     except:
            #         pass
            #     output_og = True
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

# if do_gulp:
try:
    param_file
except NameError:
    print
    "Parameter file not defined. (-p)"
    sys.exit()

# Open dump file and create list of QEoutDump()
qe_calcs = IO.read_dump(dump_file)

# -----------------------------------------------CLASSICAL CALCLUATION--------------------------------------------------
# @@ in eine eigene funktion umschreiben: gulp_calc() @@
# if do_gulp:
# open gulp files
# gulp_in_file, gulp_out_file = gulp.gulp_run_init(param_file)
#    gulp_in_file = 'tmp.gin'
#    gulp_out_file = 'tmp.gout'
gulp_in = file(output_file, 'wb')

# GULP FILE HEADER
gulp_in.write('energy comp noflags \n')

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
    gulp_in.write('\n \n')

# LJ paramerers from -p input
ff = open(param_file, 'r')
ff_params = ff.readlines()
ff.close()
for line in ff_params:
    gulp_in.write(line)

# CLOSE INPUT FILE
gulp_in.close()

#     # RUN GULP
#     sub.call(['/bin/bash',
#               '-i',
#               '-c',
#               "gulp <" + gulp_in_file + " > " + gulp_out_file])
#
#     # Read Gulp output: Energies in one array
#     gulp_out = file(gulp_out_file, 'r')
#     gulp_out_content = gulp_out.readlines()
#     gulp_out.close()
#     hit1 = 'Total lattice energy       ='
#     hit2 = 'eV'
#     e_gulp = [line.split()[4] for line in gulp_out_content if hit1 in line and hit2 in line]
#     e_gulp = np.asarray([float(i) for i in e_gulp])
#
# # -------------------------------------------CLASSICAL CALCULATION DONE -------------------------------------------
#
# # added 24.01.17
# # change angles to real angles calculated from final structure
# if output_og:
#     IO.write_e_qe_geo(qe_calcs, qe_E_ads_geo_file)
#
# # write adsorption E from QE to file
# if output_o:
#     IO.write_e_qe(qe_calcs, qe_E_ads_file)
#
# # write adsorption E from GULP to file
# if output_oc:
#     IO.write_e_gulp(qe_calcs, e_gulp, calss_E_ads_file)
#
# # write adsorption E from both to one file
# if output_op:
#     IO.write_e(qe_calcs, e_gulp, qe_vs_class_E_ads_file)

