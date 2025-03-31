# -*- coding: utf-8 -*-
  
"""
Description: This is a text to voice Daemon design to run on a RaspberryPi.
Author: HipMonsters.com 
Date Created: Jan 1, 2021
Date Modified: Oct 10, 2024
Version: 5.0
Platform: RaspberryPi
License: MIT License  
https://rhasspy.github.io/piper-samples/
"""

import platform
import time
import os
import json
import numpy as np
import pyaudio 
import settings


from piper.voice import PiperVoice  

#os.environ['SDL_AUDIODRIVER'] = 'dsp'

from nerves         import Nerves

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-d", "--devices", default="")  
 
 
class VoiceTest(object):

    def __init__(self, robot, devices , params =None, polling_rate =.15):
        """
        
        """ 
        self.os = settings.OS
       

        self.polling_rate = polling_rate
        self.robot     = robot
        self.devices  = devices
        self.nerves   =  Nerves(robot)  
        self.module   = "speak"

        with open(settings.DATA_PATH + self.robot + "/settings.json") as f:
           data = ''
           for row in f:
              data += row  
           data = json.loads(data)
        self.voice_params = data["voice"]
        #  voice = "english+f5" 
       # for key, val in params
        self.set_up(robot, self.voice_params) 


    def set_up(self,robot, params ):
        """
        
        """  
 
        self.robot = robot

        if params is not None:  
            self.voice_param  = params[self.os]
        else:
            self.voice_param  =  self.voice_params[self.os]
          

        if self.os == "LINUX":
             
            self.piper = True
            self.voise_epng = "english+f5"
            from piper.voice import PiperVoice  
            self.piper_model = settings.VOICES_PATH + params["LINUX"]["voice"] + ".onnx"   
            self.voice_engine = PiperVoice.load(self.piper_model) 

            try:
                from piper.voice import PiperVoice  
                self.piper_model = settings.VOICES_PATH + params["LINUX"]["voice"] + ".onnx"  
                self.voice_engine = PiperVoice.load(self.piper_model) 
      
            except Exception as e:

                print("Error loading piper!")
                print(str(e))
                t_error = open(settings.LOGS_PATH + "error.piper.log", "a")
                t_error.write(str(e))
                t_error.close()

                self.piper = False
                import espeakng  
                voice_engine = espeakng.Speaker()
                ## english+f5
                voice_engine.voice = "en"  
                voice_engine.pitch = params["LINUX"]["pitch"]
                voice_engine.wordgap = .5
                voice_engine.amplitude = 80
                voice_engine.wpm = 90
                self.voice_engine = voice_engine 
 
         
            
        elif self.os == "OSX":
           
          self.piper = False
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
  
           
           
    def speak(self, message ): 
        """
        
        """
        #print("Response: " + message)
        if self.os == "LINUX":

            if self.piper:
 
               # https://github.com/GDCorner/no-bs-llms/blob/main/article3/tts-piper-stream.py#L11
               # https://stackoverflow.com/questions/19230983/prevent-alsa-underruns-with-pyaudio
               # https://stackoverflow.com/questions/78642033/python-sounddevice-sound-is-played-way-to-fast-over-the-speaker
               # 16000
               
               p = pyaudio.PyAudio() 
               SAMPLE_BIT_DETH = pyaudio.paInt16
               
               self.stream = p.open(format=SAMPLE_BIT_DETH,
                                      channels=1,
                                      rate=self.voice_engine.config.sample_rate,
                                       output=True) 

               synthesize_args = {
                    "length_scale": 0.0,
                    "sentence_silence": 0.0,
               }
 
               message_audio_stream = self.voice_engine.synthesize_stream_raw(message,
                                                                   **synthesize_args)

               CHUNK_SIZE = 4096
               message_audio = bytearray()
               
               for audio_bytes in self.voice_engine.synthesize_stream_raw(message):
                  message_audio += audio_bytes
                  while len(message_audio) > CHUNK_SIZE:
                     latest_chunk = bytes(message_audio[:CHUNK_SIZE])
                     message_audio = message_audio[CHUNK_SIZE:]
                     self.stream.write(latest_chunk) 
                   
               self.stream.write(bytes(message_audio))
               self.stream.close()

            else: 
                self.voice_engine.say(message)  
            
        elif self.os == "OSX": 

            self.voice_engine.startSpeakingString_(message) 
    
    def wait(self): 
        """
        
        """
        if self.os == "LINUX":
            
            if self.piper:
                pass
            else:
                self.voice_engine.wait() 

        elif self.os == "OSX":
           
           i_cnt = 0
           while not self.voice_engine.isSpeaking():
               time.sleep(.1)
               i_cnt += 1
               if i_cnt > 100000:
                   break

           i_cnt = 0
           while self.voice_engine.isSpeaking(): 

                time.sleep(.1)
                i_cnt += 1
                if i_cnt > 100:
                    break

    
    def serve_forever(self): 
        """
        
        """ 
        import glob
        print("STARTING VOICE")
        print(" ")
        for voice_path in  glob.glob(settings.VOICES_PATH + "*.onnx") :
           
           print(voice_path)
           if self.piper:
               self.piper_model = voice_path 
               self.voice_engine = PiperVoice.load(self.piper_model)
               
           for i in range(10):
             for cmd  in ["Hello, how are you?", "I am doing OK", "Have a good day!"]:
               self.speak(cmd) 
               self.wait()
               time.sleep(.1) 
         
             name = input("Continue: ")
             if name in  ["no", ""]:
                 break

           print(" ")
           print(" ")
           time.sleep(self.polling_rate)

if __name__ == "__main__":
    """ 
    
    """ 

    voice  = VoiceTest("squirrel",  ('/dev/cu.usbmodem14201',"113") )
    voice.serve_forever()
