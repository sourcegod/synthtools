#!/usr/bin/env python3
"""
    IIR Filter resonance Cutoff implementation in python
    from Martin Finke blog Audio Plugins Part 13
    Date: Wed, 28/09/2022
    Author: Coolbrother
"""

class Filter(object):
    def __init__(self):
        self.mode_lowpass =0
        self.mode_highpass =1
        self.mode_bandpass =2
        self.mode_count =3
        self.cutoff = 0.99
        self.resonance = 0.0
        self.cutoff_mode = 0.0
        self.curmode = self.mode_lowpass
        self.buf0 = 0.0
        self.buf1 = 0.0
        self.buf2 = 0.0
        self.buf3 = 0.0
        self.feedback_amount =0.0
        self.calculate_feedback()

    #-------------------------------------------

    def new_cutoff(self, new_cutoff):
        """
        inline function 
        """

        self.cutoff = new_cutoff
        self.calculate_feedback()

    #-------------------------------------------

    def new_resonance(self, new_resonance):
        """
        inline function 
        """

        self.resonance = new_resonance
        self.calculate_feedback()

    #-------------------------------------------
    def set_cutoffmode(self, new_cutoffmode):
        """
        inline function 
        """

        self.cutoff_mode = new_cutoffmode
        self.calculate_feedback()

    #-------------------------------------------


    def set_filter_mode(self, mode):
        """
        inline function 
        """
        
        self.curmode = mode

    #-------------------------------------------

    def calculate_feedback(self):
        """
        inline function
        """
        
        self.feedback_amount = self.resonance + self.resonance / (1.0 - self.get_calculcutoff())

    #-------------------------------------------

    def get_calculcutoff(self):
        """
        inline function
        """

        return max(min(self.cutoff + self.cutoff_mode, 0.99), 0.01)
    #-------------------------------------------


    def process(self, input_value):
        """
        ### By Paul Kellett
        ### http://www.musicdsp.org/showone.php?id=29
        """

        if input_value == 0.0: return input_value
        calcul_cutoff = self.get_calculcutoff()
        self.buf0 += calcul_cutoff * (input_value - self.buf0 + self.feedback_amount * (self.buf0 - self.buf1))
        self.buf1 += calcul_cutoff * (self.buf0 - self.buf1)
        self.buf2 += calcul_cutoff * (self.buf1 - self.buf2)
        self.buf3 += calcul_cutoff * (self.buf2 - self.buf3)

        """
        # only for the cutooff
        # self.buf0 += self.cutoff * (input_value - self.buf0)
        
        # for test
        # self.buf0 += self.cutoff * (input_value)
        
        # cutoff and resonance 
        self.buf0 += self.cutoff * (input_value - self.buf0 + self.feedback_amount * (self.buf0 - self.buf1))
        self.buf1 += self.cutoff * (self.buf0 - self.buf1)

        # From -12dB to -24dB
        # getting an attenuation of -24dB per octave. Add the following two lines
        self.buf2 += self.cutoff * (self.buf1 - self.buf2)
        self.buf3 += self.cutoff * (self.buf2 - self.buf3)
        """


        if self.curmode == self.mode_lowpass:
            # return self.buf0
            # return self.buf1
            return self.buf3
        elif self.curmode == self.mode_highpass:
            return input_value - self.buf3
        elif self.curmode == self.mode_bandpass:
            return self.buf0 - self.buf3
        
        return 0.0

    #-------------------------------------------


#========================================


if __name__ == "__main__":
    input("It's OK...")
