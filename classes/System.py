#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 29.06.2015
# 
# Class to hold parameters for creation of 
# configurations
#### ------------------------------------------ ####


# wofuer war das nochmal????:
# warnings.simplefilter("ignore")



# --------------------------------------------------------------------------------------------
class MySystem:

   def __init__(self, axis, alat, dist, angrot, angads):

         # integer:       1, 2, 3
         self.axis      = axis

         # foat           0 for cartesian coordinates
         self.alat      = alat

         # array[float]   [1.5, 1.75, 2.0] distances between adsorbed molecule and slab
         self.dist      = dist

         # array[float]   [45, 90, 135] angles to rotate molecule about "z" axis
         self.angrot    = angrot

         # array[flaot]   [45, 90] angles to rotate molecule about "x" axis
         self.angads    = angads
