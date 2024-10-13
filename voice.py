# -*- coding: utf-8 -*-
  
"""
Description: This is a text to voice Daemon design to run on a RaspberryPi.
Author: HipMonsters.com 
Date Created: Jan 1, 2021
Date Modified: Oct 10, 2024
Version: 5.0
Plaftorm: RaspberryPi
License: MIT License  
"""

import platform
import time
import os
import json


from nerves         import Nerves

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-d", "--devices", default="")  
 
 
class Voice(object):

    def __init__(self, robot, devices , params =None, polling_rate =.25):
        """
        
        """ 
        self.os = "LINUX"
        if platform.system() == 'Windows':
          self.os = "WIN"
        elif platform.system() == 'Darwin': 
          self.os = "OSX" 
       
        self.polling_rate = polling_rate
        self.name     = robot
        self.devices  = devices
        self.nerves   =  Nerves(robot)  
        self.module   = "speak"

        with open("./data/" + self.name + "/settings.json") as f:
           data = ''
           for row in f:
              data += row  
           data = json.loads(data)
        self.voice_params = data["voice"]
        self.set_up(robot, params) 

    def set_up(self,robot, params ):
        """
        
        """  
 
        self.robot = robot
        if params is not None:  
            self.voice_param  = params[self.os]
        else:
            self.voice_param  =  self.voice_params[self.os]
        

        if self.os == "LINUX":
            
            import espeakng 
      #     self.voice_engine.setProperty('voice',  self.voice_param["voice"])
      #     self.voice_engine.setProperty('rate' ,  self.voice_param["rate"]) 
      #     self.voice_engine.setProperty('pitch',  self.voice_param["pitch"])
      #     self.voice_engine.setProperty('volume', self.voice_param["volume"]) 
           
            voice_engine = espeakng.Speaker()
            voice_engine.voice = "en"  
            voice_engine.pitch =90
            voice_engine.wordgap = .5
            voice_engine.amplitude = 80
            voice_engine.wpm = 90
            self.voice_engine = voice_engine 
            
        elif self.os == "OSX":
           
          from  AppKit import NSSpeechSynthesizer 
          nssp = NSSpeechSynthesizer
          self.voice_engine = nssp.alloc().init() 

          if len(self.voice_param ) > 0:
              self.voice_engine.setVoice_(self.voice_param["voice"])
              self.voice_engine.setRate_(self.voice_param["rate"]) 
              self.voice_engine.setVolume_(self.voice_param["volume"])
               
        self.speak("Voice is active")
        self.wait()
        
         
    def switch_robot(self, robot):
        """
        
        """  
        self.set_up(robot)
        self._switch_speaker(robot)

    def _switch_speaker(self, robot, speaker_config):
        """
        
        """  

        if self.os == "OSX": 
            os.system("SwitchAudioSource -i " + self.devices[robot][1])
            # os.system("SwitchAudioSource -u " + robots[robot][1])
            time.sleep(.1) 
  
           
           
    def speak(self, message): 
        """
        
        """
        print("Response: " + message)
        if self.os == "LINUX":
            self.voice_engine.say(message)  
            
        elif self.os == "OSX": 

            self.voice_engine.startSpeakingString_(message) 
    
    def wait(self): 
        """
        
        """
        if self.os == "LINUX":
            
           self.voice_engine.wait()

        elif self.os == "OSX":
           
           i_cnt = 0
           while not self.voice_engine.isSpeaking():
               time.sleep(0.1)
               i_cnt += 1
               if i_cnt > 100:
                   break

           i_cnt = 0
           while self.voice_engine.isSpeaking():
                time.sleep(0.1)
                i_cnt += 1
                if i_cnt > 100:
                    break

    
    def serve_forever(self): 
        """
        
        """
        b_flip = True

        while True:
           
           if b_flip:
               print("\r listing | ", end = "")
               b_flip = False
           else:
               print("\r listing - ", end = "")
               b_flip = True
           new, cmds = self.nerves.pop(self.module) 
           if new:
               acmds = cmds.split(";") 
               
               if acmds[0] == "speak":
                   self.speak(acmds[2])
    
               if acmds[1] == "wait":
                   self.wait()  

               self.nerves.set(self.module, "") 
     
           time.sleep(self.polling_rate)

if __name__ == "__main__":
    """
    python3 voice.py -m serve -r number_3 
    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot   


    voice  = Voice(robot,  ('/dev/cu.usbmodem14201',"113") )
    if mode == "serve":
     
        voice.serve_forever()
