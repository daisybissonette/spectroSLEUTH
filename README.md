
![spectroSLEUTH_purple_logo](https://github.com/user-attachments/assets/2b5e7939-6a6c-4d91-b90d-7fc4cf19fa38)

SpectroSLEUTH: SpectroScopy Line Emission Utility and Tracking Helper

A 2024 CodeAstro Workshop Project (Group #2)

add badges here 

This package is desined to detect emission-lines in user input spectra, as well as making best guesses as to the nature of these emission-lines. 
It is currently built for optical spectra (SDSS specifically).

Start by installing the package and running the following:

```
from spectroSLEUTH import sleuth

el = sleuth.emission_lines('path/test_spectrum.fits', redshift)
results_table_detection, fig_detection = el.line_detection()
results_table_identification, fig_identification = el.line_identification()
```

For additional features, you can set the threshold for detecting lines by setting a value for prominence (as defined in the [scipy.find_peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) function). The default prominence is set to 23. Lower values for prominence will find more peaks, while a higher value will find only the most pronounced emission-lines.
Example:
```
el = sleuth.emission_lines('path/test_spectrum.fits', redshift, prominence = value)
```
Additional options include being able to save the output table and figure to your machine. These are set to False by default.

```
el = sleuth.emission_lines('path/test_spectrum.fits', redshift, prominence = value, savefig = True, savetable = True)
```

Contributors: Daisy Bisonette, Giulia Cinquegrana, Catalina Zamora, Léa Feuillet 

