#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 18.01.16
# 
# IO functions
#### ------------------------------------------ ####

import numpy as np

from classes.QEout import *
import convert as convert
import helper as helper

# ----------------------------------------------------- START INPUT -----------------------------------------------------
def read_dump(dump_file):
    # input:  dump file "example.qed"
    # output: [QEoutDump()]
    dump         = open(dump_file, "r")
    dump_content = dump.readlines()
    dump.close()
    dump_entries = []
    entry        = []
    for line in dump_content:
        if "START" not in line and "END" not in line:
            entry.append(line)
        if "END" in line:
            dump_entries.append(entry)
            entry = []
    qe_calcs = [QEoutDump(entry) for entry in dump_entries]
    return qe_calcs


# ----------------------------------------------------- END INPUT -----------------------------------------------------

# ----------------------------------------------------- START OUTPUT -----------------------------------------------------

# output strings and formats
output_string = { 0 : ("index", ), 
                  1 : ("e_QE", ), 
                  2 : ("e_GP", ), 
                  3 : ("e_GP_init", ), 
                  4 : ("e_GP_final", ), 
                  5 : ("dist", "phi", "psi", "atom_ads", "prefix")}
output_format = { 0 : ("%6s", "%8i"), 
                  1 : ("%14s", "%14.6f"), 
                  2 : ("%14s", "%14.6f"),
                  3 : ("%14s", "%14.6f"),
                  4 : ("%14s", "%14.6f"),
                  5 : ("%10s%10s%10s%10s%10s", "%10.3f%10i%10i%10s%10s")}

head = { "simple_QE" : ("# " + output_format[0][0] + output_format[1][0] + output_format[5][0] + "\n", 
                               output_string[0]    + output_string[1]    + output_string[5]), 
         "simple_GP" : ("# " + output_format[0][0] + output_format[2][0] + output_format[5][0] + "\n", 
                               output_string[0]    + output_string[2]    + output_string[5]), 
         "compare"   : ("# " + output_format[0][0] + output_format[1][0] + output_format[2][0] + output_format[5][0] + "\n", 
                               output_string[0]    + output_string[1]    + output_string[2]    + output_string[5]), 
         "fit"       : ("# " + output_format[0][0] + output_format[1][0] + output_format[3][0] + output_format[4][0] + output_format[5][0] + "\n", 
                               output_string[0]    + output_string[1]    + output_string[3]    + output_string[4]    + output_string[5])}

body = { "simple_QE" : output_format[0][1] + output_format[1][1] + output_format[5][1] + "\n", 
         "simple_GP" : output_format[0][1] + output_format[2][1] + output_format[5][1] + "\n", 
         "compare"   : output_format[0][1] + output_format[1][1] + output_format[2][1] + output_format[5][1] + "\n", 
         "fit"       : output_format[0][1] + output_format[1][1] + output_format[3][1] + output_format[4][1] + output_format[5][1] + "\n"}

# @@ Die funktion gefaellt mir nicht da sie eine schon offene file braucht
# write numerical analysis of to energy sets
def write_e_analysis(e1, e2, name, out):
    out.write("# " + name + "\n")
    out.write("# " + "-" * 80 + "\n")
    out.write("# Dmax SOS MSD MSDstd %11.6f %11.6f %11.6f %11.6f \n" % helper.compare_e(e1, e2))
    out.write("# " + "-" * 80 + "\n\n")

# nice output of potentials
def write_potentials(potentials, name, out):
    e_unit_in  = "eV"
    e_unit_out = "kJ"
    d_unit_in  = "Ang"
    d_unit_out = "nm"
    out.write("# " + name + "(" + e_unit_out + " | " + d_unit_out + ")" + "\n")
    out.write("# " + "-" * 80 + "\n")
    for pot in potentials:
        t1, t2, pt, eps, sig = pot["type1"], pot["type2"], pot["ptype"], pot["epsilon"], pot["sigma"]
        eps = convert.e(e_unit_in, e_unit_out, eps)
        sig = convert.d(d_unit_in, d_unit_out, sig)
        out.write("# %5s%5s%12.6f%12.6f%8s\n" % (t1, t2, eps, sig, pt))
    out.write("# " + "-" * 80 + "\n\n")

# write energies from QE to file
def write_e_qe(qe_calcs, f):
    # input:  [QEoutDump()], "file.txt"
    # output: write to file
    e_unit_in  = "eV"
    e_unit_out = "kJ"
    d_unit_in  = "Ang"
    d_unit_out = "nm"

    qe_E_ads   = open(f, 'wb')
    qe_E_ads.write(head["simple_QE"][0] % head["simple_QE"][1])
    i = 0
    for calc in qe_calcs:
        e = convert.e(e_unit_in, e_unit_out, calc.getenergy())
        d = convert.d(d_unit_in, d_unit_out, calc.getdist())
        qe_E_ads.write(body["simple_QE"] % (i, e, d, calc.getphi(), calc.getpsi(), calc.getadsorbedatom(), calc.getprefix()))
        i += 1
    qe_E_ads.close()

# write adsorption E from GULP to file
def write_e_gulp(qe_calcs, e_gulp, f):
    # input:  [QEoutDump()], [float.e_gulp], "file.txt"
    # output: write to file
    e_unit_in   = "eV"
    e_unit_out  = "kJ"
    d_unit_in   = "Ang"
    d_unit_out  = "nm"
    calss_E_ads = open(f, 'wb')
    calss_E_ads.write(head["simple_GP"][0] % head["simple_GP"][1])
    i = 0
    for calc in qe_calcs:
        e = convert.e(e_unit_in, e_unit_out, e_gulp[i])
        d = convert.d(d_unit_in, d_unit_out, calc.getdist())
        calss_E_ads.write(body["simple_GP"] % (i, e, d, calc.getphi(), calc.getpsi(), calc.getadsorbedatom(), calc.getprefix()))
        i += 1
    calss_E_ads.close()

# write adsorption E from both to one file
def write_e(qe_calcs, e_gulp, f):
    # input:  [QEoutDump()], [float.e_gulp], "file.txt"
    # output: write to file
    e_unit_in   = "eV"
    e_unit_out  = "kJ"
    d_unit_in   = "Ang"
    d_unit_out  = "nm"
    e_qe        = convert.e(e_unit_in, e_unit_out, np.asarray([calc.getenergy() for calc in qe_calcs]))
    e_gulp      = convert.e(e_unit_in, e_unit_out, e_gulp)
    qe_vs_class_E_ads = file(f,  'wb')
    qe_vs_class_E_ads.write("# " + "-" * 100 + "\n")
    write_e_analysis(e_qe, e_gulp, "Energies", qe_vs_class_E_ads)
    qe_vs_class_E_ads.write("# " + "-" * 100 + "\n\n")
    qe_vs_class_E_ads.write(head["compare"][0] % head["compare"][1])
    i = 0
    for calc in qe_calcs:
        e_qe = convert.e(e_unit_in, e_unit_out, calc.getenergy())
        e_gp = convert.e(e_unit_in, e_unit_out, e_gulp[i])
        d    = convert.d(d_unit_in, d_unit_out, calc.getdist())
        qe_vs_class_E_ads.write(body["compare"] % (i, e_qe, e_gp, d, calc.getphi(), calc.getpsi(), calc.getadsorbedatom(), calc.getprefix()))
        i+=1
    qe_vs_class_E_ads.close()

#write adsorption E after fit. Here e_gulp is printed before and after fit
def write_e_after_fit(qe_calcs, gulp_calc, ff_params, f):
    # input:  GULPout, "file.txt"
    # output: write to file
    e_unit_in   = "eV"
    e_unit_out  = "kJ"
    d_unit_in   = "Ang"
    d_unit_out  = "nm"

    e_qe    = convert.e(e_unit_in, e_unit_out, gulp_calc.e_qe)
    e_init  = convert.e(e_unit_in, e_unit_out, gulp_calc.e_init)
    e_final = convert.e(e_unit_in, e_unit_out, gulp_calc.e_fin)
    
    out = file(f, 'wb')
    out.write("# " + "-" * 100 + "\n")
    out.write("# Initial input for interatomic potentials\n")
    for line in ff_params:
        out.write("# " + line)
    out.write("# " + "-" * 100 + "\n\n")
    
    out.write("# " + "-" * 100 + "\n")
    write_e_analysis(e_qe, e_init, "Initial energies:", out)
    write_potentials(gulp_calc.pot_init, "Initial potentials:", out)
    for line in gulp_calc.rawpot_init:
        out.write("# " + line)
    out.write("# " + "-" * 100 + "\n\n")
    
    out.write("# " + "-" * 100 + "\n")
    write_e_analysis(e_qe, e_final, "Final energies:", out)
    write_potentials(gulp_calc.pot_final, "Final potentials:", out)
    for line in gulp_calc.rawpot_final:
        out.write("# " + line)
    out.write("# " + "-" * 100 + "\n\n")
    
    out.write(head["fit"][0] % head["fit"][1])
    i = 0
    for calc in qe_calcs:
        d   = convert.d(d_unit_in, d_unit_out, calc.getdist())
        out.write(body["fit"] % (i, e_qe[i], e_init[i], e_final[i], d, calc.getphi(), calc.getpsi(), calc.getadsorbedatom(), calc.getprefix()))
        i+=1
    out.close()

def write_potentials_GROMACS(gulp_calc, f):
    e_unit_in   = "eV"
    e_unit_out  = "kJ"
    d_unit_in   = "Ang"
    d_unit_out  = "nm"
    
    out = file(f, 'wb')
    out.write("; GROMACS topology file \n")
    out.write("; #include \"" + f + "\" in [ nonbond_params ] section \n")
    for pot in gulp_calc.pot_final:
        t1, t2, pt, eps, sig = pot["type1"], pot["type2"], pot["ptype"], pot["epsilon"], pot["sigma"]
        eps = convert.e(e_unit_in, e_unit_out, eps)
        sig = convert.d(d_unit_in, d_unit_out, sig)
        if pt == "12_6":
            A =     eps * math.pow(sig, 12)
            B = 2 * eps * math.pow(sig, 6)
        elif pt == "9_6":
            A = 2 * eps * math.pow(sig, 9)
            B = 3 * eps * math.pow(sig, 6)
        out.write("%10s%10s%12i%16.6e%16.6e   ;%10s\n" % (t1, t2, 1, B, A, pt))
    out.close()
    
def write_potentials_gnuplot(gulp_calc, f):
    e_unit_in   = "eV"
    e_unit_out  = "kJ"
    d_unit_in   = "Ang"
    d_unit_out  = "nm"
    out = file(f, 'wb')
    out.write("# Functions to plot\n")
    out.write("s(x)         = 0\n")
    out.write("f(x,eps,sig) = eps*((sig/x)**12-2*(sig/x)**6) # LJ12_6\n")
    out.write("g(x,eps,sig) = eps*(2*(sig/x)**9-3*(sig/x)**6) # LJ9_6\n\n")
    out.write("plot s(x) with line ls 11 not, \\\n")
    for pot in gulp_calc.pot_final:
        t1, t2, pt, eps, sig = pot["type1"], pot["type2"], pot["ptype"], pot["epsilon"], pot["sigma"]
        eps = convert.e(e_unit_in, e_unit_out, eps)
        sig = convert.d(d_unit_in, d_unit_out, sig)
        if pt == "12_6":
            out.write("     f(x,%9.6f,%9.6f) with line ls 1 not, \\\n" % (eps, sig))
        elif pt == "9_6":
            out.write("     g(x,%9.6f,%9.6f) with line ls 1 not, \\\n" % (eps, sig))
    out.close()
# ----------------------------------------------------- END INPUT -----------------------------------------------------








