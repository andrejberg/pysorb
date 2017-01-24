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
    r2      = r_squared(e1, e2)
    return (np.max(delta_e), np.sum(sq), np.mean(sq), np.std(sq), r2)
    

def calc_weight(e, t):
    beta = 1/(k_b*t)
    sig = 100/(1 + exp(1E-20*beta*e))
    return sig

def r_squared(e_obs, e_model):
    mean = np.mean(e_obs)
    dev = np.sum((e_obs - mean)**2.0)
    res = np.sum((e_obs - e_model)**2.0)
    r2 = 1 - res/dev
    r2_adj = r2 - (1-r2)/(len(e_obs-2))
    return (r2_adj)
    
