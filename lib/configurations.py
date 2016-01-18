#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 03.04.15
# 
# classes and definitions to read inputfiles and
# position molecule over surface
#
# there is a quite messy print output
# clean this up
#### ------------------------------------------ ####


import math
import numpy as np

import transformations as trans
from classes.Molecule import *
from lib.helper import axis_str

# import warnings
# wofuer war das nochmal????
# warnings.simplefilter("ignore")

## Simple functions
# @@ die function ist auch schon bei helper.py mit drin
def getdist(a, b):
   dist = math.sqrt(math.pow(a[0]-b[0], 2)+math.pow(a[1]-b[1], 2)+math.pow(a[2]-b[2], 2))
   return dist

## Definitions to get the configurations --------------------------

def axisvector(a):
   if a == 1:
      v = np.array([1,0,0])
   if a == 2:
      v = np.array([0,1,0])
   if a == 3:
      v = np.array([0,0,1])
   return(v)

def orthogonalvector(a):
   if a == 1:
      v = np.array([0,1,0])
   if a == 2:
      v = np.array([0,0,1])
   if a == 3:
      v = np.array([1,0,0])
   return(v)

def lineup(system, molecule, atom, index):
    # takes instace of MyMolecule
    # returns an instance of MyMoleculeCopy ORIENTED IN SYSTEM.AXIS DIRECTION
   vector         = molecule.center-atom
   matrix         = trans.rotation_matrix(
                          trans.angle_between_vectors(vector, axisvector(system.axis)),
                          trans.vector_product(vector, axisvector(system.axis)))

   newpositions   = np.array([])

   for atom in molecule.positions:
      newpositions   = np.append(newpositions, np.dot(atom, matrix[:3,:3].T))

   newpositions   = newpositions.reshape(-1,3)
   ads            = []
   index2         = 0 
   for m in molecule.ads:
      if m and index == index2:
          ads.append(True)
          index2 = index2 + 1
      elif m and index != index2:
          ads.append(False)
          index2 = index2 + 1
      else:
          ads.append(False)
   ads = np.array(ads)

   return(MyMoleculeCopy(newpositions, molecule.labels, ads))

def rotate_about_z(system, molecule, angle):
    # takes and returns instance of MyMoleculeCopy

   matrix = trans.rotation_matrix(angle, axisvector(system.axis))

   newpositions      = np.array([])

   for atom in molecule.positions:
      newpositions   = np.append(
                                newpositions,
                                np.dot(atom, matrix[:3,:3].T))

   newpositions   = newpositions.reshape(-1,3)

   return(MyMoleculeCopy(newpositions, molecule.labels, molecule.ads, phi=str(int(angle*360/(2*math.pi)))))

def rotate_about_x(system, molecule, angle):
    # takes and returns instance of MyMoleculeCopy

   matrix = trans.rotation_matrix(angle, orthogonalvector(system.axis))

   newpositions      = np.array([])

   for atom in molecule.positions:
      newpositions   = np.append(
                                newpositions,
                                np.dot(atom, matrix[:3,:3].T))

   newpositions   = newpositions.reshape(-1,3)

   return(MyMoleculeCopy(newpositions, molecule.labels, molecule.ads, phi=molecule.phi, psi=str(int(angle*360/(2*math.pi)))))

def translate(molecule, atom, axis, dist):
    # takes and returns instance of MyMoleculeCopy
    
    toposition = np.copy(atom)
    toposition = np.array([toposition['x'], toposition['y'], toposition['z']])
    toposition[axis-1] = toposition[axis-1] + dist
    toposition = np.reshape(toposition,  (1, 3))
    matrix = trans.translation_matrix(toposition-molecule.positions[molecule.ads][0])
    
    newpositions      = np.array([])
    
    for a in molecule.positions:
        newpositions   = np.append(newpositions, np.dot(np.append(a, 1), matrix.T)[:3])
        
    newpositions   = newpositions.reshape(-1,3)
    
    return(MyMoleculeCopy(newpositions, molecule.labels, molecule.ads, phi=molecule.phi, psi=molecule.psi, slabatom=atom['label']+str(atom['number']) , dist=str(dist)))
    
'''
def translate(molecule, atom, axis, dist, slabatom):
    # takes and returns instance of MyMoleculeCopy

   toposition = np.copy(atom)
   toposition[axis-1] = toposition[axis-1]+dist

   matrix = trans.translation_matrix(toposition-molecule.positions[molecule.ads])

   newpositions      = np.array([])

   for atom in molecule.positions:
      newpositions   = np.append(
                                newpositions,
                                np.dot(np.append(atom, 1), matrix.T)[:3])


   newpositions   = newpositions.reshape(-1,3)

   return(MyMoleculeCopy(newpositions, molecule.labels, molecule.ads, phi=molecule.phi, psi=molecule.psi, slabatom=slabatom , dist=str(dist)))
'''



## Obtain an array of configurations --------------------------
def obtainconfigurations(system, molecule, slab):
    type = [('number', 'i4'), ('label', 'S2'), ('x', 'f'), ('y', 'f'), ('z', 'f'), ('flag', 'i4')]
    configurations     = []
    output             = []
    # no cofigurations at all
    index = 0
    for atom in molecule.positions[molecule.ads]:
        configurations.append(lineup(system, molecule, atom, index))
        index = index + 1
    # + one configuration per adsorbed atom

    linedup = np.copy(configurations)
    configurations = []
    for conf in linedup:
        for angle in system.angrot:
            angle = angle*2*math.pi/360
            configurations.append(rotate_about_z(system, conf, angle))
    # + one config. per adsorbed atom and rotational angle about z

    rotated = np.copy(configurations)
    configurations = []
    for conf in rotated:
        for angle in system.angads:
            angle = angle*2*math.pi/360
            configurations.append(rotate_about_x(system, conf, angle))
    # + one config. per ads. atom, rot. about z and rot. angle about x

    for conf in configurations:
        for atom in slab.positions[np.where(slab.positions['flag'] == 1)]:
            for d in system.dist:
                output.append(translate(conf, atom, system.axis, d))
    # place each conf on top of each atom on surface
    
    for conf in configurations:
        bridge_atoms = slab.positions[np.where(slab.positions['flag'] == 2)]
        used_atoms   = []
        for atom1 in bridge_atoms:
            used_atoms.append(atom1)
            for atom2 in bridge_atoms:
                if not atom2 in used_atoms:
                    atom = np.ndarray((1, ),  dtype=type)
                    atom['number'] = (atom1['number']*100 + atom2['number'])
                    atom['label']  = str(atom1['label']) + str(atom2['label'])
                    atom['x']      = (atom1['x'] + atom2['x'])/2
                    atom['y']      = (atom1['y'] + atom2['y'])/2
                    atom['z']      = (atom1['z'] + atom2['z'])/2
                    for d in system.dist:
                        output.append(translate(conf, atom[0], system.axis, d))
    # place each conf on top of each bridge side
    
    for conf in configurations:
        hollow_atoms = slab.positions[np.where(slab.positions['flag'] == 3)]
        used_atoms   = []
        for atom1 in hollow_atoms:
            used_atoms.append(atom1)
            for atom2 in hollow_atoms:
                if not atom2 in used_atoms:
                    used_atoms.append(atom2)
                    for atom3 in hollow_atoms:
                        if not atom3 in used_atoms:
                            atom = np.ndarray((1, ),  dtype=type)
                            atom['number'] = (atom1['number']*10000 + atom2['number']*100 + atom3['number'])
                            atom['label']  = '' + atom1['label'] + atom2['label'] + atom3['label']
                            atom['x']      = (atom1['x'] + atom2['x'] + atom3['x'])/3
                            atom['y']      = (atom1['y'] + atom2['y'] + atom3['y'])/3
                            atom['z']      = (atom1['z'] + atom2['z'] + atom3['z'])/3
                            for d in system.dist:
                                output.append(translate(conf, atom[0], system.axis, d))
    # place each conf on top of each hollow side
    
    '''
    for conf in configurations:
        for atom in slab.positions[slab.ads]:
          for d in system.dist:
             index_atom = np.where(atom==slab.positions)[0][0]
             label_atom = slab.labels[index_atom]
             slabatom   = str(label_atom) + str(index_atom + 1)
             output.append(translate(conf, atom, system.axis, d, slabatom))
    '''
    return(output)

## Filter out configurations -------------------------------------
def filterconfigurations(configurations, slab, rule):
   minvalue = rule[2]
   label_mol = rule[0]
   label_slab = rule[1]
   slab = slab.positions[np.where(slab.positions['label'] == label_slab)]
   filteredconfs = []
   for conf in configurations:
      nottoclose = True
      molecule = conf.positions[np.where(conf.labels==label_mol)]
      for atom_m in molecule:
         for atom_s in slab:
            atom_s = np.array([atom_s['x'], atom_s['y'], atom_s['z']])
            if getdist(atom_m, atom_s) < minvalue:
               print "Molecule to close: " + label_mol + " " + label_slab + " " + str(getdist(atom_m, atom_s))
               nottoclose = False
      if nottoclose:
         filteredconfs.append(conf)
   return(filteredconfs)
