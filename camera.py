# -*- coding: utf-8 -*-
  
"""
Description: Interface to devices camera.
Author: HipMonsters.com 
License: MIT License
"""  

import platform
import time

 
from nerves         import Nerves 

class Camera(object):

    def __init__(self, name):
        """
        
        """
        self.os = "LINUX"
        if platform.system() == 'Windows':
          self.os = "WIN"
        elif platform.system() == 'Darwin': 
          self.os = "OSX"
  
        self.name = name    
        self.nerves = Nerves(self.name)

        if self.os == "LINUX":
           from picamera2 import Picamera2, Preview

        elif self.os == "OSX": 
          from  AppKit import NSSpeechSynthesizer 
          nssp = NSSpeechSynthesizer
          self.voice_engine = nssp.alloc().init() 
         # self.voice_engine.setVoice_(voice)
         # self.voice_engine.setRate_(rate)
           
    def capture(self, message, history): 
        """
        
        """
        if self.os == "LINUX":
          
  
            picam = Picamera2()
            config = picam.create_preview_configuration()
            picam.configure(config)
            picam.start_preview(Preview.QTGL)

            picam.start()
            time.sleep(1)
            time_srt =  datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

            picam.capture_file("/home/dragon/Desktop/raspberry_pi/movement." + str(time_srt) + ".jpg")

            picam.close()
            self.voice_engine.say(message)  

        elif self.os == "LINUX":
            self.voice_engine.startSpeakingString_(message) 
    
    def runAndWait(self): 
        """
        
        """
        if OSS == "linux":
           pass
        else: 
           while not self.voice_engine.isSpeaking():
               time.sleep(0.1)

           while self.voice_engine.isSpeaking():
                time.sleep(0.1)




