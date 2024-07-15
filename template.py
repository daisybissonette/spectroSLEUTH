import numpy as np 
import scipy 
import matplotlib.pyplot as plt 
import pandas as pd 
from astropy import coordinates as coords
from astroquery.sdss import SDSS
from astropy.io import fits

class emission_lines(): 
    
    def __init__(self, filepath, z, snr):          
        co = coords.SkyCoord(filepath) #position format example: '0h8m05.63s +14d50m23.3s'
        self.spectrum = SDSS.get_spectra(coordinates=co) #import sdss data
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