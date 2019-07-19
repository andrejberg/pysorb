#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 29.06.2015
#
# Class to read a dump files
#### ------------------------------------------ ####


import numpy as np



class QEoutDump:

    def __init__(self, source):
        self.content = source

    # def getprefix(self):
    #     hit = 'PREFIX'
    #     output = [line.split()[1] for line in self.content if hit in line]
    #     return (output[0])
    #
    # def getmatom(self):
    #     hit = 'MATM'
    #     output = [line.split()[1] for line in self.content if hit in line]
    #     return (output[0])
    #
    # def getsatom(self):
    #     hit = 'SATM'
    #     output = [line.split()[1] for line in self.content if hit in line]
    #     return (output[0])
    #
    # def getdist(self):
    #     hit = 'DIST'
    #     output = [float(line.split()[1]) for line in self.content if hit in line]
    #     return (output[0])
    #
    # def getphi(self):
    #     hit = 'PHI_IN'
    #     output = [int(line.split()[1]) for line in self.content if hit in line]
    #     return (output[0])
    #
    # def getpsi(self):
    #     hit = 'PSI_IN'
    #     output = [int(line.split()[1]) for line in self.content if hit in line]
    #     return (output[0])

    def getenergy(self):
        hit = 'EADS'
        output = [float(line.split()[1]) for line in self.content if hit in line]
        return (output[0])

    def getatompositions(self):
        hit = 'ATOM'
        output = [line.split()[2:5] for line in self.content if hit in line]
        output = [[float(i) for i in set] for set in output]
        output = np.asarray(output)
        return (output)

    def getlabels(self):
        hit = 'ATOM'
        output = [line.split()[1] for line in self.content if hit in line]
        return (output)

    def getcell(self):
        hit = 'CELL'
        output = [line.split()[1:7] for line in self.content if hit in line]
        output = [float(i) for i in output[0]]
        return (output)

    # def getadsorbedatom(self):
    #     hit = 'ADSORBED'
    #     output = [line.split()[1] for line in self.content if hit in line]
    #     return (output[0])
    #
    # # added 24.01.17
    # def getoxygendistance(self):
    #     hit = 'D_OXY'
    #     output = [float(line.split()[1]) for line in self.content if hit in line]
    #     return (output[0])
    #
    # def getphireal(self):
    #     hit = 'PHI_REAL'
    #     output = [float(line.split()[1]) for line in self.content if hit in line]
    #     return (output[0])
    #
    # def getpsireal(self):
    #     hit = 'PSI_REAL'
    #     output = [float(line.split()[1]) for line in self.content if hit in line]
    #     return (output[0])