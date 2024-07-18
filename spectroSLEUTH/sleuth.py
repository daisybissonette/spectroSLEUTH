import os
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
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

    def line_detection(self): #, savefig=False, savetable=False
        """
        Line Detection 

        This function will detect peaks by using the scipy find_peak function.

        Args:
            variables defined in class declaration
        
        Returns: 
            results_table (astropy table): Table containing the observed and emitted wavelengths of detected emission lines.
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

        #plt.show()
            
        return results_table, fig

    def line_identification(self): 
        '''
        Line Identification 

        This function take in identified peaks (redshifted back to rest) and compares them to a table of atomic wavelengths to identify ion

        Args:
            variables defined in class declaration
        
        Returns:
            results_table (astropy table): Table containing the observed and emitted wavelengths of detected emission lines, as well as the best guess for the corresponding ions responsible for the line.
            fig (figure): Figure showing the spectrum with detected emission-lines indicated by a vertical line and labeled ion.
        '''

        #calls first function and saves output to use identified peaks in this function
        results_table, fig = self.line_detection()

        ion_filepath = os.path.join(os.path.dirname(__file__), 'line_data', 'defined_optical_lines.csv')
        defined_lines = pd.read_csv(ion_filepath)
        defined_wavelength = np.array(defined_lines['wavelength'])
        defined_names = defined_lines['ion']
        matches = []

        for i, lam in enumerate(defined_wavelength):
            
            #the difference between the vacuum wavelength and the peaks gets saved
            hold = np.abs(lam - np.array(results_table['emit lam']))
            
            #if there is a value in this array that is less than a desired tolerance it's probably a match. so its saved
            if min(hold) < 5:
                matches.append([lam, lam-min(hold), defined_names[i]])
        
        matches_df = pd.DataFrame(matches,columns=['Atomic Wavelength', 'Found Peak', 'Ion Match'])
      
        #plotting code
        fig = plt.figure()
        
        plt.plot(self.lam/(1+self.redshift), self.flux)
        for i, wl in enumerate(np.array(matches_df['Found Peak'])):
            plt.vlines(wl, 0, np.max(self.flux), color = 'gray', ls = '--')
        plt.xlabel(r'Wavelength ($\AA$)')
        plt.ylabel('Flux')
        plt.title('')

        labels = np.array(matches_df['Ion Match'])[0]
        labelx = np.array(matches_df['Atomic Wavelength'])[0]
        labely = np.array(results_table['flux'])[0]
        
        for i, label in enumerate(labels):
            ax.annotate(labels[i], (labelx[i], labely[i]))

        plt.show()


        return matches_df, fig

