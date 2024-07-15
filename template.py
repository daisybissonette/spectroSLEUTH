import numpy as np 
import scipy 
import matplotlib.pyplot as plt 
import pandas as pd 
from astropy import coordinates as coords
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

        return Table
    
    def func2(self, ): 
        #line identification

        return Table