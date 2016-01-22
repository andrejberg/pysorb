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
import subprocess as sub
import math

from classes.QEout import *
import lib.IO as IO
import lib.convert as convert
import lib.gulp as gulp


help = '''
--------------------  pysorb qe2gulp  ---------------

Options:
    -h              display help message
    -d  Input       QE dump file from pysorb_dump
    -p  Input, Opt  ff.param
    -o  Output      qe_E_ads.dat
    -oc Output, Opt class_E_ads.dat
    -op Output, Opt qe_vs_class_E_ads.dat
    --------------------------------------------
    -negative  no   use only structures with negative adsorption energies
    -nco       0    cut of for "negatvie" energies
------------------------------------------------------
'''

# INITIAL PARAMETER
# FILES
param_file="ff.param"
qe_E_ads_file = "qe_E_ads.dat"
calss_E_ads_file = "class_E_ads.dat"
qe_vs_class_E_ads_file = "qe_vs_class_E_ads.dat"


# OPTIONS
do_gulp = False
only_negative = False
output_o = False
output_oc = False
output_op = False


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
         qe_E_ads_file = sys.argv[sys.argv.index('-o')+1]
     except:
         pass
     output_o = True
   if option=="oc":
     try:
         calss_E_ads_file = sys.argv[sys.argv.index('-oc')+1]
     except:
         pass
     output_oc = True
     do_gulp = True
   if option=="op":
     try:
         qe_vs_class_E_ads_file = sys.argv[sys.argv.index('-op')+1]
     except:
         pass
     output_op = True
     do_gulp = True
   if option=="negative":
     only_negative = True
     negative_co = sys.argv[sys.argv.index('-negative')+1]
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

if do_gulp:
    try:
      param_file
    except NameError:
      print "Parameter file not defined. (-p)"
      sys.exit()


# Open dump file and create list of QEoutDump()
qe_calcs = IO.read_dump(dump_file)





# -----------------------------------------------CLASSICAL CALCLUATION--------------------------------------------------
# @@ in eine eigene funktion umschreiben: gulp_calc() @@
if do_gulp:
    # open gulp files
    gulp_in_file, gulp_out_file = gulp.gulp_run_init(param_file)
#    gulp_in_file = 'tmp.gin' 
#    gulp_out_file = 'tmp.gout'
    gulp_in = file(gulp_in_file, 'wb')
    
    # GULP FILE HEADER
    gulp_in.write('energy comp noflags \n')
    
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
       gulp_in.write('\n \n')
    
    # LJ paramerers from -p input
    ff = open(param_file, 'r')
    ff_params = ff.readlines()
    ff.close()
    for line in ff_params:
       gulp_in.write(line)
    
    # CLOSE INPUT FILE
    gulp_in.close()
    
    # RUN GULP
    sub.call(['/bin/bash',
                    '-i',
                    '-c',
                    "gulp <" + gulp_in_file + " > " + gulp_out_file])
    
    # Read Gulp output: Energies in one array
    gulp_out = file(gulp_out_file, 'r')
    gulp_out_content = gulp_out.readlines()
    gulp_out.close()
    hit1 = 'Total lattice energy       ='
    hit2 = 'eV'
    e_gulp = [line.split()[4] for line in gulp_out_content if hit1 in line and hit2 in line ]
    e_gulp = np.asarray([float(i) for i in e_gulp])

# -------------------------------------------CLASSICAL CALCULATION DONE -------------------------------------------

# write adsorption E from QE to file
if output_o:
    IO.write_e_qe(qe_calcs, qe_E_ads_file)

# write adsorption E from GULP to file
if output_oc:
    IO.write_e_gulp(qe_calcs, e_gulp, calss_E_ads_file)

# write adsorption E from both to one file
if output_op:
    IO.write_e(qe_calcs, e_gulp, qe_vs_class_E_ads_file)


## write adsorption E in tex file
#if not os.path.exists(os.path.join(gulp_dir,  'tex')):
#    os.mkdir(os.path.join(gulp_dir,  'tex'))
#tex_file=file(os.path.join(gulp_dir, 'tex', 'table.tex'),  'w')
#tex_file.write('''\documentclass[10pt,a4paper]{article}
#\usepackage[utf8]{inputenc}
#\usepackage{amsmath}
#\usepackage{amsfonts}
#\usepackage{amssymb}
#\usepackage{longtable}
#\\begin{document}
#''')
#tex_file.write('\\begin{longtable}{cccccccc}\n\hline\nprefix & $Atom_{Molecule}$ & $Atom_{Surface}$ & d & $\phi$ & $\psi$ & $E_{DFT}$ & $E_{classic}$ \\\\\n\hline\n')
#for i in np.arange(len(e_qe)):
#    name = out_file_names[i].split('.')
#    tex_file.write("%s & %s & %s & %s & %s & %s & %9.6f & %9.6f\\\\\n" % (name[0], name[1], name[2], name[4] + '.' + name[5], name[7], name[9], e_qe[i], e_gulp[i]))
#    tex_file.write('\hline \n')
#tex_file.write('\end{longtable}\n\end{document}')
#tex_file.close()
#
#
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
