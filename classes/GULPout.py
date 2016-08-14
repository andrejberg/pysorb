#! /usr/bin/python

#### ------------------------------------------ ####
# last edit: 18.01.2016
# 
# Class to read a GULP file after fitting
#### ------------------------------------------ ####

import numpy as np

class GULPout:
    
    def __init__(self, source):
        f = file(source, 'r')
        self.content = f.readlines()
        f.close()

        e_qe               = []
        e_initial          = []
        e_final            = []
        self.rawpot_init   = []
        self.rawpot_final  = []
    
        read_energy     = False
        fit_complete    = False
        read_potentials = False
    
        for line in self.content:
            if "Comparison of initial and final observables :" in line:
                read_energy = True
            if "Maximum range for interatomic potentials" in line:
                read_energy = False
            if "Fit completed successfully" in line:
                fit_complete = True
            
            if "General interatomic potentials" in line:
                read_potentials = True
            if "Number of variables" in line or "Total time to end of fitting" in line:
                read_potentials = False
    
            if read_energy and "Energy" in line:
                e_qe.append(float(line.split()[2]))
                e_initial.append(float(line.split()[3]))
                e_final.append(float(line.split()[4]))
            if not fit_complete and read_potentials:
                self.rawpot_init.append(line)
            if fit_complete and read_potentials:
                self.rawpot_final.append(line)
        
        self.e_qe      = np.asarray(e_qe)
        self.e_init    = np.asarray(e_initial)
        self.e_fin     = np.asarray(e_final)
        self.pot_init  = self.format_potentials(self.rawpot_init)
        self.pot_final = self.format_potentials(self.rawpot_final)
        
    def format_potentials(self, rawpot):
        rawpot     = rawpot[6:-3]
        potentials = []
        for line in rawpot:
            if "Lenn/es" in line:
                p = { "type1"   : line.split()[0], 
                      "type2"   : line.split()[2],
                      "pot"     : line.split()[4], 
                      "ptype"   : line.split()[5] + "_" + line.split()[6], 
                      "epsilon" : float(line.split()[7]), 
                      "sigma"   : float(line.split()[8]), 
                      "cutoff"  : float(line.split()[12])}
                potentials.append(p)
        return potentials
