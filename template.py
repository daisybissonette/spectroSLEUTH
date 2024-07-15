import numpy as np 
import scipy 
import matplotlib.pyplot as plt 
import pandas as pd 
from astropy import coordinates as coords
from astropy.io import fits

class emission_lines(): 
    
    def __init__(self, filepath, z, snr):
        '''
        filepath (string): filepath to the spectrum data (fits format)
        z (float): redshift of the galaxy 
        snr (float): signal-to-noise ratio desired for emission-line detection threshold
        '''          
        hdul = fits.open(filepath)
        data = hdul[1].data
        self.lamb = 10**data['loglam']
        self.flux = data['flux']
        self.redshift = z
        self.snr = snr

    def line_detection(self): 
        """
        This function will detect peaks by....
        INPUTS:
        variables defined above
        OUTPUTS: 
        1. Pandas dataframe containing the observed and emitted wavelengths of detected emission lines.
        2. Figure showing the spectrum with detected emission-lines indicated by a vertical line.
        """
        #redshift correct the wavelengths to define consistant noise range
        corrected_lam = self.lamb/(1+self.redshift)
        # putting the spectrum data into a pandas dataframe
        df = {'obs lam': lam, 'emit lam': corrected_lam, 'flux': data['flux']}
        pdtable = pd.DataFrame(df)

        #defining a noise range and getting the noise value
        noise_range = pdtable.loc[(pdtable['emit lam'] > 7000) & (pdtable['emit lam'] < 8000), 'emit lam']
        flux_noise = pdtable.loc[noise_range.index[0]: noise_range.index[-1], 'flux']
        flux_noise_std = np.std(flux_noise)

        #line detection 

        return pdtable
    
    def line_identification(self, ): 
        #line identification

        return Table