"""
EMR Calculator Main Program
"""

import sys
import emrcalc_utilities as utl
from emrcalc_tk import init_tk_objects
from emrcalc_state import EMR_Calc_State

# ----------------------------------------------------------
# Global variables
REQUIRED_MAJOR = 3
REQUIRED_MINOR = 7
MAIN_WINDOW = None
STATE_OBJECT = None
VERSION = "rubbish"

def oops(arg_string):
    """
    Log an error-string in the text window and return to caller
    """
    print("\n*** Oops, {}\n\n".format(arg_string))
    sys.exit(86)

def initialization():
    """
    Initialize the process.
    """
    ### Must be a main program
    if __name__ != "__main__":
        oops("initialization: Must be a main program")

    ### Must be Python 3.x
    if sys.version_info.major < REQUIRED_MAJOR \
    or sys.version_info.minor < REQUIRED_MINOR:
        oops("initialization: Requires Python {}.{} or higher."
             .format(REQUIRED_MAJOR, REQUIRED_MINOR))

    ### Start with visible green
    frequency = 540e12 # Hz
    desc, energy, wavelen = utl.freq2info(frequency)
    state_object = EMR_Calc_State(desc, energy, frequency, wavelen)

    ### Initialize all of the Tk objects that will be needed
    VERSION = open("VERSION.txt").read()
    window = init_tk_objects(state_object, VERSION)

    ### Done, return logger handle to caller
    if state_object.FLAG_TRACING:
        print("intialization:TRACE: End")
    return state_object, window

# ----------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------
### Call process initialization.
STATE_OBJECT, MAIN_WINDOW = initialization()

# ----------------------------------------------------------
### Enter Tk mainloop
if STATE_OBJECT.FLAG_TRACING:
    print("main:TRACE: Will now enter window mainloop")
MAIN_WINDOW.mainloop()

# ----------------------------------------------------------
### Left Tk mainloop
if STATE_OBJECT.FLAG_TRACING:
    print("main:TRACE: Just now exited window mainloop")
