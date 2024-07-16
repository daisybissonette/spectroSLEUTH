import numpy as np 
import scipy 
import matplotlib.pyplot as plt 
import pandas as pd 
from astropy import coordinates as coords
from astropy.io import fits, ascii
from scipy.signal import find_peaks
from astropy.table import Table

class emission_lines(): 
    
    def __init__(self, filepath, z, prominence=20):
        '''
        filepath (string): filepath to the spectrum data (fits format)
        z (float): redshift of the galaxy. 
        prominence (float, optional): required prominence of peaks for emission-line detection threshold. default is 20. 
        savefig (boolean, optional): set to True to save figure. default is False.
        '''  
        if z < 0:
            raise Exception("Redshift cannot be negative. Try again with a positive value.")
        
        if prominence < 0:
            raise Exception("Prominence cannot be negative. Try again with a positive value.")

        #insert type check / type error
        hdul = fits.open(filepath)

        hdul[0].verify('exception') 

        data = hdul[1].data
        self.lam = np.array(10**data['loglam'])
        self.flux = np.array(data['flux'])
        self.redshift = z
        self.prominence = prominence 

    def line_detection(self, savefig=False, savetable=False): 
        """
        This function will detect peaks by....
        INPUTS:
        variables defined in class declaration
        OUTPUTS: 
        results_table (astropy table): Astropy table containing the observed and emitted wavelengths of detected emission lines.
        fig (figure): Figure showing the spectrum with detected emission-lines indicated by a vertical line.
        """
        #redshift correct the wavelengths to define consistant noise range
        corrected_lam = self.lam/(1+self.redshift)
        df = {'obs lam': self.lam, 'emit lam': corrected_lam, 'flux': self.flux}
        pdtable = pd.DataFrame(df)
        new_table = Table.from_pandas(pdtable)

        #plotting the spectrum with the lines detected
        
        peaks, props = find_peaks(new_table["flux"], prominence=self.prominence) 
        results = [new_table["obs lam"][peaks], new_table["emit lam"][peaks], new_table["flux"][peaks]]
        results_table = Table(results)

        fig = plt.figure()
        plt.plot(new_table["emit lam"], new_table["flux"])
        plt.plot(new_table["emit lam"][peaks], new_table["flux"][peaks], 'x')
        plt.xlabel(r'Wavelength ($\AA$)')
        plt.ylabel('Flux')
        plt.title('')
        
        if savefig == True:
            plt.savefig("emission_lines_detected.png", bbox_inches ="tight", pad_inches = 0.05, dpi=300)
        
        if savetable == True:
            ascii.write(results_table, 'emission_lines_table.dat', overwrite=True)

        plt.show()
            
        return results_table, fig
    '''
    def line_identification(self, ): 
        #line identification

        return Table
        '''

el = emission_lines('/Users/leafeuillet/Desktop/heart_rate-2024-07-05.json', 0.2) #0.06456
el_table, figure = el.line_detection(savefig=False, savetable=True)
print('Here is a table of your emission lines!')
print(el_table)
