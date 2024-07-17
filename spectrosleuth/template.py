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

        #plt.show()
            
        return results_table, fig

    def line_identification(self, results_table): 
        defined_lines = pd.read_csv('defined_optical_lines.csv')
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

        # plt.text(np.array(matches_df['Atomic Wavelength'])[0], np.array(results_table['flux'])[0], 
        #          np.array(matches_df['Ion Match'])[0])

        print(np.array(matches_df['Ion Match'])[0])

        # for i, name in enumerate(np.array(matches_df['Ion Match'])):
        #     plt.text(np.array(matches_df['Atomic Wavelength'])[i], np.array(results_table['flux'])[i], name)
        
        plt.show()


        return matches_df, fig
el = emission_lines('spec-0285-51930-0309.fits', 0.06456) #0.06456
el_table, figure = el.line_detection()
test = el.line_identification(el_table)
print(test)

# filepath = input("Enter FITS filepath: ")
# z = input("Enter redshift: ")

# prom_check = input("Do you want to set prominance (Y or N)? ")
# if prom_check in ['Y', 'y', 'Yes', 'yes']: # make not case sensitive.
#     prom_userset = input("What value for prominence (Must be > 0)? ")
#     el = emission_lines(filepath, float(z), prominence=float(prom_userset))
# elif prom_check in ['N', 'n', 'No', 'no']:
#     el = emission_lines(filepath, float(z))
# else:
#     raise Exception("Must be Y or N. Try again.")

# #el = emission_lines('spec-0285-51930-0309.fits', 0.2) #0.06456
# el_table, figure = el.line_detection() #

# savefig = input("Do you want to save the figure (Y or N)? ")

# if savefig in ['Y', 'y', 'Yes', 'yes']:
#     plt.savefig("emission_lines_detected.png", bbox_inches ="tight", pad_inches = 0.05, dpi=300)

# savetable = input("Do you want to save the table (Y or N)? ")

# if savetable in ['Y', 'y', 'Yes', 'yes']:
#     ascii.write(el_table, 'emission_lines_table.dat', overwrite=True)

# print('Here is a table of your emission lines!')
# print(el_table)

# plt.show()
