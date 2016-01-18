#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 03.04.15
# 
# Class for Surface
#### ------------------------------------------ ####


import numpy as np
#import lib.convert
#from lib.helper import center

# wofuer war das nochmal????
# warnings.simplefilter("ignore")
'''
class MySlab:
      # class for the surface, folowing data is stored here:
      ## positions = array with [Atom label, x, y, z, (0/1 adsorbed?)]
      ## axis      = 1,2,3 integer (in which direction is the vacuum)
      ## ads       = index array with atoms on which the molecule is adsorbed 
   def __init__(self, source, system):

         self.positions = np.genfromtxt(source, usecols=(1,2,3))
         if np.shape(self.positions) == (3,):
            self.positions = self.positions.reshape(-1,3)
         if system.alat != 0:
            self.positions = self.positions*system.alat*convert.bohr2ang(1)

         self.labels    = np.genfromtxt(source, usecols=(0), dtype="string")
         if np.shape(self.labels) == ():
            self.labels = self.labels.reshape(-1,)

         self.ads       = self.makeadsmask(source)
         if np.where(self.ads == True)[0].size == 0:
            self.ads    = self.makeadsmaskauto(system)
        
         # self.ads_positions = #array mit den positions auf denen adsorbiert wird

         print '''
#------------------------------------------------------
'''
         print "Creating Slab from: " + str(source)

         if len(self.positions) == len(self.labels):
            for n in np.arange(len(self.positions)):
               if self.ads[n]:
                  a = "adsorb"
               else:
                  a = ""
               print str(self.labels[n]) + " " + str(self.positions[n]) + " " + a
         print '''
#------------------------------------------------------
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
      
   def get_ads_positions(self,  source):
       top    = False
       bridge = False
       hollow = False
       for i in np.arange(len(self.positions)):
           line = np.genfromtxt(source, skip_header=i, skip_footer=len(self.positions)-1-i)
           if int(value) == 1 and len(line) == 4:
               top = True
           elif int(value) == 2 and len(line) == 4:
               bridge = True
           elif int(value) == 3 and len(line) == 4:
               hollow = True
               
       positions = []
       if top:
           for i in np.arange(len(self.positions)):
               line = np.genfromtxt(source, skip_header=i, skip_footer=len(self.positions)-1-i)
               if int(value) == 1 and len(line) == 4:
                  positions.append([line[1], line[2], line[3]])
       if bridge:
           p = []
           for i in np.arange(len(self.positions)):
               line = np.genfromtxt(source, skip_header=i, skip_footer=len(self.positions)-1-i)
               if int(value) == 2 and len(line) == 4:
                   p.append([line[1], line[2], line[3]])
           positions.append(center(p[0], p[1]))

   def makeadsmaskauto(self, system):

      mask = np.zeros(len(self.positions)).astype(bool)
      full = np.argsort(self.positions[:,system.axis-1])
      surf = np.sort(full)[-10:]
      for n in surf:
         i = 0
         for m in full:
            if n == m:
               mask[i] = True
               i = i+1
            else:
               i = i+1
      return(mask)
      
'''
class MySlab:
    def __init__(self, source):
        lenth = np.genfromtxt(source, usecols=(0), dtype="string").size
            
        self.positions = self.get_positions(lenth,  source)
        
    def get_positions(self, lenth, source):
        type = [('number', 'i4'), ('label', 'S2'), ('x', 'f'), ('y', 'f'), ('z', 'f'), ('flag', 'i4')]
        positions = np.ndarray((lenth, ),  dtype=type)
        for i in np.arange(lenth):
            line = np.genfromtxt(source, dtype=None, skip_header=i, skip_footer=lenth-1-i)
            line = line.reshape(1, )[0]
            positions['number'][i] = i + 1
            positions['label'][i] = line[0]
            positions['x'][i] = line[1]
            positions['y'][i] = line[2]
            positions['z'][i] = line[3]
            if len(line) == 5:
                positions['flag'][i] = line[4]
            else:
                positions['flag'][i] = 0
        return positions
'''
    def get_ads_positions(self):
        if np.where(self.positions['flag'] == 2)[0].size == 2:
            ads_bridge = 1
        else:
            ads_bridge = 0
        if np.where(self.positions['flag'] == 3)[0].size == 3:
            ads_hollow = 1
        else:
            ads_hollow = 0
        lenth = np.where(self.positions['flag'] == 1)[0].size + ads_bridge + ads_hollow
        type = [('number', 'i4'), ('label', 'S2'), ('x', 'f'), ('y', 'f'), ('z', 'f'), ('flag', 'i4')]
        ads_positions = np.ndarray((lenth, ),  dtype=type)
        for i in np.where(self.positions['flag'] == 1)[0]:
            
'''














