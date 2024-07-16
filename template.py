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
        data.byteswap().newbyteorder()
        self.lam = np.array(10**data['loglam'])
        self.flux = np.array(data['flux'])
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
        corrected_lam = self.lam/(1+self.redshift)
        # putting the spectrum data into a pandas dataframe
        df = {'obs lam': self.lam, 'emit lam': corrected_lam, 'flux': self.flux}
        pdtable = pd.DataFrame(df)

        #defining a noise range and getting the noise value
        noise_range = pdtable.loc[(pdtable['emit lam'] > 7000) & (pdtable['emit lam'] < 8000), 'emit lam']
        flux_noise = pdtable.loc[noise_range.index[0]: noise_range.index[-1], 'flux']
        flux_noise_std = np.std(flux_noise)

        #line detection 

        #plotting the spectrum with the lines detected
        fig = plt.figure()
        plt.plot(pdtable["emit lam"], pdtable["flux"])
        plt.xlabel("wavelength in Angstrom")
        plt.ylabel("flux")
        return pdtable, fig
    '''
    def line_identification(self, ): 
        #line identification

        return Table
        '''

el = emission_lines('spec-0285-51930-0309.fits', 0.06456, 3)
table, figure = el.line_detection()
#print(table)
plt.show()
