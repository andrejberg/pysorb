#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 18.01.16
# 
# functions to convert units
# added some new functions
# would be nice if function could also convert arrays or lists
#### ------------------------------------------ ####
import numpy as np

# distances
# to nm
def ang2nm(ang):
    return(ang * 0.1)
def bohr2nm(bohr):
    return(bohr * 0.0529)


# from nm
def nm2ang(nm):
    return(nm / 0.1)
def nm2bohr(nm):
    return(nm / 0.0529)


def bohr2ang(bohr):
   return(bohr * 0.529)

def ang2bohr(ang):
    return(ang / 0.529)

def d(from_unit, to_unit, x):
    # input:  "nm", "Ang", float
    # output: float
    factor = { "bohr"  : 0.0529, 
               "Ang"   : 0.1,
               "nm"    : 1.0}
    if hasattr(x, '__iter__'):
        return(np.asarray([(i * factor[from_unit] / factor[to_unit]) for i in x]))
    else:
        return(x * factor[from_unit] / factor[to_unit])




# energies
# to kJ
def ry2kj(ry):
    return(ry * 13.60569253 * 1.60217733E-022 * 6.022E+023)
def ev2kj(ev):
    return(ev * 1.60217733E-022 * 6.022E+023)
def kcal2kj(kcal):
    return(kcal * 4.1897)

# from kJ
def kj2ry(kj):
    return(kj / (13.60569253 * 1.60217733E-022 * 6.022E+023))
def kj2ev(kj):
    return(kj / (1.60217733E-022 * 6.022E+023))
def kj2kcal(kj):
    return(kj / 4.1897)

# das hier wird dann depricated
def ry2ev(ry):
   return(ry * 13.60569253)

def ev2ry(ev):
   return(ev / 13.60569253)


def e(from_unit, to_unit, x):
    # input:  "eV", "kJ", float
    # output: float
    factor = { "Ry"   : (13.60569253 * 1.60217733E-022 * 6.022E+023), 
               "eV"   : (1.60217733E-022 * 6.022E+023),
               "kcal" : (4.1897),
               "kJ"   : 1.0}
    if hasattr(x, '__iter__'):
        return(np.asarray([(i * factor[from_unit] / factor[to_unit]) for i in x]))
    else:
        return(x * factor[from_unit] / factor[to_unit])
