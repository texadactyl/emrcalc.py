"""
Electromagnetic Radiation laws:
Frequency f = c / λ
Wavelength λ = c / f
Planck's Energy quanta: E = h * f = h * c / λ

where:
f = frequency in Hertz (Hz = 1/sec)
λ = wavelength in meters (m)
c = the speed of light (299,792,458 m/s)
E = energy in electron Volts (eV)
h = Plank's constant = 6.626068 * 10^-34 (m^2 * kg / s)
"""

from numpy import floor, log10
import scipy.constants as sc

# Factor for converting joules to electron volts
J2EV = 1. / sc.value(u'electron volt-joule relationship')

"""
Float-F formatter, used in float2str()
"""
FFORMATTER = lambda arg_float: "{0:f}".format(arg_float).rstrip("0").rstrip(".")

"""
Table of frequency in Hz and corresponding descriptive text
"""
EMR_TABLE = [
    [30e3, "Radio Very Low Frequency (VLF)"],
    [300e3, "Radio Low Frequency (LF)"],
    [3000e3, "Radio Medium Frequency (MF)"],
    [30e6, "Radio High Frequency (HF)"],
    [300e6, "Radio Very High Frequency (VHF)"],
    [1e9, "Radio Ultra High Frequency (UHF)"],
    [2e9, "Radio NASA Band L"],
    [4e9, "Radio NASA Band S"],
    [8e9, "Radio NASA Band C"],
    [12e9, "Radio NASA Band X"],
    [18e9, "Radio NASA Band Ku"],
    [27e9, "Radio NASA Band K"],
    [40e9, "Radio NASA Band Ka"],
    [75e9, "Radio NASA Band V"],
    [110e9, "Radio NASA Band W"],
    [300e9, "Radio Extremely High Frequency (EHF)"],
    [1.2e14, "Infrared (IR)"],
    [4.0e14, "Near Infrared (NIR)"],
    [450e12, "Visible Red"],
    [508e12, "Visible Orange"],
    [540e12, "Visible Yellow"],
    [597e12, "Visible Green"],
    [610e12, "Visible Cyan"],
    [666e12, "Visible Blue"],
    [689e12, "Visible Indigo"],
    [750e12, "Visible Violet"],
    [3e16, "Ultraviolet (UV)"],
    [1e19, "X-ray"],
    [1e21, "Gamma ray"]
    ]

def angstrom2meters(arg_angstrom):
    """
    Given a wavelength (Angstroms), return the equivalent in meters.
    """
    return arg_angstrom * 1e-10

def dump_pyobject(arg_subject, arg_object):
    """
    Dump a Python object to stdout.
    """
    for attr in dir(arg_object):
        if hasattr(arg_object, attr):
            print("%s.%s = %s" % (arg_subject, attr, getattr(arg_object, attr)))

def wvlen2num(arg_wvlen):
    return 1 / arg_wvlen

def wvnum2len(arg_wvnum):
    return 1 / arg_wvnum

def energy2info(arg_energy):
    """
    Given energy (J),
    return a brief description, frequency (Hz), wavelength (m), wave number (1/m).
    """
    freq = arg_energy / sc.h
    wavelength = sc.c / freq
    wavenum = wvlen2num(wavelength)
    for row_freq, row_desc in EMR_TABLE:
        if freq < row_freq:
            return row_desc, freq, wavelength, wavenum
    return "Cosmic ray", freq, wavelength, wavenum

def float2str(arg_scalar, arg_n):
    '''
    Given a scalar and the # of desired signficant figures requested,
    convert it to a string.
    If the scalar argument cannot be converted to a float, return "-0.0".
    '''
    try:
        scalar = float(arg_scalar)
    except:
        return "0"
    if abs(scalar) == 0.0:
        return "0"
    value = round(scalar, arg_n - int(floor(log10(abs(scalar)))) - 1)
    if 1e-5 <= value <= 1e5:
        return FFORMATTER(value)
    return "{:.5G}".format(value)

def freq2info(arg_freq):
    """
    Given a frequency (Hz),
    return a brief description, energy (J), wavelength (m), wave number(1/m).
    """
    wavelength = sc.c / arg_freq
    wavenum = wvlen2num(wavelength)
    joules = sc.h * arg_freq
    for row_freq, row_desc in EMR_TABLE:
        if arg_freq < row_freq:
            return row_desc, joules, wavelength, wavenum
    return "Gamma", joules, wavelength, wavenum

def wvlen2info(arg_wvlen):
    """
    Given a wavelength (meters),
    return a brief description, energy (J), frequency (Hz), wave number(m).
    """
    wavenum = wvlen2num(arg_wvlen)
    freq = sc.c / arg_wvlen
    joules = sc.h * freq
    for row_freq, row_desc in EMR_TABLE:
        if freq < row_freq:
            return row_desc, joules, freq, wavenum
    return "Cosmic ray", joules, freq, wavenum

def test_nm_to_info(arg_nm):
    """
    Given a wavelength (nm), show brief description, frequency (Hz), energy (eV), wave number(m).
    """
    xdesc, xfreq, xjoules, xwvnum = wvlen2info(arg_nm / 1.0e9)
    print("{} nm --> {}, {:.3e} Hz, {:.3f} J, {:.3f} m^-1".format(arg_nm, xdesc, xfreq, xjoules, xwvnum))

if __name__ == "__main__":
    """
    testing 1-2-3
    """
    # ultraviolet radiation (UV, 100 to 400 nm),
    # visible radiation (light, 400 to 700 nm),
    # and infrared radiation (IR, 700 nm to 1 mm = 10^6 nm)
    test_nm_to_info(200)
    test_nm_to_info(400)
    test_nm_to_info(700)
    test_nm_to_info(2000)
