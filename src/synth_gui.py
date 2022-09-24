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

        # Simple Combobox
        # lst = ["coucou", "man", "yes"]
        self._combo = Gtk.ComboBoxText()
        
        # filling the combo later
        """
        for item in mode_lst:
            self._combo.append_text(item)
        self._combo.set_active(0)
        """

        self._combo.connect("changed", self.on_change_combo)
        box.add(self._combo)
        
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

    def on_change_combo(self, widget):
        # text = widget.get_active_text()
        index = widget.get_active()
        self.buf.set_text(f"Combo Index: {index}")
        if self.iap:
            self.iap.set_mode(index)

        """
        # print("Hello World")
        if widget.get_text_length() <= 3:
            beep()
        """

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
