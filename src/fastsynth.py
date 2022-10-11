#!/usr/bin/python3
"""
    File: fastsynth.py
    Rapid Test for Synth
    Date: Fri, 16/09/2022
    Author: Coolbrother
"""
from math import pow
import time
import numpy as np
import oscillator as osc
import streamplayer as spl
import envelopegenerator as env
import filter as fil
import midutils as mid
# get freq by index in a list, more rapid than calculate the freq
mid2freq = mid.mid2freq_index

def beep():
    print("\a")

#-------------------------------------------

# """
def _mid2freq(note):
    ### Deprecated function
    return 440.0 * pow(2, (note - 69) / 12.0)

#-------------------------------------------
# """

class TMessage(object):
    def __init__(self, note=0, vel=0):
        self.note = note
        self.vel = vel
    
#-------------------------------------------
#========================================

class TParam(object):
    """ param values """
    volume =0
    waveform =1
    env_mode =2
    env_param =3
    filter_mode =4
    cutoff =5
    resonance =6
    filter_envmod =7 # Filter Env Modulation
    filter_envparam =8
    filter_envamount =9

#-------------------------------------------
#========================================


class FastSynth(object):
    """ Fast synth to test oscillator """
    def __init__(self, device_index=(None, None), channels=2):
        # device_index = (6, 6)
        # device_index = (0, 0)
        self.pl = spl.Player(device_index=device_index, channels=channels)
        self.pl._audio_callback = self._audio_callback
        self.pl.start_stream()
        self.playing = False
        self.volume = 1.0
        self.osc = None
        self.envgen = env.EnvelopeGenerator()
        # Filter Envelope to modulate cutoff frequency
        self.filter_env = env.EnvelopeGenerator()
        self.filter_env_amount = 0.0
        self.filter = fil.Filter()

        # LFO oscillator
        self.LFO = None
        # how much the LFO will modulate the filter's cutoff frequency
        self.lfo_filtermod_amount = 0.1
        self.init_osc()
        self._last_note = TMessage()

    #-------------------------------------------

    def init_osc(self):
        """
        init oscillators 
        """

        if self.osc is None:
            # only one instance
            self.osc = osc.Oscillator()
            self.osc.set_muted(False)
            self.osc.set_mode(0) # Sine Osc 
        if self.LFO is None:
            # only one instance
            self.LFO = osc.Oscillator()
            self.LFO.set_mode(3) # Triangle Osc 
            self.LFO.set_freq(6.0)
            self.LFO.set_muted(False)

    #-------------------------------------------

    def set_volume(self, volume):
        if volume >=0.0 and volume <= 1.0:
            self.volume = volume

    #-------------------------------------------

    def set_params(self, mode=0, muted=False):
        """
        change oscillators params
        """

        if not self.osc: return
        
        self.osc.set_mode(mode) 
        self.osc.set_muted(muted)

    #-------------------------------------------

    def get_oscmode(self):
        if not self.osc: return

        return self.osc._mode

    #-------------------------------------------

    def set_oscmode(self, mode):
        """
        sets oscillator mode 
        """

        if not self.osc: return

        if mode >=0 and mode <= self.osc._max_mode:
            self.osc._mode = mode

    #-------------------------------------------

    def get_mode_list(self):
        if not self.osc: return

        return self.osc._mode_lst

    #-------------------------------------------


    def _audio_callback(self, indata, outdata, nb_frames):
        """
        Note: this function is equivalent of ProcessDoubleReplacing function in the Martin Finke Audio Plugins Tutorial.
        The User Callback function must be called by the threading loop
        """

        # for performance without lookup rattribute
        envgen_nextsample = self.envgen.next_sample
        filter_process = self.filter.process
        osc_nextsample = self.osc.next_sample
        volume = self.volume
        filter_set_cutoffmod = self.filter.set_cutoffmode
        filter_env_nextsample = self.filter_env.next_sample
        # Filter Envelope Amount must be vary between -1.0 to 1.0
        filter_env_amount = self.filter_env_amount
        lfo_nextsample = self.LFO.next_sample
        lfo_filtermod_amount = self.lfo_filtermod_amount
        if self.playing:
            for i in range(nb_frames):
                # Calculate LFO Filter Modulation with a value between -1 and 1.0
                lfo_filtermod = lfo_nextsample() * lfo_filtermod_amount
                # the Cutoff will be modulated by both the Filter's envelope and the LFO
                filter_set_cutoffmod((
                    filter_env_nextsample() * filter_env_amount)\
                    + lfo_filtermod
                        ) 
                val = filter_process( 
                    osc_nextsample() * envgen_nextsample() * volume
                        )
                outdata[i] = val
        
        return outdata

    #-------------------------------------------

    def start_engine(self):
        """
        Running the main loop in thread
        """

        self.pl.start_thread()
        print("Starting Engine...""")

    #-------------------------------------------

    def stop_engine(self):
        self.pl.stop_thread()
        print("Stopped Engine...""")

    #-------------------------------------------

    def get_stage_value(self, index):
        """
        Returns the envelope stage value by index
        """
        
        return  self.envgen.get_stage_value(index)

    #-------------------------------------------

    def set_stage_value(self, index, val):
        """
        Sets the envelope stage value by index
        """
        
        self.envgen.set_stage_value(index, val)

    #-------------------------------------------

    def set_filter_mode(self, mode):
        """
        sets filter mode 
        """

        if not self.filter: return
        self.filter.set_filter_mode(mode)

    #-------------------------------------------

    def set_filter_cutoff(self, val):
        """
        sets filter cutoff
        """

        if not self.filter: return
        self.filter.new_cutoff(val)

    #-------------------------------------------

    def set_filter_resonance(self, val):
        """
        sets filter resonance
        """

        if not self.filter: return
        self.filter.new_resonance(val)

    #-------------------------------------------
   
    def param_change(self, param_index, index, val):
        """
        change synth param by index
        """
        
        # print(f"param_index: {param_index}, index: {index}, val: {val}")
        if param_index == TParam.volume:
            self.set_volume(val)
        elif param_index == TParam.waveform:
            self.set_oscmode(val)
        elif param_index == TParam.env_mode:
            pass # no action
        elif param_index == TParam.env_param:
            # change value stage for envelope 1
            self.set_stage_value(index+1, val)
        elif param_index == TParam.filter_mode:
            self.set_filter_mode(val)
        elif param_index == TParam.cutoff:
            self.set_filter_cutoff(val)
        elif param_index == TParam.resonance:
            self.set_filter_resonance(val)
        elif param_index == TParam.filter_envmod:
            pass # No action
        elif param_index == TParam.filter_envparam:
            # change value stage for filter envelope  2
            self.filter_env.set_stage_value(index+1, val)
        elif param_index == TParam.filter_envamount:
            self.filter_env_amount = val

    #-------------------------------------------

    def note_on(self, note=60, vel=127):
        
        """
        if self._last_note.note != note:
            print("Playing Note: ", note)
        """

        if self._last_note.vel == 0:
            self._last_note.note = note
            self._last_note.vel = vel
            freq = mid2freq(note)
            self.osc.set_freq(freq)
            self.envgen.enter_stage(self.envgen._stage_attack) # Attack stage
            self.filter_env.enter_stage(self.envgen._stage_attack) # Attack stage
        self.playing = True
        # print("Playing Note...")

    #-------------------------------------------

    def note_off(self, note=60, vel=0):
        
        """
        if self._last_note.note != note:
            print("Stopping Note: ", note)
        """

        self._last_note.note = note
        self._last_note.vel = vel
        self.envgen.enter_stage(self.envgen._stage_release) # Release stage
        self.filter_env.enter_stage(self.envgen._stage_release)
        
        # self.playing = False
        # print("Stopping Note...")
    #-------------------------------------------

#========================================

def main():
    device_index = (6, 6)
    synth = FastSynth(device_index)
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
