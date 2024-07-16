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
        new_table = Table.from_pandas(pdtable)
        #defining a noise range and getting the noise value
        #noise_range = new_table.loc[(new_table['emit lam'] > 7000) & (new_table['emit lam'] < 8000), 'emit lam']
        #flux_noise = new_table.loc[noise_range.index[0]: noise_range.index[-1], 'flux']
        #flux_noise_std = np.std(flux_noise)

        #plotting the spectrum with the lines detected
        peaks, props = find_peaks(new_table["flux"], prominence=23) #mess with arguments to get better peak finding, normalize spectra first
        #new_table['peak_lam'] = new_table["emit lam"][peaks]
        results = [new_table["obs lam"][peaks], new_table["emit lam"][peaks], new_table["flux"][peaks]]
        results_table = Table(results)

        fig = plt.figure()
        plt.plot(new_table["emit lam"], new_table["flux"])
        plt.plot(new_table["emit lam"][peaks], new_table["flux"][peaks], 'x')
        plt.xlabel('Wavelength')
        plt.ylabel('Flux')
        plt.show()

        return results_table, fig
    '''
    def line_identification(self, ): 
        #line identification

        return Table
        '''

el = emission_lines('spec-0285-51930-0309.fits', 0.06456, 3)
el_table, figure = el.line_detection()
print(el_table)
plt.show()