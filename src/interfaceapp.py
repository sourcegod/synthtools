#!/usr/bin/env python3
"""
    File: interfaceapp.py
    Interface app for Fastsynth
    Date: Fri, 16/09/2022
    Author: Coolbrother
"""

import fastsynth as fsyn
import midutils as mid

class InterfaceApp(object):
    def __init__(self, parent=None):
        self._parent = parent
        self.synth = None
        self._key_base =60

    #-------------------------------------------
    
    def init_app(self):
        device_index = (6, 6) # (0, 0)
        channels =2
        mid_inport =1
        mid_outport =-1 # No Midi Out
        mid.start_midi_thread(mid_inport, mid_outport, func=self._midi_handler)
        self.synth = fsyn.FastSynth(device_index=device_index, channels=channels)
        self.synth.set_params(mode=0, muted=False) # mode 4: White Noise
        self.synth.start_engine()
        msg = "Init  App..."
        self._notify(msg)

    #-------------------------------------------

    def close_app(self):
        mid.stop_midi_thread()
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

    def param_change(self, param_index, index, val):
        """
        change param value by index
        """

        if not self.synth: return
        self.synth.param_change(param_index, index, val)

        msg = f"Index: {index}: value: {val}"
        self._notify(msg)

    #-------------------------------------------

    def _midi_handler(self, msg, inport=0, outport=0, printing=False):
        """ 
        Handling midi messages 
        from InterfaceApp
        """
        
        if msg:
            # print("\a") # beep
            m_type = msg.type
            if m_type in ['note_on', 'note_off']:
                m_note = msg.note
                m_vel = msg.velocity
                # Note off
                if m_type == "note_on" and m_vel == 0:
                    m_type = "note_off"
                    self.note_off(m_note, m_vel)
                    if printing:
                        print("Midi_in Message: ")
                        print(f"Note_off, Midi Number: {m_note}, Name: {mid.mid2note(m_note)}")
                        print(f"Details: {msg}")
                # Note on
                elif m_type == "note_on" and m_vel >0:
                    self.note_on(m_note, m_vel)
                    if printing:
                        print(f"Note_on, Midi Number: {m_note}, Name: {mid.mid2note(m_note)}")
                        freq = mid.mid2freq(m_note)
                        print(f"Freq: {freq:.2f}")
                        print(f"Details: {msg}")
            else: # others messages
                if printing:
                    print("Unknown message")
                    print(f"Details: {msg}")
            
            """
            if  self._midi_out:
                self._midi_out.send(msg)
                if printing: 
                    print("Midi_out message.")
            # beep
            if printing: 
                print("\a")
            """

    #-------------------------------------------

#========================================

if __name__ == "__main__":
    iap = InterfaceApp()
    iap.init_app()
    input("It's Ok...")
    iap.close_app()
