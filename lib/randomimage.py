#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 03.04.15
# 
# class and funktion to get a random distributed
# image of a (gold) surface for GolP models
# 
# class should have an additional atribute for
# labels
#### ------------------------------------------ ####


import math
import random
import numpy as np
import transformations as trans

class MyImage:
   def __init__(self, positions):
      self.positions    = positions


def getrandomimage(obj, distance=0.7):
   imagepositions = []

   for atom in obj.positions:
      matrix = trans.random_rotation_matrix()
      image  = np.dot([distance, 0.0, 0.0], matrix[:3,:3].T)
      matrix = trans.translation_matrix(atom)
      image = np.dot(np.append(image, 1), matrix.T)[:3]
      imagepositions = np.append(imagepositions, image)

   imagepositions = imagepositions.reshape(-1,3)

   return(MyImage(imagepositions))

def getdist(a, b):
   dist = math.sqrt(math.pow(a[0]-b[0], 2)+math.pow(a[1]-b[1], 2)+math.pow(a[2]-b[2], 2))
   return dist


# DEV

#def randomangle():
#   return(random.vonmisesvariate(0,0))
"""
slab = MySlab("gold.pos")

print slab.positions

image = getrandomimage(slab)

print image.positions

b = 0
for a in image.positions:
   print(getdist(a, slab.positions[b]))
   b+=1
"""
