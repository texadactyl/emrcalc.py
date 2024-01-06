"""
emrcalc Tk procedures
"""
import tkinter as tk
from tkinter import ttk

from emrcalc.emrcalc_utilities import float2str, freq2info, energy2info, wvlen2info, J2EV

# Global constants:
PAD_HORZ = 2
PAD_VERT = 2
SIGFIG = 5
STATUS_OK = "Everything is nominal, Captain."
STATUS_OOPS = "This makes no sense, Captain: "
STYLE_FRAME1 = "My.TFrame"
WIDTH_FLOAT = 12
WIDTH_UNITS = 4
FONT_GENERAL = ("Ariel", 12, "normal")
FONT_LABEL = ("Ariel", 12, "normal")

# Energy units
UNITS_J = "J"
UNITS_KJ = "kJ"
UNITS_EV = "eV"

# Wavelength units
UNITS_METERS = "m"
UNITS_MICRONS = "μm"
UNITS_NM = "nm"
UNITS_ANGSTROMS = "Å"

# wavenumber units
UNITS_IM = "1/m"
UNITS_ICM = "1/cm"

# Frequency units
UNITS_HZ = "Hz"
UNITS_MHZ = "MHz"
UNITS_GHZ = "Ghz"

# Other global variables:
ENTRY_ENERGY = None
ENTRY_FREQ = None
ENTRY_WVLEN = None
ENTRY_WVNUM = None
SPINBOX_ENERGY = None
SPINBOX_FREQ = None
SPINBOX_WVLEN = None
SPINBOX_WVNUM = None
STATE_OBJECT = None
TEXT_KJMOL = None
TEXT_DESC = None
TEXT_STATUS = None
WINDOW = None

def destroyer():
    """
    Operator selected to quit to the O/S.
    """

    if STATE_OBJECT.FLAG_TRACING:
        print("destroyer:TRACE: Begin")
    if not WINDOW is None:
        if STATE_OBJECT.FLAG_TRACING:
            print("destroyer:TRACE: Destroying the main window now")
        WINDOW.destroy()
    if STATE_OBJECT.FLAG_TRACING:
        print("destroyer:TRACE: End")

def refresh_all_display_values():
    """
    Update Tk display from the normalized values in the state object.
    """
    global STATE_OBJECT, ENTRY_FREQ, ENTRY_WVLEN, ENTRY_WVNUM, ENTRY_ENERGY, TEXT_KJMOL, TEXT_DESC

    if STATE_OBJECT.FLAG_TRACING:
        print("refresh_all_display_values:TRACE: Begin")

    # --- Energy
    if STATE_OBJECT.disp_units_energy == UNITS_J:
        STATE_OBJECT.disp_value_energy = STATE_OBJECT.norm_value_energy
    else:
        if STATE_OBJECT.disp_units_energy == UNITS_KJ:
            STATE_OBJECT.disp_value_energy = STATE_OBJECT.norm_value_energy / 1e3
        else: # eV
            STATE_OBJECT.disp_value_energy = STATE_OBJECT.norm_value_energy * J2EV
    ENTRY_ENERGY.delete(0, tk.END)
    ENTRY_ENERGY.insert(0, float2str(STATE_OBJECT.disp_value_energy, SIGFIG))

    # --- kJ/mol (energy density)
    STATE_OBJECT.update_kJ_per_mol()
    TEXT_KJMOL["text"] = float2str(STATE_OBJECT.kJ_per_mol, SIGFIG)

    # --- Frequency
    if STATE_OBJECT.disp_units_freq == UNITS_HZ:
        STATE_OBJECT.disp_value_freq = STATE_OBJECT.norm_value_freq
    else:
        if STATE_OBJECT.disp_units_freq == UNITS_MHZ:
            STATE_OBJECT.disp_value_freq = STATE_OBJECT.norm_value_freq / 1e6
        else: # UNITS_GHZ
            STATE_OBJECT.disp_value_freq = STATE_OBJECT.norm_value_freq / 1e9
    ENTRY_FREQ.delete(0, tk.END)
    ENTRY_FREQ.insert(0, float2str(STATE_OBJECT.disp_value_freq, SIGFIG))

    # --- Wavelength
    if STATE_OBJECT.disp_units_wvlen == UNITS_METERS:
        STATE_OBJECT.disp_value_wvlen = STATE_OBJECT.norm_value_wvlen
    else:
        if STATE_OBJECT.disp_units_wvlen == UNITS_MICRONS:
            STATE_OBJECT.disp_value_wvlen = STATE_OBJECT.norm_value_wvlen * 1e6
        else:
            if STATE_OBJECT.disp_units_wvlen == UNITS_NM:
                STATE_OBJECT.disp_value_wvlen = STATE_OBJECT.norm_value_wvlen * 1e9
            else: # Angstroms
                STATE_OBJECT.disp_value_wvlen = STATE_OBJECT.norm_value_wvlen * 1e10
    ENTRY_WVLEN.delete(0, tk.END)
    ENTRY_WVLEN.insert(0, float2str(STATE_OBJECT.disp_value_wvlen, SIGFIG))

    # --- wavenumber
    if STATE_OBJECT.disp_units_wvnum == UNITS_IM:
        STATE_OBJECT.disp_value_wvnum = STATE_OBJECT.norm_value_wvnum
    else: # 1/cm
        STATE_OBJECT.disp_value_wvnum = STATE_OBJECT.norm_value_wvnum / 100
    ENTRY_WVNUM.delete(0, tk.END)
    ENTRY_WVNUM.insert(0, float2str(STATE_OBJECT.disp_value_wvnum, SIGFIG))

    # --- Band descriptor
    TEXT_DESC["text"] = str(STATE_OBJECT.band_desc)

    if STATE_OBJECT.FLAG_TRACING:
        print("refresh_all_display_values:TRACE: End")

def proc_energy_value():
    """
    The operator modified the energy value.
    """
    global STATE_OBJECT, ENTRY_ENERGY, TEXT_STATUS

    if STATE_OBJECT.FLAG_TRACING:
        print("proc_energy_value:TRACE: Begin")
    new_str_value = ENTRY_ENERGY.get()
    try:
        new_float_value = float(new_str_value)
        # new norm = old norm * ( new disp / old disp)
        STATE_OBJECT.norm_value_energy = STATE_OBJECT.norm_value_energy \
            * new_float_value / STATE_OBJECT.disp_value_energy
        # Recompute desc, frequency, & wavelength based on normalized energy
        STATE_OBJECT.band_desc, \
            STATE_OBJECT.norm_value_freq, \
            STATE_OBJECT.norm_value_wvlen, \
            STATE_OBJECT.norm_value_wvnum = energy2info(STATE_OBJECT.norm_value_energy)
        refresh_all_display_values()
        TEXT_STATUS['text'] = STATUS_OK
    except:
        TEXT_STATUS['text'] = STATUS_OOPS + new_str_value
    if STATE_OBJECT.FLAG_TRACING:
        print("proc_energy_value:TRACE: End")

def proc_freq_value():
    """
    The operator modified the frequency value.
    """
    global STATE_OBJECT, ENTRY_FREQ, TEXT_STATUS

    if STATE_OBJECT.FLAG_TRACING:
        print("proc_freq_value:TRACE: Begin")
    new_str_value = ENTRY_FREQ.get()
    try:
        new_float_value = float(new_str_value)
        # new norm = old norm * ( new disp / old disp)
        STATE_OBJECT.norm_value_freq = STATE_OBJECT.norm_value_freq \
            * new_float_value / STATE_OBJECT.disp_value_freq
        # Recompute desc, energy, & wavelength based on normalized energy
        STATE_OBJECT.band_desc, \
            STATE_OBJECT.norm_value_energy, \
            STATE_OBJECT.norm_value_wvlen, \
            STATE_OBJECT.norm_value_wvnum = freq2info(STATE_OBJECT.norm_value_freq)
        refresh_all_display_values()
        TEXT_STATUS['text'] = STATUS_OK
    except:
        TEXT_STATUS['text'] = STATUS_OOPS + new_str_value
    if STATE_OBJECT.FLAG_TRACING:
        print("proc_freq_value:TRACE: End")

def proc_wvlen_value():
    """
    The operator modified the wavelength value.
    """
    global STATE_OBJECT, ENTRY_WVLEN, TEXT_STATUS

    if STATE_OBJECT.FLAG_TRACING:
        print("proc_wvlen_value:TRACE: Begin")
    new_str_value = ENTRY_WVLEN.get()
    try:
        new_float_value = float(new_str_value)
        # new norm = old norm * ( new disp / old disp)
        STATE_OBJECT.norm_value_wvlen = STATE_OBJECT.norm_value_wvlen \
            * new_float_value / STATE_OBJECT.disp_value_wvlen
        # Recompute desc, energy, & wavelength based on normalized energy
        STATE_OBJECT.band_desc, \
            STATE_OBJECT.norm_value_energy, \
            STATE_OBJECT.norm_value_freq, \
            STATE_OBJECT.norm_value_wvnum = wvlen2info(STATE_OBJECT.norm_value_wvlen)
        refresh_all_display_values()
        TEXT_STATUS['text'] = STATUS_OK
    except:
        TEXT_STATUS['text'] = STATUS_OOPS + new_str_value
    if STATE_OBJECT.FLAG_TRACING:
        print("proc_wvlen_value:TRACE: End")

def proc_wvnum_value():
    """
    The operator modified the wavenumber value.
    """
    global STATE_OBJECT, ENTRY_WVNUM, TEXT_STATUS

    if STATE_OBJECT.FLAG_TRACING:
        print("proc_wvnum_value:TRACE: Begin")
    new_str_value = ENTRY_WVNUM.get()
    try:
        new_float_value = float(new_str_value)
        # new norm = old norm * ( new disp / old disp)
        STATE_OBJECT.norm_value_wvlen = STATE_OBJECT.norm_value_wvnum \
            * new_float_value / STATE_OBJECT.disp_value_wvnum
        STATE_OBJECT.norm_value_wvlen = 1 / STATE_OBJECT.norm_value_wvlen
        # Recompute desc, energy, & wavelength based on normalized energy
        STATE_OBJECT.band_desc, \
            STATE_OBJECT.norm_value_energy, \
            STATE_OBJECT.norm_value_freq, \
            STATE_OBJECT.norm_value_wvnum = wvlen2info(STATE_OBJECT.norm_value_wvlen)
        refresh_all_display_values()
        TEXT_STATUS['text'] = STATUS_OK
    except:
        TEXT_STATUS['text'] = STATUS_OOPS + new_str_value
    if STATE_OBJECT.FLAG_TRACING:
        print("proc_wvnum_value:TRACE: End")

def proc_energy_units():
    """
    The operator modified the energy units.
    """
    global STATE_OBJECT, ENTRY_FREQ, SPINBOX_FREQ

    new_units = SPINBOX_ENERGY.get()
    if new_units == STATE_OBJECT.disp_units_energy:
        return
    STATE_OBJECT.disp_units_energy = new_units
    refresh_all_display_values()
    ENTRY_ENERGY.focus_set()

def proc_freq_units():
    """
    The operator modified the frequency units.
    """
    global STATE_OBJECT, ENTRY_FREQ, SPINBOX_FREQ

    new_units = SPINBOX_FREQ.get()
    if new_units == STATE_OBJECT.disp_units_freq:
        return
    STATE_OBJECT.disp_units_freq = new_units
    refresh_all_display_values()
    ENTRY_FREQ.focus_set()

def proc_wvlen_units():
    """
    The operator modified the wavelength units.
    """
    global STATE_OBJECT, ENTRY_WVLEN, SPINBOX_WVLEN

    new_units = SPINBOX_WVLEN.get()
    if new_units == STATE_OBJECT.disp_units_wvlen:
        return
    STATE_OBJECT.disp_units_wvlen = new_units
    refresh_all_display_values()
    ENTRY_WVLEN.focus_set()

def proc_wvnum_units():
    """
    The operator modified the wavelength units.
    """
    global STATE_OBJECT, ENTRY_WVNUM, SPINBOX_WVNUM

    new_units = SPINBOX_WVNUM.get()
    if new_units == STATE_OBJECT.disp_units_wvnum:
        return
    STATE_OBJECT.disp_units_wvnum = new_units
    refresh_all_display_values()
    ENTRY_WVNUM.focus_set()

def init_tk_objects(arg_state_object, arg_version):
    """
    Present the operator with a set of buttons.
    """
    global WINDOW, STATE_OBJECT, \
        ENTRY_FREQ, ENTRY_WVLEN, ENTRY_WVNUM, ENTRY_ENERGY, TEXT_KJMOL, TEXT_DESC, TEXT_STATUS, \
        SPINBOX_FREQ, SPINBOX_WVLEN, SPINBOX_WVNUM, SPINBOX_ENERGY

    STATE_OBJECT = arg_state_object
    if STATE_OBJECT.FLAG_TRACING:
        print("init_tk_objects:TRACE: Begin, {} {} {} {}"
              .format(STATE_OBJECT.disp_value_freq, \
                      STATE_OBJECT.disp_value_wvlen, \
                      STATE_OBJECT.disp_value_wvnum, \
                      STATE_OBJECT.disp_value_energy))

    # Create window.
    WINDOW = tk.Tk()
    WINDOW.attributes("-fullscreen", False)
    WINDOW.title("EMR Calculator v" + arg_version)
    WINDOW.columnconfigure(0, weight=1)

    # Change default fonts.
    WINDOW.option_add("*Font", FONT_GENERAL)
    WINDOW.option_add("*Label*Font", FONT_LABEL)

    # Set up frame.
    style = ttk.Style()
    style.configure(STYLE_FRAME1, background=STATE_OBJECT.FRAME_BG)
    frame1 = ttk.Frame(WINDOW, style=STYLE_FRAME1)
    frame1.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    # Set up heading row.
    label_heading1 = ttk.Label(frame1, text="Value")
    label_heading1.grid(column=1, row=0, padx=PAD_HORZ, pady=PAD_VERT)
    label_heading2 = ttk.Label(frame1, text="Units")
    label_heading2.grid(column=3, row=0, padx=PAD_HORZ, pady=PAD_VERT)

    # Set up frequency row.
    label_freq = ttk.Label(frame1, text="Frequency:")
    label_freq.grid(column=0, row=1, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    ENTRY_FREQ = ttk.Entry(frame1, width=WIDTH_FLOAT, justify=tk.RIGHT)
    ENTRY_FREQ.focus_set()
    ENTRY_FREQ.insert(0, float2str(STATE_OBJECT.disp_value_freq, SIGFIG))
    ENTRY_FREQ.grid(column=1, row=1, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))
    button_freq = ttk.Button(frame1, text="Update", command=proc_freq_value)
    button_freq.grid(column=2, row=1, padx=PAD_HORZ, pady=PAD_VERT)
    SPINBOX_FREQ = ttk.Spinbox(frame1, width=WIDTH_UNITS, command=proc_freq_units)
    SPINBOX_FREQ['values'] = STATE_OBJECT.list_units_freq
    SPINBOX_FREQ.set(STATE_OBJECT.disp_units_freq)
    SPINBOX_FREQ.grid(column=3, row=1, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up wavelength row.
    label_wvlen = ttk.Label(frame1, text="Wavelength:")
    label_wvlen.grid(column=0, row=2, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    ENTRY_WVLEN = ttk.Entry(frame1, width=WIDTH_FLOAT, justify=tk.RIGHT)
    ENTRY_WVLEN.insert(0, float2str(STATE_OBJECT.disp_value_wvlen, SIGFIG))
    ENTRY_WVLEN.grid(column=1, row=2, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))
    button_wvlen = ttk.Button(frame1, text="Update", command=proc_wvlen_value)
    button_wvlen.grid(column=2, row=2, padx=PAD_HORZ, pady=PAD_VERT)
    SPINBOX_WVLEN = ttk.Spinbox(frame1, width=WIDTH_UNITS, command=proc_wvlen_units)
    SPINBOX_WVLEN['values'] = STATE_OBJECT.list_units_wvlen
    SPINBOX_WVLEN.set(STATE_OBJECT.disp_units_wvlen)
    SPINBOX_WVLEN.grid(column=3, row=2, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up wavenumber row.
    label_wvnum = ttk.Label(frame1, text="Wavenumber:")
    label_wvnum.grid(column=0, row=3, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    ENTRY_WVNUM = ttk.Entry(frame1, width=WIDTH_FLOAT, justify=tk.RIGHT)
    ENTRY_WVNUM.insert(0, float2str(STATE_OBJECT.disp_value_wvnum, SIGFIG))
    ENTRY_WVNUM.grid(column=1, row=3, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))
    button_wvnum = ttk.Button(frame1, text="Update", command=proc_wvnum_value)
    button_wvnum.grid(column=2, row=3, padx=PAD_HORZ, pady=PAD_VERT)
    SPINBOX_WVNUM = ttk.Spinbox(frame1, width=WIDTH_UNITS, command=proc_wvnum_units)
    SPINBOX_WVNUM['values'] = STATE_OBJECT.list_units_wvnum
    SPINBOX_WVNUM.set(STATE_OBJECT.disp_units_wvnum)
    SPINBOX_WVNUM.grid(column=3, row=3, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up energy row.
    label_energy = ttk.Label(frame1, text="Energy:")
    label_energy.grid(column=0, row=4, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    ENTRY_ENERGY = ttk.Entry(frame1, width=WIDTH_FLOAT, justify=tk.RIGHT)
    ENTRY_ENERGY.insert(0, float2str(STATE_OBJECT.disp_value_energy, SIGFIG))
    ENTRY_ENERGY.grid(column=1, row=4, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))
    button_energy = ttk.Button(frame1, text="Update", command=proc_energy_value)
    button_energy.grid(column=2, row=4, padx=PAD_HORZ, pady=PAD_VERT)
    SPINBOX_ENERGY = ttk.Spinbox(frame1, width=WIDTH_UNITS, command=proc_energy_units)
    SPINBOX_ENERGY['values'] = STATE_OBJECT.list_units_energy
    SPINBOX_ENERGY.set(STATE_OBJECT.disp_units_energy)
    SPINBOX_ENERGY.grid(column=3, row=4, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up kJ/mol row.
    label_desc = ttk.Label(frame1, text="kJ/mol:")
    label_desc.grid(column=0, row=5, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    TEXT_KJMOL = tk.Label(frame1, justify=tk.CENTER)
    TEXT_KJMOL["text"] = float2str(STATE_OBJECT.kJ_per_mol, SIGFIG)
    TEXT_KJMOL.grid(column=1, row=5, columnspan=3, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up description row.
    label_desc = ttk.Label(frame1, text="EMR Band:")
    label_desc.grid(column=0, row=6, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    TEXT_DESC = tk.Label(frame1, justify=tk.CENTER)
    TEXT_DESC["text"] = str(STATE_OBJECT.band_desc)
    TEXT_DESC.grid(column=1, row=6, columnspan=3, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up buttons.
    button_quit = ttk.Button(frame1, text="Quit", command=destroyer)
    button_quit.grid(columnspan=3, padx=PAD_HORZ, pady=PAD_VERT)

    # Set up status line.
    TEXT_STATUS = ttk.Label(frame1, justify=tk.LEFT)
    TEXT_STATUS.grid(columnspan=4, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))
    TEXT_STATUS["text"] = STATUS_OK

    # Add row and column resizing.
    WINDOW.rowconfigure(0, weight=1)
    frame1.columnconfigure(0, weight=3)
    frame1.columnconfigure(1, weight=3)
    frame1.columnconfigure(2, weight=3)
    frame1.columnconfigure(3, weight=3)
    frame1.rowconfigure(1, weight=1)

    # All done.
    if STATE_OBJECT.FLAG_TRACING:
        print("init_tk_objects:TRACE: End")
    return WINDOW
