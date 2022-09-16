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
        super().__init__(title="Hello World")

        self.iap = None
        self.set_default_size(800, 800)
        self.connect("destroy", self.on_destroy)
        self.connect("key-press-event", self.on_keypress)
        self.connect("key-release-event", self.on_keyrelease)

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
        lst = ["coucou", "man", "yes"]
        combo = Gtk.ComboBoxText()
        for item in lst:
            combo.append_text(item)

        combo.set_active(0)
        combo.connect("changed", self.on_change)
        # combo.connect("key-release-event", self.on_keyrelease)
        box.add(combo)
        
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

    def on_change(self, widget):
        print("Hello World")
        if widget.get_text_length() <= 3:
            beep()

    #-------------------------------------------

    def on_keypress(self, widget, evt):
        """
        Note: pygtk do not report error when klass or attribute is not found.
        """

        if self.iap is None: return
        keyname = Gdk.keyval_name(evt.keyval)
        if keyname == "q":
            beep()
        elif keyname == "h":
            beep()
            self.iap.note_on()
        elif keyname == "KP_0":
            self.iap.note_on()
        
        is_ctrl = bool(evt.state & Gdk.ModifierType.CONTROL_MASK)
        is_shift = bool(evt.state & Gdk.ModifierType.SHIFT_MASK)
        is_alt = bool(evt.state & Gdk.ModifierType.MOD1_MASK)
        
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
        if keyname == "h" or keyname == "KP_0":
            self.iap.note_off()
            pass
        # beep()
        pass

    #-------------------------------------------

#========================================
if __name__ == "__main__":
    win = MainWindow()
    Gtk.main()

#-------------------------------------------
