# vital imports
import matplotlib.pyplot as plt
import numpy as np

class hyti_proc :
    nsamps= 324
    nlines= 256
    
    def __init__(self, ns, nl) :
        self.nsamps = ns 
        self.nlines = nl
        
        
    def extract_and_flatten (self, fname):
        tmparr = np.fromfile(fname, dtype=np.uint16).reshape((self.nbands, self.nlines, self.nsamps))
        flatten = np.mean(tmparr, axis=0)
        return flag
    