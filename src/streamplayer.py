#!/usr/bin/python3
"""
    File: streamplayer.py
    Streaming Audio player with SoundDevice module
    Date: Wed, 14/09/2022
    Author: Coolbrother
"""
import threading
import sounddevice as sd

class Player(object):
    """ Simple player """
    def __init__(self, device_index = (None, None)):
        self._rate = 44100
        self._channels =2
        self._buffer_size = 1024 # 512 for each channel
        self._running = False
        self._audio_callback = None
        self._thr = None

        print(sd.query_devices())
        if sd.query_devices(device=device_index[1]):
            sd.default.device = device_index
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
            data = self._audio_callback()
            lock.release()
            if data is None: break
          
            write_data(data)
       
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
    pl = Player()
    input("It's OK...")
