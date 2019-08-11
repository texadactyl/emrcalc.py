"""
emrcalc Tk procedures
"""
import tkinter as tk
import tkinter.ttk as ttk

from emrcalc_utilities import float2str, freq2info, energy2info, wvlen2info, J2EV

# Global constants:
PAD_HORZ = 2
PAD_VERT = 2
SIGFIG = 5
STATUS_OK = "Everything is nominal, Captain."
STATUS_OOPS = "This makes no sense, Captain: "
STYLE_FRAME1 = "My.TFrame"
WIDTH_FLOAT = 12
WIDTH_UNITS = 3
FONT_GENERAL = ("Ariel", 12, "normal")
FONT_LABEL = ("Ariel", 12, "normal")
UNITS_EV = "eV"
UNITS_METERS = "m"
UNITS_MICRONS = "μm"
UNITS_NM = "nm"
UNITS_ANGSTROMS = "Å"
UNITS_HZ = "Hz"
UNITS_MHZ = "MHz"
UNITS_GHZ = "Ghz"

# Global variables:
entry_energy = None
entry_freq = None
entry_wvlen = None
text_desc = None
text_status = None
spinbox_energy = None
spinbox_freq = None
spinbox_wvlen = None
state_obj = None
window = None

def destroyer():
    """
    Operator selected to quit to the O/S.
    """
    global window

    if state_obj.FLAG_TRACING:
        print("destroyer:TRACE: Begin")
    if not window is None:
        if state_obj.FLAG_TRACING:
            print("destroyer:TRACE: Destroying the main window now")
        window.destroy()
    if state_obj.FLAG_TRACING:
        print("destroyer:TRACE: End")

def refresh_all_display_values():
    """
    Update Tk display from the normalized values in the state object.
    """
    global state_obj, entry_freq, entry_wvlen, entry_energy, text_desc

    if state_obj.FLAG_TRACING:
        print("refresh_all_display_values:TRACE: Begin")

    # --- Energy
    if state_obj.disp_units_energy == UNITS_EV:
        state_obj.disp_value_energy = state_obj.norm_value_energy
    else: # Joules
        state_obj.disp_value_energy = state_obj.norm_value_energy / J2EV
    entry_energy.delete(0, tk.END)
    entry_energy.insert(0, float2str(state_obj.disp_value_energy, SIGFIG))

    # --- Frequency
    if state_obj.disp_units_freq == UNITS_HZ:
        state_obj.disp_value_freq = state_obj.norm_value_freq
    else:
        if state_obj.disp_units_freq == UNITS_MHZ:
            state_obj.disp_value_freq = state_obj.norm_value_freq / 1e6
        else: # UNITS_GHZ
            state_obj.disp_value_freq = state_obj.norm_value_freq / 1e9
    entry_freq.delete(0, tk.END)
    entry_freq.insert(0, float2str(state_obj.disp_value_freq, SIGFIG))

    # --- Wavelength
    if state_obj.disp_units_wvlen == UNITS_METERS:
        state_obj.disp_value_wvlen = state_obj.norm_value_wvlen
    else:
        if state_obj.disp_units_wvlen == UNITS_MICRONS:
            state_obj.disp_value_wvlen = state_obj.norm_value_wvlen * 1e6
        else:
            if state_obj.disp_units_wvlen == UNITS_NM:
                state_obj.disp_value_wvlen = state_obj.norm_value_wvlen * 1e9
            else: # Angstroms
                state_obj.disp_value_wvlen = state_obj.norm_value_wvlen * 1e10
    entry_wvlen.delete(0, tk.END)
    entry_wvlen.insert(0, float2str(state_obj.disp_value_wvlen, SIGFIG))

    # --- Band descriptor
    text_desc["text"] = str(state_obj.band_desc)

    if state_obj.FLAG_TRACING:
        print("refresh_all_display_values:TRACE: End")

def proc_energy_value():
    """
    The operator modified the energy value.
    """
    global state_obj, entry_energy, text_status

    if state_obj.FLAG_TRACING:
        print("proc_energy_value:TRACE: Begin")
    new_str_value = entry_energy.get()
    try:
        new_float_value = float(new_str_value)
        # new norm = old norm * ( new disp / old disp)
        state_obj.norm_value_energy = state_obj.norm_value_energy \
            * new_float_value / state_obj.disp_value_energy
        # Recompute desc, frequency, & wavelength based on normalized energy
        state_obj.band_desc, \
            state_obj.norm_value_freq, \
            state_obj.norm_value_wvlen = energy2info(state_obj.norm_value_energy)
        refresh_all_display_values()
        text_status['text'] = STATUS_OK
    except:
        text_status['text'] = STATUS_OOPS + new_str_value
    if state_obj.FLAG_TRACING:
        print("proc_energy_value:TRACE: End")

def proc_freq_value():
    """
    The operator modified the frequency value.
    """
    global state_obj, entry_freq, text_status

    if state_obj.FLAG_TRACING:
        print("proc_freq_value:TRACE: Begin")
    new_str_value = entry_freq.get()
    try:
        new_float_value = float(new_str_value)
        # new norm = old norm * ( new disp / old disp)
        state_obj.norm_value_freq = state_obj.norm_value_freq \
            * new_float_value / state_obj.disp_value_freq
        # Recompute desc, energy, & wavelength based on normalized energy
        state_obj.band_desc, \
            state_obj.norm_value_energy, \
            state_obj.norm_value_wvlen = freq2info(state_obj.norm_value_freq)
        refresh_all_display_values()
        text_status['text'] = STATUS_OK
    except:
        text_status['text'] = STATUS_OOPS + new_str_value
    if state_obj.FLAG_TRACING:
        print("proc_freq_value:TRACE: End")

def proc_wvlen_value():
    """
    The operator modified the wavelength value.
    """
    global state_obj, entry_wvlen, text_status

    if state_obj.FLAG_TRACING:
        print("proc_wvlen_value:TRACE: Begin")
    new_str_value = entry_wvlen.get()
    try:
        new_float_value = float(new_str_value)
        # new norm = old norm * ( new disp / old disp)
        state_obj.norm_value_wvlen = state_obj.norm_value_wvlen \
            * new_float_value / state_obj.disp_value_wvlen
        # Recompute desc, energy, & wavelength based on normalized energy
        state_obj.band_desc, \
            state_obj.norm_value_energy, \
            state_obj.norm_value_freq = wvlen2info(state_obj.norm_value_wvlen)
        refresh_all_display_values()
        text_status['text'] = STATUS_OK
    except:
        text_status['text'] = STATUS_OOPS + new_str_value
    if state_obj.FLAG_TRACING:
        print("proc_wvlen_value:TRACE: End")

def proc_energy_units():
    """
    The operator modified the energy units.
    """
    global state_obj, entry_freq, spinbox_freq

    new_units = spinbox_energy.get()
    if new_units == state_obj.disp_units_energy:
        return
    state_obj.disp_units_energy = new_units
    refresh_all_display_values()
    entry_energy.focus_set()

def proc_freq_units():
    """
    The operator modified the frequency units.
    """
    global state_obj, entry_freq, spinbox_freq

    new_units = spinbox_freq.get()
    if new_units == state_obj.disp_units_freq:
        return
    state_obj.disp_units_freq = new_units
    refresh_all_display_values()
    entry_freq.focus_set()

def proc_wvlen_units():
    """
    The operator modified the wavelength units.
    """
    global state_obj, entry_wvlen, spinbox_wvlen

    new_units = spinbox_wvlen.get()
    if new_units == state_obj.disp_units_wvlen:
        return
    state_obj.disp_units_wvlen = new_units
    refresh_all_display_values()
    entry_wvlen.focus_set()

def init_tk_objects(arg_state_obj):
    """
    Present the operator with a set of buttons.
    """
    global window, state_obj, \
        entry_freq, entry_wvlen, entry_energy, text_desc, text_status, \
        spinbox_freq, spinbox_wvlen, spinbox_energy

    state_obj = arg_state_obj
    if state_obj.FLAG_TRACING:
        print("init_tk_objects:TRACE: Begin, {} {} {}"
              .format(state_obj.disp_value_freq, \
                      state_obj.disp_value_wvlen, \
                      state_obj.disp_value_energy))

    # Create window.
    window = tk.Tk()
    window.attributes("-fullscreen", False)
    window.title("EMR Calculator")
    window.columnconfigure(0, weight=1)

    # Change default fonts.
    window.option_add("*Font", FONT_GENERAL)
    window.option_add("*Label*Font", FONT_LABEL)

    # Set up frame.
    style = ttk.Style()
    style.configure(STYLE_FRAME1, background=state_obj.FRAME_BG)
    frame1 = ttk.Frame(window, style=STYLE_FRAME1)
    frame1.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    # Set up heading row.
    label_heading1 = ttk.Label(frame1, text="Value")
    label_heading1.grid(column=1, row=0, padx=PAD_HORZ, pady=PAD_VERT)
    label_heading2 = ttk.Label(frame1, text="Units")
    label_heading2.grid(column=3, row=0, padx=PAD_HORZ, pady=PAD_VERT)

    # Set up frequency row.
    label_freq = ttk.Label(frame1, text="Frequency:")
    label_freq.grid(column=0, row=1, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    entry_freq = ttk.Entry(frame1, width=WIDTH_FLOAT, justify=tk.RIGHT)
    entry_freq.focus_set()
    entry_freq.insert(0, float2str(state_obj.disp_value_freq, SIGFIG))
    entry_freq.grid(column=1, row=1, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))
    button_freq = ttk.Button(frame1, text="Update", command=proc_freq_value)
    button_freq.grid(column=2, row=1, padx=PAD_HORZ, pady=PAD_VERT)
    spinbox_freq = ttk.Spinbox(frame1, width=WIDTH_UNITS, command=proc_freq_units)
    spinbox_freq['values'] = state_obj.list_units_freq
    spinbox_freq.set(state_obj.disp_units_freq)
    spinbox_freq.grid(column=3, row=1, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up wavelength row.
    label_wvlen = ttk.Label(frame1, text="Wavelength:")
    label_wvlen.grid(column=0, row=2, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    entry_wvlen = ttk.Entry(frame1, width=WIDTH_FLOAT, justify=tk.RIGHT)
    entry_wvlen.insert(0, float2str(state_obj.disp_value_wvlen, SIGFIG))
    entry_wvlen.grid(column=1, row=2, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))
    button_wvlen = ttk.Button(frame1, text="Update", command=proc_wvlen_value)
    button_wvlen.grid(column=2, row=2, padx=PAD_HORZ, pady=PAD_VERT)
    spinbox_wvlen = ttk.Spinbox(frame1, width=WIDTH_UNITS, command=proc_wvlen_units)
    spinbox_wvlen['values'] = state_obj.list_units_wvlen
    spinbox_wvlen.set(state_obj.disp_units_wvlen)
    spinbox_wvlen.grid(column=3, row=2, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up energy row.
    label_energy = ttk.Label(frame1, text="Energy:")
    label_energy.grid(column=0, row=3, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    entry_energy = ttk.Entry(frame1, width=WIDTH_FLOAT, justify=tk.RIGHT)
    entry_energy.insert(0, float2str(state_obj.disp_value_energy, SIGFIG))
    entry_energy.grid(column=1, row=3, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))
    button_energy = ttk.Button(frame1, text="Update", command=proc_energy_value)
    button_energy.grid(column=2, row=3, padx=PAD_HORZ, pady=PAD_VERT)
    spinbox_energy = ttk.Spinbox(frame1, width=WIDTH_UNITS, command=proc_energy_units)
    spinbox_energy['values'] = state_obj.list_units_energy
    spinbox_energy.set(state_obj.disp_units_energy)
    spinbox_energy.grid(column=3, row=3, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up description row.
    label_desc = ttk.Label(frame1, text="EMR Band:")
    label_desc.grid(column=0, row=4, sticky=tk.E, padx=PAD_HORZ, pady=PAD_VERT)
    text_desc = tk.Label(frame1, justify=tk.CENTER)
    text_desc["text"] = str(state_obj.band_desc)
    text_desc.grid(column=1, row=4, columnspan=3, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))

    # Set up buttons.
    button_quit = ttk.Button(frame1, text="Quit", command=destroyer)
    button_quit.grid(columnspan=3, padx=PAD_HORZ, pady=PAD_VERT)

    # Set up status line.
    text_status = ttk.Label(frame1, justify=tk.LEFT)
    text_status.grid(columnspan=4, padx=PAD_HORZ, pady=PAD_VERT, sticky=(tk.E, tk.W))
    text_status["text"] = STATUS_OK

    # Add row and column resizing.
    window.rowconfigure(0, weight=1)
    frame1.columnconfigure(0, weight=3)
    frame1.columnconfigure(1, weight=3)
    frame1.columnconfigure(2, weight=3)
    frame1.columnconfigure(3, weight=3)
    frame1.rowconfigure(1, weight=1)

    # All done.
    if state_obj.FLAG_TRACING:
        print("init_tk_objects:TRACE: End")
    return window
