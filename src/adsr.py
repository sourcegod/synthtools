#! /usr/bin/env python3
"""
    Test on audio enveloppe ADSR
    Date: Wed, 31/08/2022
    Author: Coolbrother
"""

from math import exp, log as logln
import numpy as np
import sounddevice as sd

def beep():
    print("\a")
#-----------------------------------------

class ADSR(object):
    def __init__(self, attack_time, decay_time, sustain_time, sustain_level, release_time):
        self.rate =  44100
        self.sustain_level = sustain_level
        self.attack_len = int(attack_time * self.rate)
        self.decay_len = int(self.attack_len + decay_time * self.rate)
        self.sustain_len = int(self.decay_len + sustain_time * self.rate)
        self.release_len = int(self.sustain_len + release_time * self.rate)
        self.curpos =0
        self.curlen =0

        """
        self.attack = np.linspace(0, 1, self.attack_len)
        self.decay = np.linspace(1, sustain_level, self.decay_len)
        self.sustain = np.full((self.sustain_length, ), sustain_level)
        self.release = np.linspace(sustain_level, 0, self.release_len)
        """

    #-----------------------------------------
    
    def process_data(self, wav_data, data_len):
        """
        process data
        """

        self.curpos =0
        curpos = self.curpos
        # attack stage
        if curpos >= 0 and curpos < self.attack_len:
            curlen = self.attack_len - curpos
            pos = curpos
            print(f"curpos at Attack Stage: {curpos}, curlen: {curlen}")
            for i in range(curlen):
                wav_data[pos + i] *=  (i / curlen)
                curpos +=1

        # decay stage
        if curpos >= self.attack_len and curpos < self.decay_len:
            curlen = self.decay_len - curpos
            pos = curpos
            print(f"curpos at Decay Stage: {curpos}, curlen: {curlen}")
            for i in range(curlen):
                val = 1 - (i / curlen) * (1 - self.sustain_level)
                wav_data[pos+i] *=  val 
                curpos +=1
            print(f"val: {val}")
         
        # Sustain Stage
        if curpos >= self.decay_len and curpos < self.sustain_len:
            curlen = self.sustain_len - curpos
            pos = curpos
            print(f"curpos at Sustain Stage: {curpos}, curlen: {curlen}")
            for i in range(curlen):
                val = self.sustain_level
                wav_data[pos + i] *=  val 
                curpos +=1
            print(f"val: {val}")

        # Release Stage
        if curpos >= self.sustain_len and curpos < data_len:
            curlen = data_len - curpos
            pos = curpos
            print(f"curpos at Release Stage: {curpos}, curlen: {curlen}, with data_len: {data_len}")
            for i in range(curlen):
                index = pos + i
                # val =  self.sustain_level - (i / curlen) * (1 - self.sustain_level)
                val =  self.sustain_level - (i / curlen) 
                # print(f"val0: {val}, with i: {i}, curlen: {curlen}")
                if val <0: val =0
                wav_data[index] *=  val 
                curpos +=1
            print(f"val: {val}")
  
        self.curpos = curpos

        """
        # else:
        curlen = data_len - curpos
        for i in range(curlen):
            wav_data[curpos+i] *= 0

        
        beep()
        """
        
        """
        for i in range(data_len):
            pos = i
            if pos >= 0 and pos <= self.attack_len:
                wav_data[i] *=  (pos / self.attack_len)
                if pos >= self.attack_len:
                    print(f"attack_len: {pos}")
                    print("\a") # beep
            elif pos >= self.attack_len and pos <= self.decay_len:
                wav_data[i] *= (1 -  self.sustain_level) / self.decay_len
                if pos >= self.decay_len:
                    print(f"decay_len: {pos}")
                    print("\a") # beep
                    return
            elif pos >= self.decay_len and pos <= self.sustain_len:
                wav_data[i] *= self.sustain_level
                if pos >= self.sustain_len:
                    print(f"sustain_len: {pos}")
                    print("\a") # beep
            elif pos >= self.sustain_len and pos <= self.release_len:
                wav_data[i] *= -(self.sustain_level - pos) / data_len
                # wav_data[i] *= 1 -  (pos / data_len)
                if pos >= self.release_len:
                    print(f"Release_len: {pos}")
                    print("\a") # beep
            elif pos >= self.release_len and pos <= data_len:
                wav_data[i] *=1 -  (pos / data_len)
                if pos >= data_len:
                    print(f"data_len: {pos}")
            pass
        """

    #-----------------------------------------

#========================================

class Player(object):
    """ Simple player """
    def __init__(self, device = (None, None)):
        if sd.query_devices(device=device[1]):
            sd.default.device = device
        else:
            sd.default.device = None # (None, 6)


    def get_samples(self, _len=1):
        freq = 440
        rate = 44100
        # length =1 # length samples
        nb_samples = int(_len * rate)
        # create an array
        x = np.arange(nb_samples)
        # the math function, is also the final sample
        y = np.sin(2 * np.pi * freq * x/rate) # in float only
        
        return y 

    #-------------------------------------------

    def play(self, samp):
        # samp = get_samples()
        sd.play(samp, blocking=True)

    #-------------------------------------------

    def stop(self):
        sd.stop()

    #-------------------------------------------

#========================================

class Fade(object):
    """ Fade manager """
    def __init__(self):
        pass

    #-------------------------------------------

    def fade_in_lin(self, wav_data, data_len, pos=0, vol=1):
        """
        Linear Fade In
        """
        
        len1 = data_len - pos
        curpos =0
        for i in range(data_len):
            if curpos >= len1: break
            if i >= pos:
                curpos = i - pos
                # if curpos == 0: print(f"Voici curpos: {curpos}")
                val = (curpos / len1) * vol
                wav_data[i] *= val 
        beep()

    #-------------------------------------------

    def fade_out_lin(self, wav_data, data_len, pos=0, vol=1):
        """
        Linear Fade Out
        """
        
        len1 = data_len - pos
        val =0
        for i in range(data_len):
            # if curpos >= data_len: break
            if i >= pos:
                curpos = i - pos
                # print(f"curpos: {curpos}, data_len: {len1}")
                # to block at a certain volume
                val = 1 - (curpos / len1) * (1 - vol)
                wav_data[i] *= val
        # print(f"val: {val:0.3f}")
        beep()

    #-------------------------------------------

    def fade_in_exp(self, wav_data, data_len, pos=0, vol=1):
        """
        Exponential Fade In
        Inspired from Zikforge 1.1
        """
        
        len1 = data_len - pos
        max_exp = 150.0 # 37767
        _const = logln(max_exp) / (len1 -1);

        curpos =0
        for i in range(data_len):
            if curpos >= len1: break
            if i >= pos:
                curpos = i - pos
                # if curpos == 0: print(f"Voici curpos: {curpos}")
                # val = ((curpos) / len1) # * vol
                val = ((max_exp - exp((len1 - curpos) * _const)) / max_exp)
                wav_data[i] *= val 
        print("\a")

    #-------------------------------------------

    def fade_out_exp(self, wav_data, data_len, pos=0, vol=1):
        """
        Exponential Fade Out
        Inspired from Zikforge 1.1
        """
        
        len1 = data_len - pos
        max_exp = 150.0 # 37767
        _const = logln(max_exp) / (len1 -1);

        curpos =0
        for i in range(data_len):
            if curpos >= len1: break
            if i >= pos:
                curpos = i - pos
                # if curpos == 0: print(f"Voici curpos: {curpos}")
                # val = ((curpos) / len1) # * vol
                val = (1.0 / exp(curpos * _const))
                wav_data[i] *= val 
        print("\a")
        """
        # Note: Fade Out Inverse Exponential:
        val = ((max_exp - exp(curpos * _const)) / max_exp)

        # Note: Fade In Inverse Exponential:
        val = ((max_exp - exp((len1 - curpos) * _const)) / max_exp)
        """


    #-------------------------------------------



#========================================

def main(samp):
    pl.play(samp)
    pl.stop()

#-------------------------------------------

if __name__ == "__main__":
    # print(f"device list: {sd.query_devices()}")
    _device = (None, 6) # second audio card
    pl = Player(device=_device)
    at_dur = 2
    dec_dur = 0.3
    sus_dur = 1
    sus_lev = 0.5
    rel_dur =3
    adsr = ADSR(at_dur, dec_dur, sus_dur, sus_lev, rel_dur)
    # adsr.process_data(wav_data, len(wav_data))
    fade = Fade()
    buf_data = pl.get_samples(5)


    while 1:
        wav_data = buf_data.copy()
        # wav_data = buf_data
        val_str = input("-> ")
        if val_str == "Q":
            print("Bye Bye!")
            print("\a")
            pl.stop()
            break

        elif val_str == "fil": # Fade In Linear
            fade.fade_in_lin(wav_data, len(wav_data), pos=88200, vol=0.3)
        elif val_str == "fol": # Fade Out Linear
            # print(f"len_data: {len(wav_data)}")
            fade.fade_out_lin(wav_data, len(wav_data), pos=88200, vol=0.3)
        elif val_str == "fie": # Fade In Exponential
            fade.fade_in_exp(wav_data, len(wav_data), pos=0, vol=1)
        elif val_str == "foe": # Fade Out Exponential
            fade.fade_out_exp(wav_data, len(wav_data), pos=0, vol=1)
        elif val_str == "ads": # Fade Out Exponential
            adsr.process_data(wav_data, len(buf_data))
            pass
        else:
            beep()
            continue

        pl.play(wav_data)



    # main(wav_data)

