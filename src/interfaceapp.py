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
        self._key_base =60

    #-------------------------------------------
    
    def init_app(self):
        device_index = (6, 6) # (0, 0)
        channels =2
        self.synth = fsyn.FastSynth(device_index=device_index, channels=channels)
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

    def _notify(self, msg):
        if self._parent:
            self._parent.display(msg)

    #-------------------------------------------

    def beep(self):
        print("\a")

    #-------------------------------------------

    def note_on(self, note=60, vel=127):
        if not self.synth: return
        self.synth.note_on(note, vel)
        
        msg = "Note Off"
        self._notify(msg)

    #-------------------------------------------

    def note_off(self, note, vel):
        if not self.synth: return
        self.synth.note_off(note, vel)
        
        msg = "Note On"
        self._notify(msg)

    #-------------------------------------------

    def set_mode(self, mode):
        """
        sets synth mode:
        Sine, Square, Sawtooth ...
        """

        if not self.synth: return
        self.synth.set_mode(mode)
        
        mode = self.synth.get_mode()
        msg = f"Mode: {mode}"
        self._notify(msg)

    #-------------------------------------------

    def get_mode_list(self):
        """
        returns synth mode: 
        Sine, Square, Sawtooth ...
        """

        if not self.synth: return

        return self.synth.get_mode_list()
        

    #-------------------------------------------

    def get_key_base(self):
        """
        get the key base for octave number
        """

        return self._key_base

    #-------------------------------------------

    def change_key_base(self, step=1, adding=0):
        """
        change the key base for octave number
        """

        if not self.synth: return
        if adding:
            step += self._key_base
        if step >=24 and step <= 108:
            self._key_base = step

        msg = f"Kye Base: {self._key_base}"
        self._notify(msg)
    
    #-------------------------------------------

    def set_env_param(self, index, value):
        """
        sets envelope param value:
        """

        if not self.synth: return
        # adding 1 to index to avoid envelope stage off: 0
        index +=1
        self.synth.set_stage_value(index, value)
        
        val = self.synth.get_stage_value(index)
        msg = f"Param, value: {index: param}"
        self._notify(msg)

    #-------------------------------------------

    def change_param(self, index, val):
        """
        change param value by index
        """

        if not self.synth: return
        if index == 0:    
            self.synth.set_mode(val)
        elif index in [1, 2, 3, 4]:
            self.synth.set_stage_value(index, val)
        elif index == 5:
            self.synth.set_filter_mode(val)
        elif index == 6:
            self.synth.set_filter_cutoff(val)
        elif index == 7:
            # self.beep()
            self.synth.set_filter_resonance(val)
          
        val = self.synth.get_stage_value(index)
        msg = f"Index: {index}: value: {val}"
        self._notify(msg)

    #-------------------------------------------


#========================================

if __name__ == "__main__":
    iap = InterfaceApp()
    input("It's Ok...")
