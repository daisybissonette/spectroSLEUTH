import os
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
from astropy.io import fits, ascii
from scipy.signal import find_peaks
from astropy.table import Table

class emission_lines(): 
    """
    Class containing functions to detect and identify emission lines

    Args:
        filepath (string): filepath to the spectrum data (fits format)
        z (float): redshift of the galaxy. 
        prominence (float, optional): required prominence of peaks for emission-line detection threshold. default is 20.
    """
    
    def __init__(self, filepath, z, prominence=20):

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
        plt.plot(new_table["emit lam"], new_table["flux"], c='cornflowerblue', linewidth=0.8)
        plt.plot(new_table["emit lam"][peaks], new_table["flux"][peaks], 'x', c='black')
        plt.xlabel(r'Wavelength ($\AA$)')
        plt.ylabel('Flux')
        plt.title('Potential emission lines found in spectrum')

        #plt.show()
            
        return results_table, fig

    def line_identification(self): 
        """
        Line Identification 

        This function take in identified peaks (redshifted back to rest) and compares them to a table of atomic wavelengths to identify ion

        Args:
            variables defined in class declaration
        
        Returns:
            results_table (astropy table): Table containing the observed and emitted wavelengths of detected emission lines, as well as the best guess for the corresponding ions responsible for the line.
            fig (figure): Figure showing the spectrum with detected emission-lines indicated by a vertical line and labeled ion.
        """

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
                matches.append([lam, lam+min(hold), defined_names[i]])
        
        matches_df = pd.DataFrame(matches,columns=['Atomic Wavelength', 'Found Peak', 'Ion Match'])
      
        #plotting code

        # Determine the min and max of the wavelength range
        min_wl = np.min(self.lam) / (1 + self.redshift)
        max_wl = np.max(self.lam) / (1 + self.redshift)

        # Calculate the number of subplots needed
        num_subplots = int(np.ceil((max_wl - min_wl) / 2000))

        fig, axes = plt.subplots(num_subplots, 1, figsize=(15, 5 * num_subplots), sharey=True)
        if num_subplots == 1:
            axes = [axes]  # Make sure axes is iterable if there's only one subplot

        for i in range(num_subplots):
            ax = axes[i]
            start_wl = min_wl + i * 2000
            end_wl = min(start_wl + 2000, max_wl)

            # Plot the flux in the current range
            mask = (self.lam / (1 + self.redshift) >= start_wl) & (self.lam / (1 + self.redshift) < end_wl)
            ax.plot(self.lam[mask] / (1 + self.redshift), self.flux[mask], c='cornflowerblue')

            # Plot the vertical lines for 'Found Peak' and determine the new end_wl
            found_peaks_in_range = []
            for wl in np.array(matches_df['Found Peak']):
                if start_wl <= wl < end_wl:
                    ax.vlines(wl, 0, np.max(self.flux[mask]), color='gray', ls='--')
                    found_peaks_in_range.append(wl)

            if found_peaks_in_range:
                end_wl = min(max(found_peaks_in_range) + 100, max_wl)

            # Annotate the labels with staggered y positions
            labels = np.array(matches_df['Ion Match'])
            labelx = np.array(matches_df['Atomic Wavelength'])
            labely = np.array(results_table['flux'])
            avgflux = (min(labely)+max(labely))/2
            staggered_y = np.array([0.8*avgflux if j % 2 == 0 else 0.8*avgflux+(0.1*avgflux) for j in range(len(labels))])

            for j, label in enumerate(labels):
                if start_wl <= labelx[j] < end_wl:
                    ax.annotate(
                        label,
                        (labelx[j], staggered_y[j % len(staggered_y)]),
                        xytext=(25, 25),
                        textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', edgecolor='indigo', facecolor='thistle'),
                        arrowprops=dict(arrowstyle='->', color='indigo')
                    )
            ax.set_xlim(start_wl, end_wl)
            ax.set_xlabel(r'Wavelength ($\AA$)')
            if i == 0:
                ax.set_ylabel('Flux')
            ax.set_title(f'Wavelength Range: {int(start_wl)} - {int(end_wl)} $\AA$')

        plt.tight_layout()
        plt.show()

        return matches_df, fig
    

