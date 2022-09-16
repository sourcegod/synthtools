#!/usr/bin/python3
"""
    File: synth_com.py
    Test for fastsynth module
    Date: Fri, 16/09/2022
    Author: Coolbrother
"""
import fastsynth as syn

def main():
    synth = syn.FastSynth()
    synth.start_engine()
    while 1:
        val_str = input("-> ")
        if val_str == "Q":
            synth.stop_engine()
            print("Bye Bye!")
            syn.beep()
            break
        elif val_str == "p":
            synth.note_on()
        elif val_str == "s":
            synth.note_off()

        else:
            syn.beep()

#-------------------------------------------

if __name__ == "__main__":
    main()
    # input("It's OK...")
