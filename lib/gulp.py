#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 18.01.16
# 
# functions for GULP calculations
#### ------------------------------------------ ####
import datetime
import os
import time


# create dictionary for gulp run files and create file names for input and output files
def gulp_run_init(param_file):
    if not os.path.exists("gulp_run_files"):
       os.makedirs("gulp_run_files")
       print "Creating dictionary for GULP run files."
    param_file = os.path.basename(param_file).split(".")[0]
    ts         = time.time()
    tstamp     = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
    file_name  = os.path.join("gulp_run_files", tstamp + "_" + param_file)
    return file_name + ".gin", file_name + ".gout"



#
#def fit():
#    return()
#
## open gulp files
#gulp_in_file = 'tmp.gin' 
#gulp_out_file = 'tmp.gout'
#gulp_in = open(gulp_in_file, 'wb')
#
## GULP FILE HEADER
#gulp_in.write('fit comp noflags \n')
#
## write QEoutDump to gulp file
#for calc in qe_calcs:
#   gulp_in.write('cell \n')
#   cell = calc.getcell()
#   gulp_in.write("%9.6f %9.6f %9.6f %9.6f %9.6f %9.6f \n" % (cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]) )
#   gulp_in.write('cartesian \n')
#   labels = calc.getlabels()
#   atoms  = calc.getatompositions()
#   for a in range(len(labels)):
#      atom = atoms[a]
#      gulp_in.write("%-2s %9.6f %9.6f %9.6f\n" % (labels[a], atom[0], atom[1], atom[2]))
#   gulp_in.write('observable\nenergy ev\n')
#   gulp_in.write(str(calc.getenergy()) + '\nend\n\n')
#
## LJ paramerers from -p input
#ff = open(param_file, 'r')
#ff_params = ff.readlines()
#ff.close()
#for line in ff_params:
#    if "core" in line:
#        gulp_in.write(" ".join(line.split()[0:7]) + " 1 1\n")
#    else:
#        gulp_in.write(line)
#
## CLOSE INPUT FILE
#gulp_in.close()
#
## RUN GULP
#sub.call(['/bin/bash',
#                '-i',
#                '-c',
#                "gulp <" + gulp_in_file + " > " + gulp_out_file])
#
## Read Gulp output
#gulp_calc = GULPout(gulp_out_file)

