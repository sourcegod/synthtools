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
        self.curmode = self.mode_lowpass
        self.buf0 = 0.0
        self.buf1 = 0.0
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
        
        self.feedback_amount = self.resonance + self.resonance / (1.0 - self.cutoff)

    #-------------------------------------------

    def process(self, input_value):
        """
        ### By Paul Kellett
        ### http://www.musicdsp.org/showone.php?id=29
        """

        # only for the cutooff
        # self.buf0 += self.cutoff * (input_value - self.buf0)
        
        # cutoff and resonance 
        self.buf0 += self.cutoff * (input_value - self.buf0 + self.feedback_amount * (self.buf0 - self.buf1))
        self.buf1 += self.cutoff * (self.buf0 - self.buf1)

        if self.curmode == self.mode_lowpass:
            return self.buf1
        elif self.curmode == self.mode_highpass:
            return input_value - self.buf0
        elif self.curmode == self.mode_bandpass:
            return self.buf0 - self.buf1;
        
        return 0.0

    #-------------------------------------------


#========================================


if __name__ == "__main__":
    input("It's OK...")
