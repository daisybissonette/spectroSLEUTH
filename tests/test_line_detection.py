import numpy as np
import matplotlib.pyplot as plt
from pytest import approx
import spectroSLEUTH
from spectroSLEUTH.sleuth import emission_lines

def test_line_detection(): 
    """
    Test that evaluates the correctess of the emission_lines.line_detection() function. 
    """   

    el = emission_lines('spectroSLEUTH/tests/test_spectrum_1.fits', 0.0646, promience=20)
    el.results_table, el.fig = el.line_detection()
    # assert that emission line at OIII is detection 
    assert el.results_table[7] == '[O III]'

    # assert plotting doesn't fail 
    fig, ax = el.fig()
    assert fig is not None
    assert ax is not None

    pass
