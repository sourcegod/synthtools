#!/usr/bin/python3
"""
    File: streamplayer.py
    Streaming Audio player with SoundDevice module
    Date: Wed, 14/09/2022
    Author: Coolbrother
"""

import sounddevice as sd

class Player(object):
    """ Simple player """
    def __init__(self, device = (None, None)):
        self._rate = 44100
        self._channels =2
        self._buffer_size = 1024 # 512 for each channel

        if sd.query_devices(device=device[1]):
            sd.default.device = device
        else:
            sd.default.device = None # (None, 6)

        self._stream = sd.OutputStream(
            samplerate = self._rate,
            channels = self._channels,
            dtype = 'float32', # by default
            blocksize = self._buffer_size,
            clip_off = True,
            )

    #-------------------------------------------


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

    def start_stream(self):
        if self._stream:
            self._stream.start()

    #-------------------------------------------

    def stop_stream(self):
        if self._stream:
            self._stream.stop()

    #-------------------------------------------

    def write_data(self, data):
        if self._stream:
            self._stream.write(data)
            
    #-------------------------------------------

#========================================


if __name__ == "__main__":
    pl = Player()
    input("It's OK...")
