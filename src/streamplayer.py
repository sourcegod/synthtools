#!/usr/bin/python3
"""
    File: streamplayer.py
    Streaming Audio player with SoundDevice module
    Date: Wed, 14/09/2022
    Author: Coolbrother
"""
import numpy as np
import threading
import sounddevice as sd

class Player(object):
    """ Simple player """
    def __init__(self, device_index = (None, None), rate=44100, channels=1, debug=0):
        self._rate = rate
        self._channels = channels
        self._buffer_size = 1024 # 512 for each channel
        self._running = False
        self._audio_callback = None
        self._thr = None
        self._stream = None

        if debug:
            print(sd.query_devices())
        
        if sd.query_devices(device=device_index[1]):
            sd.default.device = device_index
            print("Query Device index is: ", sd.default.device)
        else:
            sd.default.device = None # (None, 6)
            print("Query Default Device index is: ", sd.default_device)

        try:
            self._stream = sd.OutputStream(
                samplerate = self._rate,
                channels = self._channels,
                dtype = 'float32', # by default
                blocksize = self._buffer_size,
                clip_off = True,
                )
        
        except sd.PortAudioError as err:
            sd.default.device = None # (None, 6)
            self._stream = sd.OutputStream(
                samplerate = self._rate,
                channels = self._channels,
                dtype = 'float32', # by default
                blocksize = self._buffer_size,
                clip_off = True,
                )
        
        except sd.PortAudioError as err:
            print("OutStream Error: ", err)
            return
        
        print("Final Device Index is: ", sd.default.device)

    #-------------------------------------------


    def get_samples(self, _len=1):
        freq = 440
        rate = 44100
        # length =1 # length samples
        nb_samples = int(_len * rate)
        # create an array
        x = np.arange(nb_samples)
        # the math function, is also the final sample
        y = np.sin(2 * np.pi * freq * x/rate, dtype='float32') # in float only
        
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
            print("Starting Stream...")

    #-------------------------------------------

    def stop_stream(self):
        if self._stream:
            self._stream.stop()
            print("Stopping Stream...")

    #-------------------------------------------

    def _run_proc(self):
        """
        The Main Loop responsable to call the Callback User Function.
        """

        write_data = self.write_data # for performance
        lock = threading.Lock()
        while 1:
            if not self._running:
                # beep()
                break
            # for real threading function
            lock.acquire()
            # data shape must be correspond to the channel number
            outdata = np.zeros((512, 2), dtype='float32')
            indata = outdata
            self._audio_callback(indata, outdata, len(outdata))
            lock.release()
            if outdata is None: break
          
            write_data(outdata)
       
    #-------------------------------------------


    def start_thread(self):
        """
        Running the main loop in thread
        """

        if self._audio_callback is None: return
        self._running = True
        self._thr = threading.Thread(target=self._run_proc).start()
        print("Start Threading...""")

    #-------------------------------------------

    def stop_thread(self):
        self._running = False
        if self._thr:
            self._thr.join()
            self._thr = None
        print("Stopped Threading...""")

    #-------------------------------------------


    def write_data(self, data):
        if self._stream:
            self._stream.write(data)
            
    #-------------------------------------------

#========================================


if __name__ == "__main__":
    device_index = [6, 6]
    pl = Player(device_index, channels=1)
    samp = pl.get_samples() # 1 sec length

    """
    pl.play(samp)
    pl.stop()
    """

    pl.start_stream()
    pl.write_data(samp)
    pl.stop_stream()

    input("It's OK...")
