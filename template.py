import numpy as np 
import scipy 
import matplotlib.pyplot as plt 
import pandas as pd 
from astropy import coordinates as coords
from astroquery.sdss import SDSS
from astropy.io import fits

class emission_lines(): 
    
    def __init__(self, filepath, z, snr):          
        hdul = fits.open(filepath)
        data = hdul[1].data
        self.lamb = 10**data['loglam']
        self.flux = data['flux']
        self.redshift = z
        self.snr = snr

    def func1(self, ): 
        """
        inse
        """
        #line detection 

        return Table
    
    def func2(self, ): 
        #line identification

        return Table