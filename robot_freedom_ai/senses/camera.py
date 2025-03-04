# -*- coding: utf-8 -*-
  
"""
Description: Interface to devices camera.
Author: HipMonsters.com 
License: MIT License
"""  
 
import time
import datetime   
from ._sense  import SenseBase


class Camera(object):

    def __init__(self, robot, nerves, config):
        """
        
        """
        self.os = config.OS
        self.robot = robot    
        self.config = config
        self.nerves = nerves

        if self.os == "LINUX":
           from picamera2 import Picamera2, Preview

        elif self.os == "OSX": 
         # from  AppKit import NSSpeechSynthesizer 
          #nssp = NSSpeechSynthesizer
          self.camera = None #nssp.alloc().init()  
          
    def video(self):

        if self.os == "LINUX":
            from picamera2 import Picamera2
            from picamera2.encoders import H264Encoder

            picam2 = Picamera2()
            video_config = picam2.create_video_configuration()
            picam2.configure(video_config)

            encoder = H264Encoder(10000000)
            time_srt =  datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            picam2.start_recording(encoder, self.config.OUTPUT_PATH + "video." + time_srt + ".h264")
            time.sleep(10)
            picam2.stop_recording()

    def capture(self ): 
        """
        
        """
        if self.os == "LINUX":
          
            from picamera2 import Picamera2, Preview
            picam = Picamera2()
            config = picam.create_preview_configuration()
            picam.configure(config)
            picam.start_preview(Preview.QTGL)

            picam.start()
            
            time.sleep(1)
            time_srt =  datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            picam.capture_file( self.config.OUTPUT_PATH + str(time_srt) + ".jpg")
            picam.close()  

        elif self.os == "OSX":
            self.camera.capture()

    
    def runAndWait(self): 
        """
        
        """
        if self.os == "linux":
           pass
        
        else: 
           
           while not self.voice_engine.isSpeaking():
               
                 time.sleep(.1)

           while self.voice_engine.isSpeaking():
               time.sleep(.1)




