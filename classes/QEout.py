#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 29.06.2015
# 
# Class to read a QE outputfile
#### ------------------------------------------ ####

import numpy as np
import math
import lib.convert as convert
from lib.helper import distance


class QEout:

    def __init__(self, source, name):
      self.prefix = name.split(".")[0]
      self.matom = name.split(".")[1]
      self.satom = name.split(".")[2]
      self.dist = name.split(".")[4] + "." + name.split(".")[5]
      self.phi = name.split(".")[7]
      self.psi = name.split(".")[9]
      f = file(source, 'r')
      self.content = f.readlines()
      f.close()

    def getenergy(self):
      hit = '!'
      output = [float(line.split()[4]) for line in self.content if hit in line]
      return(output[-1])

# 24.01.17 angepasst damit positionen aus relax runs auch richtig gelesen werden
    def getatompositions(self):
        if 'Begin final coordinates' in "".join(self.content):
            start = "Begin final coordinates"
            end = "End final coordinates"
            output = []
            parse = False
            for line in self.content:
                if start in line:
                    parse = True
                    continue
                if end in line:
                    break
                if parse and len(line.split()) == 4 or parse and len(line.split()) == 7:
                    output = output + [ line.split()[1:4] ]
            output = [[float(i) for i in set] for set in output]
            output = np.asarray(output)
        else:
            hit = 'tau('
            output = [line.split()[6:9] for line in self.content if hit in line]
            output = [[float(i) for i in set] for set in output]
            output = np.asarray(output)*self.getalat()*convert.bohr2ang(1)
        return(output)

    def getlabels(self):
      hit = 'tau('
      output = [line.split()[1] for line in self.content if hit in line]
      return(output)
    
    def getalat(self):
      hit = 'lattice parameter (alat)  ='
      output = [float(line.split()[4]) for line in self.content if hit in line]
      return(output[0])
    
    def getcell(self):
      hit1 = 'a(1) = ('
      hit2 = 'a(2) = ('
      hit3 = 'a(3) = ('
      output = [line.split()[3:6] for line in self.content if hit1 in line or hit2 in line or hit3 in line]
      output = [[float(i) for i in set] for set in output]
      output = np.asarray(output)
      return(output)
    
    def makecellparams(self):
      cell = self.getcell()*self.getalat()*convert.bohr2ang(1)
      a = cell[0,0]
      b = math.sqrt(math.pow(cell[1,0], 2) + math.pow(cell[1,1], 2))
      c = math.sqrt((math.pow(cell[2,0], 2) + math.pow(cell[2,1], 2) + math.pow(cell[2,2], 2)))
      alpha = math.degrees(math.acos(cell[2,1]/c))
      beta = math.degrees(math.acos(cell[2,0]/b))
      gamma = math.degrees(math.acos(cell[1,0]/b))
      cellparams = np.array([a,b,c,alpha,beta,gamma])
      return cellparams
    
    def getadsorbedatom(self):
        distances = []
        labels = self.getlabels()
        atoms  = self.getatompositions()
        for m in range(len(labels)):
            if labels[m] != "Au":
                matom = atoms[m,:]
                for n in range(len(labels)):
                    if labels[n] == "Au":
                        atom = atoms[n,:]
                        distances.append((labels[m], distance(matom,  atom)))
        mindist = min(distances, key=lambda t: t[1])
        return mindist
    
    # added to calculate min dinstance between Au and O
    def getadsorbeddistance(self):
        distances = []
        labels = self.getlabels()
        atoms  = self.getatompositions()
        for m in range(len(labels)):
            if labels[m] == "O":
                matom = atoms[m,:]
                for n in range(len(labels)):
                    if labels[n] == "Au":
                        atom = atoms[n,:]
                        distances.append((labels[m], distance(matom,  atom)))
        mindist = min(distances, key=lambda t: t[1])
        return mindist

class QEoutDump:

   def __init__(self, source):
      self.content = source

   def getprefix(self):
      hit = 'PREFIX'
      output = [line.split()[1] for line in self.content if hit in line]
      return(output[0])

   def getmatom(self):
      hit = 'MATM'
      output = [line.split()[1] for line in self.content if hit in line]
      return(output[0])

   def getsatom(self):
      hit = 'SATM'
      output = [line.split()[1] for line in self.content if hit in line]
      return(output[0])

   def getdist(self):
      hit = 'DIST'
      output = [float(line.split()[1]) for line in self.content if hit in line]
      return(output[0])

   def getphi(self):
      hit = 'PHI_IN'
      output = [int(line.split()[1]) for line in self.content if hit in line]
      return(output[0])

   def getpsi(self):
      hit = 'PSI_IN'
      output = [int(line.split()[1]) for line in self.content if hit in line]
      return(output[0])

   def getenergy(self):
      hit = 'EADS'
      output = [float(line.split()[1]) for line in self.content if hit in line]
      return(output[0])

   def getatompositions(self):
      hit = 'ATOM'
      output = [line.split()[2:5] for line in self.content if hit in line]
      output = [[float(i) for i in set] for set in output]
      output = np.asarray(output)
      return(output)

   def getlabels(self):
      hit = 'ATOM'
      output = [line.split()[1] for line in self.content if hit in line]
      return(output)

   def getcell(self):
      hit = 'CELL'
      output = [line.split()[1:7] for line in self.content if hit in line]
      output = [float(i) for i in output[0]]
      return(output)

   def getadsorbedatom(self):
      hit = 'ADSORBED'
      output = [line.split()[1] for line in self.content if hit in line]
      return(output[0])
    # added 24.01.17
   def getoxygendistance(self):
      hit = 'D_OXY'
      output = [float(line.split()[1]) for line in self.content if hit in line]
      return(output[0])

   def getphireal(self):
      hit = 'PHI_REAL'
      output = [float(line.split()[1]) for line in self.content if hit in line]
      return(output[0])

   def getpsireal(self):
      hit = 'PSI_REAL'
      output = [float(line.split()[1]) for line in self.content if hit in line]
      return(output[0])

