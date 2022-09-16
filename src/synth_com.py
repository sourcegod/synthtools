#!/usr/bin/python3
"""
    File: synth_com.py
    Interactif shell for fastsynth module
    Date: Fri, 16/09/2022
    Author: Coolbrother
"""

from prompt_toolkit import prompt,print_formatted_text
from prompt_toolkit import prompt, PromptSession, patch_stdout
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter, PathCompleter
from os.path import expanduser
import interfaceapp as _iap

_session = PromptSession(history = FileHistory(expanduser('~/.synth_history')))

class SynthCom(object):
    """ FastSynth commandline manager """
    def __init__(self):
        self.iap = _iap.InterfaceApp()

    #-------------------------------------------

    def display(self, msg=""):
        if msg:
            print(msg)
        else:
            # beep
            print("\a")

    #-------------------------------------------

    def main(self):
        """
        Using Prompt Toolkit Module as Input
        """

        if self.iap is None: return
        iap = self.iap
        iap.init_app()

        while 1:
            val_str = _session.prompt("-> ")
            if val_str == "Q":
                iap.close_app()
                msg = "Bye Bye!"
                self.display(msg)
                break

            elif val_str == "p":
                iap.note_on()
            elif val_str == "s":
                iap.note_off()

            else:
                iap.beep()
    
#-------------------------------------------

#========================================


if __name__ == "__main__":
    app = SynthCom()
    app.main()
   
