#!/usr/bin/env python3
"""
    Implementation for Enveloppe Generator or ADSR
    inspired from Martin Finke Enveloppe Generator in Audio Plugins Part 11
    Date: Sat, 10/09/2022
    Coolbrother
"""

import math
from math import log as log_ln
from enum import Enum

### Enumeration klass with autonumber
EnvStage = Enum('EnvStage', [
            'OFF', 'ATTACK', 'DECAY',
            'SUSTAIN', 'RELEASE', 'STAGE_COUNT'
            ], start=0)


class EnvelopeGenerator(object):
    """ ADSR manager """
    def __init__(self):
        self._stage_off =0
        self._stage_attack =1
        self._stage_decay =2
        self._stage_sustain =3
        self._stage_release =4
        self._stage_count =5
        self._curstage = self._stage_off
        self._min_level =0.0001 # minimum level
        self._curlevel = self._min_level
        self._multiplier = 1.0
        self._sample_rate = 44100.0
        self._cursample_index =0
        self._nextstage_index =0
        self._stage_lst = [0] * self._stage_count
        self._stage_lst[self._stage_off] = 0.0
        self._stage_lst[self._stage_attack] = 0.01
        self._stage_lst[self._stage_decay] = 1
        self._stage_lst[self._stage_sustain] = 0.1
        self._stage_lst[self._stage_release] = 2

    #-------------------------------------------

    def enter_stage(self, new_stage):
        self._curstage = new_stage;
        self._cursample_index = 0;
        if (self._curstage == self._stage_off or\
                self._curstage == self._stage_sustain):
            self._nexttage_index = 0;
        else:
            self._nextstage_index = self._stage_lst[self._curstage] * self._sample_rate;
        
        # switch on new stage
        if new_stage == self._stage_off:
            self._curlevel = 0.0
            self._multiplier = 1.0
        elif new_stage == self._stage_attack:
            self._curlevel = self._min_level;
            self.calculate_multiplier(self._curlevel,
                                    1.0,
                                    self._nextstage_index)
            
        elif new_stage == self._stage_decay:
                self._curlevel = 1.0
                self.calculate_multiplier(self._curlevel,
                                    max(self._stage_lst[self._stage_sustain], self._min_level),
                                    self._nextstage_index)
            
        elif new_stage == self._stage_sustain:
            self._curlevel = self._stage_lst[self._stage_sustain]
            self._multiplier = 1.0

        elif new_stage == self._stage_release:
            ### We could go from ATTACK/DECAY to RELEASE,
            ### so we're not changing currentLevel here.
            self.calculate_multiplier(self._curlevel,
                    self._min_level,
                    self._nextstage_index)
          
    #-------------------------------------------

    def set_samplerate(self, sample_rate):
        self._sample_rate = sample_rate

    #-------------------------------------------

    def get_stage(self):
        return self._curstage

    #-------------------------------------------

    def next_sample(self):
        ### whether curstage is not in stage OFF and not in SUSTAIN stage
        if (self._curstage != self._stage_off and\
                self._curstage != self._stage_sustain):
            if (self._cursample_index == self._nextstage_index):
                new_stage = (self._curstage + 1) % self._stage_count
                self.enter_stage(new_stage)

            self._curlevel *= self._multiplier
            self._cursample_index +=1
    
        return self._curlevel

    #-------------------------------------------

    def calculate_multiplier(self, start_level, end_level, len_samples):
        """
        Note: it's more naturel to calculate sound variation in exponential way instead linear.
        """

        # TODO: manage Value Error with math domain when logln is zero
        try:
            self._multiplier = 1.0 + (log_ln(end_level) - log_ln(start_level)) / (len_samples)
        except ValueError:
            pass


    #-------------------------------------------

#========================================
envgen = EnvelopeGenerator()
_note_status = False

def note_on(note_num, vel):
    global _note_status
    envgen.enter_stage(envgen._stage_attack)
    _note_status = True

#-------------------------------------------

def note_off(note_num, vel):
    global _note_status
    envgen.enter_stage(envgen._stage_release)
    _note_status = False

#-------------------------------------------

def test():
    old_stage = None
    for i in range(44100):
        stage = envgen.get_stage()
        val = envgen.next_sample()
        if stage != old_stage:
            old_stage = stage
            print(f"stage: {stage}, with i, val: {i, val}")
        if i >= 441 and i <= 33075 and _note_status == False:
            note_on(note_num=0, vel=1)
        elif i >= 33075 and _note_status == True:
            note_off(note_num=0, vel=0)


    stage = envgen.get_stage()
    val = envgen.next_sample()
    print(f"Finished with stage: {stage}, with i, val: {i, val}")

#-------------------------------------------


if __name__ == "__main__":
    test()
    print(f"envstage.OFF: {EnvStage.OFF.value}")
    print(f"envstage.SUSTAIN: {EnvStage.SUSTAIN.value}")

    input("It's Cool...")
