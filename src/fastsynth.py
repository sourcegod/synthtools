#!/usr/bin/python3
"""
    File: fastsynth.py
    Rapid Test for Synth
    Date: Fri, 16/09/2022
    Author: Coolbrother
"""

import time
import threading
import numpy as np
import oscillator as osc
import streamplayer as spl

def beep():
    print("\a")

#-------------------------------------------

class FastSynth(object):
    """ Fast synth to test oscillator """
    def __init__(self):
        self.pl = spl.Player()
        self.pl.start_stream()
        self.playing = False
        self._thr = None
        self._running = False
        self.osc = osc.Oscillator()
        self._proc_cback = self._proc_callback
        self.init_osc()

    #-------------------------------------------

    def init_osc(self):
        """
        init oscillators 
        """

        if self.osc:
            self.osc.set_muted(False)
            self.osc.set_mode(0) # Sine Osc 

    #-------------------------------------------

    def set_params(self, mode=0, muted=False):
        """
        change oscillators params
        """

        if self.osc:
            self.osc.set_mode(mode) 
            self.osc.set_muted(muted)

    #-------------------------------------------
         
    def _proc_callback(self):
        """
        The User Callback function must be called by the threading loop
        """

        # data shape must be correspond to the channel number
        data = np.zeros((512, 2), dtype='float32')
        if self.playing:
            for i in range(len(data)):
                val = self.osc.next_sample()
                data[i] = val
       
        return data

    #-------------------------------------------

    def _run_proc(self):
        """
        The Main Loop responsable to call the Callback User Function.
        """

        write_data = self.pl.write_data # for performance
        lock = threading.Lock()
        while 1:
            if not self._running:
                beep()
                break
            # for real threading function
            lock.acquire()
            data = self._proc_cback()
            lock.release()
            if data is None: break
          
            write_data(data)
       
    #-------------------------------------------

    def start_engine(self):
        """
        Running the main loop in thread
        """

        if self._proc_cback is None: return
        self._running = True
        self._thr = threading.Thread(target=self._run_proc).start()
        print("Starting Engine...""")

    #-------------------------------------------

    def stop_engine(self):
        self._running = False
        if self._thr:
            self._thr.join()
            self._thr = None
        print("Stopped Engine...""")

    #-------------------------------------------


    def note_on(self):
        self.playing = True
        print("Playing Note...")

    #-------------------------------------------

    def note_off(self):
        self.playing = False
        print("Stopping Note...")
    #-------------------------------------------


#========================================

def main():
    synth = FastSynth()
    synth.start_engine()
    while 1:
        val_str = input("-> ")
        if val_str == "Q":
            synth.stop_engine()
            print("Bye Bye!")
            beep()
            break
        elif val_str == "p":
            synth.note_on()
        elif val_str == "s":
            synth.note_off()

        else:
            beep()

#-------------------------------------------

if __name__ == "__main__":
    main()
    # input("It's OK...")
