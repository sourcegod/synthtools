#!/usr/bin/python3
"""
    File: synth_com.py
    Test for fastsynth module
    Date: Fri, 16/09/2022
    Author: Coolbrother
"""
import fastsynth as syn

from prompt_toolkit import prompt,print_formatted_text
from prompt_toolkit import prompt, PromptSession, patch_stdout
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter, PathCompleter
from os.path import expanduser

_session = PromptSession(history = FileHistory(expanduser('~/.synth_history')))

def _main0():
    """
    Deprecated function
    """

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

def main():
    """
    Using Prompt Toolkit Module as Input
    """

    synth = syn.FastSynth()
    synth.set_params(mode=5, muted=False) # mode 4: White Noise
    synth.start_engine()
    while 1:
        val_str = _session.prompt("-> ")
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
