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
    -d   Input        | QE dump file from pysorb_dump
    -p   Input        | ff.param
    -o   Output, Opt  | fit.dat
    -itp Output, Opt  | potentials.itp (GROMACS topology file)
    -gp  Output, Opt  | potentials.gp (Gnuplot input file)
    -------------------------------------------------------------------------
    -negative  no     | use only structures with negative adsorption energies
    -nco       0      | cut of for "negatvie" energies
    -w         -1     | change weights of energies in fitting (temperature)
-----------------------------------------------------------------------------
'''

# INITIAL PARAMETER
# FILES
param_file = "ff.param"
o_file     = "fit.dat"
itp_file   = "potentials.itp"
gp_file    = "potentials.gp"

# OPTIONS
only_negative = False
weight_fit    = -1
output_o      = False
output_itp    = False
output_gp     = False
#use_simplex = False

if len(sys.argv)>1:
 for i in sys.argv:
  if i.startswith('-'):
   option=i.split('-')[1]
   if option=="d":
     dump_file = sys.argv[sys.argv.index('-d')+1]
   if option=="p":
     param_file = sys.argv[sys.argv.index('-p')+1]
     do_gulp = True
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
   if option=="negative":
     only_negative = True
     negative_co = sys.argv[sys.argv.index('-negative')+1]
   if option=="w":
     weight_fit = int(sys.argv[sys.argv.index('-w')+1])
   if option=="h":
    print(help)
    sys.exit()
else:
 print(help)
 sys.exit()


try:
  dump_file
except NameError:
  print "Dump file not defined. (-d)"
  sys.exit()

try:
  param_file
except NameError:
  print "Parameter file not defined. (-p)"
  sys.exit()

# Open dump file and create list of QEoutDump()
qe_calcs = IO.read_dump(dump_file)


# ------------------------------------------------- GULP FIT ---------------------------------------------------------
# @@ in eine eigene funktion umschreiben: gulp_fit() @@
# open gulp files
gulp_in_file, gulp_out_file = gulp.gulp_run_init(param_file)

gulp_in = file(gulp_in_file, 'wb')

# GULP FILE HEADER
gulp_in.write('fit comp noflags \n')

# write QEoutDump to gulp file
for calc in qe_calcs:
   gulp_in.write('cell \n')
   cell = calc.getcell()
   gulp_in.write("%9.6f %9.6f %9.6f %9.6f %9.6f %9.6f \n" % (cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]) )
   gulp_in.write('cartesian \n')
   labels = calc.getlabels()
   atoms  = calc.getatompositions()
   for a in range(len(labels)):
      atom = atoms[a]
      gulp_in.write("%-2s %9.6f %9.6f %9.6f\n" % (labels[a], atom[0], atom[1], atom[2]))
   gulp_in.write('observable\nenergy ev\n' + str(calc.getenergy()))
   if weight_fit != -1:
       weight = calc_weight(calc.getenergy(), weight_fit)
       gulp_in.write(' ' + str(weight))
   gulp_in.write('\nend\n\n')

# LJ paramerers from -p input
ff = open(param_file, 'r')
ff_params = ff.readlines()
ff.close()
for line in ff_params:
    #if "core" in line:
    #    gulp_in.write(" ".join(line.split()[0:7]) + " 1 1\n")
    #else:
    gulp_in.write(line)

# CLOSE INPUT FILE
gulp_in.close()

# RUN GULP
sub.call(['/bin/bash',
                '-i',
                '-c',
                "gulp <" + gulp_in_file + " > " + gulp_out_file])

# Read Gulp output
gulp_calc = GULPout(gulp_out_file)

# ------------------------------------------------GULP FIT DONE -------------------------------------------------

# write adsorption E from both to one file
if output_o:
    IO.write_e_after_fit(qe_calcs, gulp_calc, ff_params, o_file)
if output_itp:
    IO.write_potentials_GROMACS(gulp_calc, itp_file)
if output_gp:
    IO.write_potentials_gnuplot(gulp_calc, gp_file)
    


# get reference energy for QE IN THE BEGINING!!!
#ref = open(gulp_dir + '/e.ref', 'r')
#ref_content = ref.readlines()
#ref.close()
#e_sys = 0
#for e in ref_content:
#   e_sys = e_sys + convert.ry2ev(float(e))

# get the file names
#out_file_names = [f for f in sorted(os.listdir(output_dir)) if os.path.isfile(os.path.join(output_dir,f))]
#
## make list of QEout
#out_files = [QEout(os.path.join(output_dir,f)) for f in out_file_names]
#
## sort out if E_ads is > 0
##out_files = [f for f in out_files if convert.ry2ev(float(f.getenergy()))-e_sys < 0]
#
#
## open gulp file and write header
#gulp_in = gulp_dir + '/e_gulp.gin'
#gulp_out = gulp_dir +'/e_gulp.gout'
#gulp = file(gulp_in, 'w')
#if use_simplex:
#    gulp.write('fit simplex comp noflags \n')
#else:
#    gulp.write('fit comp noflags \n')
#
#
#
#
## write QEout to file
#for calc in out_files:
#   gulp.write('cell \n')
#   cell = calc.makecellparams()
#   gulp.write("%9.6f %9.6f %9.6f %9.6f %9.6f %9.6f \n" % (cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]) )
#   gulp.write('cartesian \n')
#   labels = calc.getlabels()
#   atoms  = calc.getatompositions()
#   for a in range(len(labels)):
#      atom = atoms[a,:]
#      gulp.write("%-2s %9.6f %9.6f %9.6f\n" % (labels[a], atom[0], atom[1], atom[2]))
#   gulp.write('observable\nenergy ev\n')
#   gulp.write(str(convert.ry2ev(float(calc.getenergy()))-e_sys) + '\nend\n\n')
#
#
## LJ paramerers (has to be read from a file)
#ff = open(gulp_dir + '/ff.param', 'r')
#ff_params = ff.readlines()
#ff.close()
#
#for line in ff_params:
#   gulp.write(line + '\n')
#
#gulp.close()
#
## RUN GULP
#sub.call(['/bin/bash',
#                '-i',
#                '-c',
#                "gulp <" + gulp_in + " > " + gulp_out])
#
## Read Gulp output to list
#gout = file(gulp_out, 'r')
#gout_content = gout.readlines()
#gout.close()
#
## read content of GULP output
#hit1 = 'Total lattice energy       ='
#hit2 = 'eV'
#
#e_gulp = [line.split()[4] for line in gout_content if hit1 in line and hit2 in line ]
#e_gulp = [float(i) for i in e_gulp]
#e_gulp = np.asarray(e_gulp)
#
## qe adsorbtion E in one list
#e_qe = [convert.ry2ev(float(calc.getenergy()))-e_sys for calc in out_files]
#
#e_file = file(gulp_dir + '/e.out', 'w')
#
#for i in np.arange(len(e_qe)):
#   e_file.write("%9.6f %9.6f\n" % (e_qe[i], e_gulp[i]))
#
#e_file.close()
#
## calc rmsd
#rms = 0
#for i in np.arange(len(e_qe)):
#   rms = rms + math.pow(e_qe[i]-e_gulp[i], 2)
#
#rms = math.sqrt(rms/len(e_qe))
#
##r = open(gulp_dir + '/rms.out', 'w')
##r.write(str(rms))
##r.close()
#
## gnuplot data
#axis_max=str(max(max(e_qe), max(e_gulp))*1.1)
#axis_min=str(min(min(e_qe), min(e_gulp))*1.1)
#
#gnplt = '''
#reset
#set terminal pngcairo size 800,800 enhanced font 'Verdana,10'
#set output "''' + gulp_dir + '''/e.png"
#set title "''' + gulp_dir + '''\\n RMS: ''' + str(rms) + '''"
## Line styles
#set border linewidth 1.5
#set style line 1 linecolor rgb '#000000' ps 3  # black X
#set style line 2 linecolor rgb '#dd181f' linetype 1 linewidth 1  # red line
## Axes label 
#set xlabel 'E_{ads-quantum} (eV)'
#set ylabel 'E_{ads-classic} (eV)'
## Axis ranges
#set xrange[''' + axis_min + ':' + axis_max + ''']
#set yrange[''' + axis_min + ':' + axis_max + ''']
#f(x) = x
## Plot
#plot f(x) notitle with line ls 2, \\
#     "''' + gulp_dir + '''/e.out" using 1:2 notitle with points ls 1
#'''
#
#g = open(gulp_dir + '/plot.gnu', 'w')
#g.write(gnplt)
#g.close()
#
#sub.call(['/bin/bash',
#                '-i',
#                '-c',
#                "gnuplot " + gulp_dir + "/plot.gnu"])
#
