"""
EMR Calculator Main Program
"""

import sys

from emrcalc import __version__
import emrcalc.emrcalc_utilities as utl
from emrcalc.emrcalc_tk import init_tk_objects
from emrcalc.emrcalc_state import EMR_Calc_State

# Global variables
REQUIRED_MAJOR = 3
REQUIRED_MINOR = 7

def oops(arg_string):
    """
    Log an error-string in the text window and return to caller
    """
    print(f"\n*** Oops, {arg_string}\n\n")
    sys.exit(86)

def initialization():
    """
    Initialize the process.
    """
    ### Must be Python 3.7 or later
    if sys.version_info.major < REQUIRED_MAJOR \
    or sys.version_info.minor < REQUIRED_MINOR:
        oops(f"initialization: Requires Python {REQUIRED_MAJOR}.{REQUIRED_MINOR} or later.")

    ### Start with visible green
    frequency = 540e12 # Hz
    desc, energy, wavelen, wavenum = utl.freq2info(frequency)
    state_object = EMR_Calc_State(desc, energy, frequency, wavelen, wavenum)

    ### Initialize all of the Tk objects that will be needed
    window = init_tk_objects(state_object, __version__)

    ### Done, return logger handle to caller
    if state_object.FLAG_TRACING:
        print("intialization:TRACE: End")
    return state_object, window


def main():

    """
    Main program entry point
    """
    main_window = None
    state_object = None

    ### Call process initialization.
    state_object, main_window = initialization()

    # ----------------------------------------------------------
    ### Enter Tk mainloop
    if state_object.FLAG_TRACING:
        print("main:TRACE: Will now enter window mainloop")
    main_window.mainloop()

    # ----------------------------------------------------------
    ### Left Tk mainloop
    if state_object.FLAG_TRACING:
        print("main:TRACE: Just now exited window mainloop")

if __name__ == "__main__":
    main()
