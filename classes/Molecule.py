#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 29.06.2015
# 
# Classes for molecules
#### ------------------------------------------ ####


import numpy as np

# wofuer war das nochmal????
# warnings.simplefilter("ignore")

class MyMolecule:
      # class for the molecule, folowing data is stored here:
      ## positions = array [Atom label, x, y, z, (0/1 adsorbed?)]
      ## axis      = 1,2,3 integer (in which direction ist the vaccum)
      ## ads       = index array with atoms which are adsorbed on the surface
      ## center    = array [x, y, z] of the center 
   def __init__(self, source):

         self.positions = np.genfromtxt(source, usecols=(1,2,3))
         if np.shape(self.positions) == (3,):
            self.positions = self.positions.reshape(-1,3)

         self.labels    = np.genfromtxt(source, usecols=(0), dtype="string")
         if np.shape(self.labels) == ():
            self.labels = self.labels.reshape(-1,)

         self.ads       = self.makeadsmask(source)
         if np.where(self.ads == True)[0].size == 0:
            self.ads    = np.ones(len(self.positions)).astype(bool)

         self.center       = self.getcenter()

         self.orientations = self.getorientations()

         print '''
------------------------------------------------------
         '''
         print "Creating Molecule from: " + str(source)
         if len(self.positions) == len(self.labels):
            for n in np.arange(len(self.positions)):
               if self.ads[n]:
                  a = "adsorb"
               else:
                  a = ""
               print str(self.labels[n]) + " " + str(self.positions[n]) + " " + a
         print '''
------------------------------------------------------
         '''

   def makeadsmask(self, source):   

      mask = np.array([], dtype=bool)
      for i in np.arange(len(self.positions)):

         value = np.genfromtxt(
                    source, usecols=(4), invalid_raise=False,
                    skip_header=i, skip_footer=len(self.positions)-1-i)

         if value.size == 0:
               mask = np.append(mask, False)
         else:
               mask = np.append(mask, value)
      mask = mask.astype(bool)
      return(mask)

   def getcenter(self):
      if np.shape(self.positions) == (3,):
         return(self.positions)
       # just the center of the molecule
      center            = np.array([
                             (self.positions[:,0].max()+self.positions[:,0].min())/2,
                             (self.positions[:,1].max()+self.positions[:,1].min())/2,
                             (self.positions[:,2].max()+self.positions[:,2].min())/2])
      return(center)

   def getorientations(self):
       # an array of vectors between center of molecule and adsorbed atoms
      atoms             = self.positions[self.ads]
      return([self.center-x for x in atoms])

# --------------------------------------------------------------------------------------------
class MyMoleculeCopy:
      # this class is for the molecule copies which should be created
   def __init__(self, positions, labels, ads, phi=None, psi=None, slabatom=None, dist=None):
      self.positions = positions
      
      self.labels    = labels

      self.ads       = ads

      self.phi       = phi
      self.psi       = psi
      self.slabatom  = slabatom
      self.dist      = dist
