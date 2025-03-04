#!/usr/bin/env python
"""


"""

from  AppKit import NSSpeechSynthesizer
import time
import sys 
import os 

"""
python voice_test.py "lets watch tv" com.apple.speech.synthesis.voice.Bubbles 1 1

"""
#while true:
from cmd import Cmd
  

class VoiceTester(Cmd):
   
   def __init__(self): 
       super(VoiceTester, self).__init__()
       self.voice = "com.apple.speech.synthesis.voice.Bubbles"
       self.rate  = 1
       self.vol   = 1
       
   prompt = '> '
   intro = '\n'.join(['        Welcome To   ',
         '...Voice Tester...'])
   
   def do_set_voice(self, inp): 
       self.voice = inp

   def do_set_rate(self, inp):  
       self.rate  = float(inp) 

   def do_set_vol(self, inp):  
       self.vol   = float(inp)

   def do_exit(self, inp):
        print("Bye")
        return True
 
   def do_speak(self, inp): 
       nssp = NSSpeechSynthesizer
       ve = nssp.alloc().init()
       ve.setVoice_(self.voice) 
       ve.setRate_(self.rate)
       ve.setVolume_(self.vol)
       ve.startSpeakingString_(inp)

       while not ve.isSpeaking():
         time.sleep(0.1)

       while ve.isSpeaking():
          time.sleep(0.1)
        
 
VoiceTester().cmdloop()