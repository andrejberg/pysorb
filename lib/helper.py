#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 29.06.2015
# 
# helper functions
#### ------------------------------------------ ####
from math import *
import numpy as np

k_b = 1.3805E-23 # bolzmann constant


# get center vector. wrong for two vectors if c=(000) ?
def center(a, b, c=[0, 0, 0]):
    ab = [(a[0]+b[0])/2, (a[1]+b[1])/2, (a[2]+b[2])/2]
    abc = [(ab[0]+c[0])/2, (ab[1]+c[1])/2, (ab[2]+c[2])/2]
    return abc
    
def axis_str(i):
    if i == 1:
        return 'x'
    elif i == 2:
        return 'y'
    elif i == 3:
        return 'z'

def distance(a, b):
    d = sqrt(pow((a[0]-b[0]), 2) + pow((a[1]-b[1]), 2) + pow((a[2]-b[2]), 2))
    return d

def compare_e(e1, e2):
    delta_e = e1 - e2
    sq      = np.square(delta_e)
    return (np.max(delta_e), np.sum(sq), np.mean(sq), np.std(sq))
    

def calc_weight(e, t):
    beta = 1/(k_b*t)
    sig = 100/(1 + exp(1E-20*beta*e))
    return sig

# added 24.01.17 (from analysis of gold slab simulations)
def water_mol_orientation(mol, z):
    # mol is a 3x3 array of positions
    # z is orthogonal to surface plane
    b1 = mol[1] - mol[0] # bond 1
    b2 = mol[2] - mol[0] # bond 2
    d  = b1 + b2         # dipole vector
    o1 = np.cross(b1,b2)
    o2 = np.cross(b2,b1)
    
    z_mag  = np.linalg.norm(z)
    d_mag  = np.linalg.norm(d)
    o1_mag = np.linalg.norm(o1)
    o2_mag = np.linalg.norm(o2)
    
    fi     = acos(np.dot(d,z)/(d_mag*z_mag))
    theta1 = acos(np.dot(o1,z)/(o1_mag*z_mag))
    theta2 = acos(np.dot(o2,z)/(o2_mag*z_mag))
    theta  = min(theta1, theta2)
    return degrees(fi),degrees(theta)
