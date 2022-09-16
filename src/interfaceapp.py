#!/usr/bin/env python3
"""
    File: interfaceapp.py
    Interface app for Fastsynth
    Date: Fri, 16/09/2022
    Author: Coolbrother
"""

import fastsynth as fsyn

class InterfaceApp(object):
    def __init__(self, parent=None):
        self._parent = parent
        self.synth = None
    
    #-------------------------------------------
    
    def init_app(self):
        self.synth = fsyn.FastSynth()
        self.synth.set_params(mode=0, muted=False) # mode 4: White Noise
        self.synth.start_engine()
        msg = "Init  App..."
        self._notify(msg)

    #-------------------------------------------

    def close_app(self):
        if self.synth:
            self.synth.stop_engine()
            self.beep()
        
        msg = "Closing App"
        self._notify(msg)

    #-------------------------------------------
    
    def note_on(self):
        if self.synth:
            self.synth.note_on()
        
        msg = "Note Off"
        self._notify(msg)


    #-------------------------------------------

    def note_off(self):
        if self.synth:
            self.synth.note_off()
        
        msg = "Note On"
        self._notify(msg)

    #-------------------------------------------

    def _notify(self, msg):
        if self._parent:
            self._parent.display(msg)

    #-------------------------------------------

    def beep(self):
        print("\a")

    #-------------------------------------------

#========================================

if __name__ == "__main__":
    iap = InterfaceApp()
    input("It's Ok...")
