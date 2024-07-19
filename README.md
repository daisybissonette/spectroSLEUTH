
![spectroSLEUTH_logo_final](https://github.com/user-attachments/assets/043fbead-d89d-4661-bcea-733a9bfd7cc5)



A 2024 CodeAstro Workshop Project (Group #2)

[![License: MIT](https://cdn.prod.website-files.com/5e0f1144930a8bc8aace526c/65dd9eb5aaca434fac4f1c34_License-MIT-blue.svg)](/LICENSE) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12760739.svg)](https://doi.org/10.5281/zenodo.12760739)

This package is designed to detect emission-lines in user input spectra and make a best guess at classifying the nature of each emission-line. 
It is currently built for optical spectra (SDSS specifically).

Start by installing the package and running the following:

```
from spectroSLEUTH import sleuth

el = sleuth.emission_lines('path/test_spectrum.fits', redshift)
results_table_detection, fig_detection = el.line_detection()
results_table_identification, fig_identification = el.line_identification()
```

Additional features: 
- The threshold for emission line detection can be adjusted via `prominence`. This is based on the scipy.find_peaks function, see their documentation for further detail: [scipy.find_peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html). The default value for `prominence` is set to 23; lower values will find more peaks, greater values will seek only the most pronounced emission-lines.

Example:
```
el = sleuth.emission_lines('path/test_spectrum.fits', redshift, prominence = value)
```
- Output figures and tables can be saved by adding the following line of code to your script:  

```
plt.savefig('figure.png', bbox_inches ="tight", pad_inches = 0.05, dpi=300)
ascii.write(results_table, 'results.dat', overwrite=True)
```

The optical line list was obtained from http://astronomy.nmsu.edu/drewski/tableofemissionlines.html.

Contributors: Daisy Bisonette, Giulia Cinquegrana, Catalina Zamora, Léa Feuillet 

