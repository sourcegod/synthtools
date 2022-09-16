#!/usr/bin/python3
"""
    File: oscillator.py
    Inspired from Martin Finke Audio Plugins 
    Date: Wed, 14/09/2022
    Author: Coolbrother

"""

import math
from math import sin
from random import random, uniform as randuni


class Oscillator(object):
    def __init__(self):
        self._mode =0 # oscillator mode
        self._PI = math.pi
        self._twoPI = self._PI * 2
        self._freq = 440.0
        self._phase = 0.0
        self._sample_rate = 44100.0
        self._phase_inc = 0.0
        self._is_muted = True
        self._update_increment()

    #-------------------------------------------

    def _update_increment(self):
        self._phase_inc  = self._freq * self._twoPI / self._sample_rate

    #-------------------------------------------
    
    def set_mode(self, mode):
        self._mode = mode # oscillator's mode

    #-------------------------------------------

    def set_freq(self, freq):
        self._freq = freq
        self._update_increment()

    #-------------------------------------------

    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate
        self._update_increment()

    #-------------------------------------------

    def set_muted(self, muted):
        self._is_muted = muted

    #-------------------------------------------

    def generate(buffer, nb_frames):
        twoPI = self._twoPI
        if mode == 0: # sine oscillator
            for i in range(nb_frames):
                buffer[i] = sin(self._phase)
                self._phase += self._phase_inc  
                if self._phase >= twoPI:
                    self._phase -= twoPI

    #-------------------------------------------

    def next_sample(self):
        value = 0.0
        if self._is_muted: return value
        
        mode = self._mode
        PI = self._PI
        twoPI = self._twoPI
        if mode == 0: # sine osc
            value = sin(self._phase)
        
        elif mode == 1: # SAW osc
            value = 1.0 - (2.0 * self._phase / twoPI)

        elif mode == 2: # Square Osc
            if self._phase <= PI:
                value = 1.0
            else:
                value = -1.0
        elif mode == 3: # Triangle Osc
            value = -1.0 + (2.0 * self._phase / twoPI)
            value = 2.0 * (abs(value) - 0.5)
        
        elif mode == 4: # White Noise with uniform random 
            value = random() # randuni(-1, 1)
            return value

        elif mode == 5: # Pink Noise with uniform random 
            value = randuni(-1, 1)
            return value

        elif mode == 6: # Silence
            return value
           
        self._phase += self._phase_inc
        
        if self._phase >= twoPI:
            self._phase -= twoPI
        
        return value

    #-------------------------------------------

#========================================

if __name__ == "__main__":
    osc = Oscillator()
    osc.set_muted(False)
    samp_lst = []
    osc.set_mode(0) # Sine Osc
    for i in range(512):
        val = osc.next_sample()
        samp_lst.append(val)
    print(f"Last val: {val}")
    
    input("It's OK...")
#-------------------------------------------
