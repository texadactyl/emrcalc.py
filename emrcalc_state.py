"""
EMR Calculator Class Definition for EMR_Calc_State
"""

class EMR_Calc_State():
    """
    EMR Calculator State Variables
    """

    FLAG_TRACING = False
    FRAME_BG = "aquamarine"

    band_desc = "RUBBISH"
    disp_value_energy = 0.0
    disp_value_freq = 0.0
    disp_value_wvlen = 0.0

    norm_value_energy = 0.0 # eV
    norm_value_freq = 0.0 # Hz
    norm_value_wvlen = 0.0 # meters

    list_units_energy = ("eV", "J")
    list_units_freq = ("Hz", "MHz", "GHz")
    list_units_wvlen = ("m", "μm", "nm", "Å")

    disp_units_energy = list_units_energy[0]
    disp_units_freq = list_units_freq[0]
    disp_units_wvlen = list_units_wvlen[0]

    def __init__(self, arg_desc, arg_energy, arg_freq, arg_wvlen):
        """
        Initialize a new EMR_Calc_State object.
        """
        self.band_desc = arg_desc
        self.norm_value_energy = self.disp_value_energy = arg_energy
        self.norm_value_freq = self.disp_value_freq = arg_freq
        self.norm_value_wvlen = self.disp_value_wvlen = arg_wvlen
