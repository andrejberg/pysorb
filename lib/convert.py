#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 18.01.16
# 
# functions to convert units
# added some new functions
# would be nice if function could also convert arrays or lists
#### ------------------------------------------ ####

# distances
def bohr2ang(bohr):
   return(bohr * 0.529)

def ang2bohr(ang):
    return(ang / 0.529)
# --
def ang2nm(ang):
    return(ang / 10)

def nm2ang(nm):
    return(nm * 10)


# energies
def ry2ev(ry):
   return(ry * 13.60569253)

def ev2ry(ev):
   return(ev / 13.60569253)
# --
def ev2kJ(ev):
    return(ev * (1.60217733E-022 * 6.022E+023))

def kJ2ev(kJ):
    return(kJ / (1.60217733E-022 * 6.022E+023))
# --
def kcal2kJ(kcal):
    return(kcal * 4.1897)

def kJ2kcal(kJ):
    return(kJ / 4.1897)
