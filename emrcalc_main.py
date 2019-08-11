"""
EMR Calculator Main Program
"""

import sys
import emrcalc_utilities as utl
from emrcalc_tk import init_tk_objects
from emrcalc_state import EMR_Calc_State

# ----------------------------------------------------------
# Global variables
main_window = None
state_obj = None

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
    global state_obj

    ### Must be a main program
    if __name__ != "__main__":
        oops("initialization: Must be a main program")

    ### Must be Python 3.x
    if sys.version_info[0] < 3:
        oops("initialization: Requires Python 3")

    ### Start with visible green
    frequency = 540e12 # Hz
    desc, energy, wavelen = utl.freq2info(frequency)
    state_obj = EMR_Calc_State(desc, energy, frequency, wavelen)

    ### Initialize all of the Tk objects that will be needed
    window = init_tk_objects(state_obj)

    ### Done, return logger handle to caller
    if state_obj.FLAG_TRACING:
        print("intialization:TRACE: End")
    return window

# ----------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------
### Call process initialization.
main_window = initialization()

# ----------------------------------------------------------
### Enter Tk mainloop
if state_obj.FLAG_TRACING:
    print("main:TRACE: Will now enter window mainloop")
main_window.mainloop()

# ----------------------------------------------------------
### Left Tk mainloop
if state_obj.FLAG_TRACING:
    print("main:TRACE: Just now exited window mainloop")
