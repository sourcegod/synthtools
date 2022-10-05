#!/usr/bin/python3
"""
    File: synth_gui.py
    IGraphic interface for fastsynth module 
    using Gtk tools
    Date: Fri, 16/09/2022
    Author: Coolbrother
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import time
import threading
import interfaceapp as _iap

def beep():
    print("\a")

#-------------------------------------------


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Fast Synth")

        self.iap = None
        self.set_default_size(800, 800)
        self.connect("destroy", self.on_destroy)
        self.connect("key-press-event", self.on_keypress)
        self.connect("key-release-event", self.on_keyrelease)
        # Note: using Shift key with Keypad keys to obtain KP_Insert, KP_Down ...
        self._key_notes = {
                "KP_0": 0, "KP_Insert": 1, "KP_1": 2, "KP_End": 3, 
                "KP_2": 4, "KP_Down": 5,
                "KP_3": 5, "KP_Next": 6, "KP_4": 7, "KP_Left": 8,
                "KP_5": 9, "KP_Begin": 10, "KP_6": 11, "KP_Right": 12,
                "KP_7": 12, "KP_Home": 13, "KP_8": 14, "KP_Up": 15,
                "KP_9": 16, "KP_Page_Up": 17
                }

        self.create_ui()
        # init Interface Synth
        self.init_app()
        self.show_all()

    #-------------------------------------------

    def create_ui(self):
        """
        Create the User Interface 
        """

        # connect the key-press event - this will call the keypress
        # handler when any key is pressed
        box = Gtk.VBox(spacing=6)
        self.add(box)
        # volume adjust
        # default value, min, max, step, page_step, page_size
        lb1 = Gtk.Label(label="Volume Params")
        box.add(lb1)
        adj0 = Gtk.Adjustment(1.0, 0, 1.0, 0.01, 0.1, 0.0)
        self._vol_scale = Gtk.HScale(adjustment=adj0)
        # sets the number of decimal to scale
        self._vol_scale.set_digits(2)
        self._vol_scale.connect("value-changed", self.on_change_volume)
        box.add(self._vol_scale)


        # Simple Combobox
        # lst = ["coucou", "man", "yes"]
        self._combo = Gtk.ComboBoxText()
        
        # filling the combo later
        self._combo.connect("changed", self.on_change_combo)
        box.add(self._combo)

        # Enveloppe widgets
        lb1 = Gtk.Label(label="Enveloppe Params")
        box.add(lb1)
        
        self._env_combo = Gtk.ComboBoxText()
        env_lst = ["Attack", "Decay", "Sustain", "Release", ]
                # "FilterMode", "Cutoff", "Resonance",
        for item in env_lst:
            self._env_combo.append_text(item)
        self._env_combo.set_active(0)
        self._env_combo.connect("changed", self.on_change_envparam)
        box.add(self._env_combo)
 
        # Adjustments with
                      # value, min, max, step_incr, pg_incr, pg_size
        self._adj1 = Gtk.Adjustment(0.1, 0.01, 5.0, 0.01, 0.1, 0.0)

        self._env_scale = Gtk.HScale(adjustment=self._adj1)
        # sets the number of decimal to scale
        # self._adj1.configure(0, 0, 5, 1, 1, 0.0)
        self._env_scale.set_digits(2)
        self._env_scale.connect("value-changed", self.on_change_envscale)

        box.add(self._env_scale)
        
        # Filter Mode widgets
        lb1 = Gtk.Label(label="Filter Mode")
        box.add(lb1)
        self._fil_mode = Gtk.ComboBoxText()
        fil_lst = ["Low Pass", "Band Pass", "High Pass", ]
        for item in fil_lst:
            self._fil_mode.append_text(item)
        self._fil_mode.set_active(0)
        self._fil_mode.connect("changed", self.on_change_filmode)
        box.add(self._fil_mode)
         
         # Cutoff widget
        lb1 = Gtk.Label(label="Filter Cutoff")
        box.add(lb1)
        adj1 = Gtk.Adjustment(0.99, 0.01, 0.99, 0.01, 0.1, 0.0)

        self._fil_cutoff = Gtk.HScale(adjustment=adj1)
        self._fil_cutoff.set_digits(2)
        self._fil_cutoff.connect("value-changed", self.on_change_filcutoff)

        box.add(self._fil_cutoff)

        # Resonance widget
        lb1 = Gtk.Label(label="Filter Resonance")
        box.add(lb1)
        adj1 = Gtk.Adjustment(0.01, 0.01, 0.99, 0.01, 0.1, 0.0)
        self._fil_resonance = Gtk.HScale(adjustment=adj1)
        self._fil_resonance.set_digits(2)
        self._fil_resonance.connect("value-changed", self.on_change_filresonance)

        box.add(self._fil_resonance)


        """
        self.entry = Gtk.Entry()
        self.entry.set_text("-> ")
        self.entry.connect("activate", self.on_activate_entry, self.entry)
        box.add(self.entry)
        """

        """
        bt1 = Gtk.Button(label="Click Here")
        bt1.connect("clicked", self.on_click)
        box.add(bt1)
        """
        
        tv = Gtk.TextView()
        self.buf = tv.get_buffer()
        self.buf.set_text("-> ")
        tv.set_editable(False)
        box.add(tv)
 
    #-------------------------------------------

    def on_destroy(self, wid):
        if self.iap: 
            self.iap.close_app()
        print("Bye Bye!")
        Gtk.main_quit()

    #-------------------------------------------

    def init_app(self):
        """
        init the Synth Interface
        """
        self.iap = _iap.InterfaceApp()
        self.iap.init_app()
        if self.iap and self._combo:
            mode_lst = self.iap.get_mode_list()
            for item in mode_lst:
                self._combo.append_text(item)
            self._combo.set_active(0)


    #-------------------------------------------

    def on_activate_entry(self, widget, entry):
        text = widget.get_text()
        print(f"The contents is: {text}")
        beep()

    def on_click(self, widget):
        print("Hello World")
        # MyThread("A").start()
        # beep()
        # prtt()

        # """
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "This is an INFO MessageDialog")
        dialog.format_secondary_text(
            "And this is the secondary text that explains things.")
        dialog.run()
        # """

        print("INFO dialog closed")

        dialog.destroy()

    #-------------------------------------------

    def on_change_volume(self, widget):
        """
        change volume scale
        """

        param_index =0
        index =0
        val = widget.get_value()
        if self.iap:
            self.iap.change_param(param_index, index, val)


    #-------------------------------------------

    def on_change_combo(self, widget):
        # text = widget.get_active_text()
        param_index =1
        index =0
        val = widget.get_active()
        # self.buf.set_text(f"Combo Index: {index}")
        if self.iap:
            # self.iap.set_mode(index)
            self.iap.change_param(param_index, index, val)

        """
        # print("Hello World")
        if widget.get_text_length() <= 3:
            beep()
        """

    #-------------------------------------------

    def on_change_envparam(self, widget):
        """
        change envelope param combo
        """

        # text = widget.get_active_text()
        param_index =2
        index =0
        val = widget.get_active()
        
        
        """
        if index == 0:
            # Waveform mode
            self._adj1.configure(0, 0, 5, 1, 1, 0.0)
        elif index in [1, 2, 3, 4]:
            # Enveloppe params
            self._adj1.configure(0.01, 0.01, 1.0, 0.01, 0.1, 0.0)
            self._env_scale.set_digits(2)
        elif index == 5:
            # Filter mode
            self._adj1.configure(0, 0, 2, 1, 1, 0.0)
        elif index == 6:
            # Filter Cutoff
            # Value must be never at 1.0 to avoid ZeroDivision Error
            self._adj1.configure(0.99, 0.01, 0.99, 0.01, 0.1, 0.0)
            self._env_scale.set_digits(2)
        elif index == 7:
            # Filter Resonance
            self._adj1.configure(0.01, 0.01, 1.0, 0.01, 0.1, 0.0)
            self._env_scale.set_digits(2)
        """

        if self.iap:
            # self.iap.change_param(param_index, index, val)
            pass

    #-------------------------------------------

    def on_change_envscale(self, widget):
        """
        change envelope param scale
        """

        param_index =3
        index = self._env_combo.get_active()
        val = widget.get_value()
        # beep()
        if self.iap:
            self.iap.change_param(param_index, index, val)


    #-------------------------------------------

    def on_change_filmode(self, widget):
        """
        change filter mode
        """

        param_index =4
        index =0
        val = widget.get_active()
        if self.iap:
            self.iap.change_param(param_index, index, val)

    #-------------------------------------------

    def on_change_filcutoff(self, widget):
        """
        change filter cutoff
        """

        param_index =5
        index =0
        val = widget.get_value()
        if self.iap:
            self.iap.change_param(param_index, index, val)

    #-------------------------------------------

    def on_change_filresonance(self, widget):
        """
        change filter resonance
        """

        param_index =6
        index =0
        val = widget.get_value()
        if self.iap:
            self.iap.change_param(param_index, index, val)

    #-------------------------------------------


    def on_keypress(self, widget, evt):
        """
        Note: pygtk do not report error when klass or attribute is not found.
        """

        index =0
        if self.iap is None: return
        keyname = Gdk.keyval_name(evt.keyval)
        is_ctrl = bool(evt.state & Gdk.ModifierType.CONTROL_MASK)
        is_shift = bool(evt.state & Gdk.ModifierType.SHIFT_MASK)
        is_alt = bool(evt.state & Gdk.ModifierType.MOD1_MASK)
        if keyname == "Q":
            beep()
        elif keyname == "h":
            beep()
            self.iap.note_on()
        elif keyname in self._key_notes.keys():
            octave = self.iap.get_key_base()
            note = octave + self._key_notes[keyname]
            self.iap.note_on(note, 127)
        elif keyname == "KP_Subtract":
            self.iap.change_key_base(step=-12, adding=1)
        elif keyname == "KP_Add":
            self.iap.change_key_base(step=12, adding=1)
       
        if is_ctrl:
            beep()
        
        if is_shift:
            beep()
            time.sleep(0.1)
            beep()
            pass
        if is_alt:
            beep()

        self.buf.set_text(f"Key: {keyname}")
        # self.buf.insert(0, f"{keyname}")
        # beep()
        # Gtk.Window.Beep()
        pass

    #-------------------------------------------


    def on_keyrelease(self, widget, evt):
        if self.iap is None: return
        keyname = Gdk.keyval_name(evt.keyval)
        if keyname == "h":
            self.iap.note_off()
            pass
        elif keyname in self._key_notes.keys():
            octave = self.iap.get_key_base()
            note = octave + self._key_notes[keyname]
            self.iap.note_off(note, 0)
 
        # beep()

    #-------------------------------------------

#========================================
if __name__ == "__main__":
    win = MainWindow()
    Gtk.main()

#-------------------------------------------
