# -*- coding: utf-8 -*-
  
"""
Description: This is a text to voice Daemon design to run on a RaspberryPi.
Author: HipMonsters.com 
Date Created: Jan 1, 2021
Date Modified: Oct 10, 2024
Version: 5.0
Platform: RaspberryPi
License: MIT License   
""" 
from os import system
import time
import os 
import json
import numpy as np  
import subprocess 
import pyaudio   
 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot")  
 
 
class Voice(object):

    def __init__(self, robot, nerves, config, settings, polling_rate =.05):
        """
        
        """ 
        self.os = config.OS  
        self.robot    = robot  
        self.nerves   = nerves  
        self.settings = settings  
        self.config   = config    
        self.polling_rate = polling_rate
        self.robot     = robot
        self.devices  = {}  
        self.module   = "speak"
        self.log      = True 

        with open(self.config.DATA_PATH + self.robot + "/settings.json") as f:
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
             
            self.piper  = False
            self.espeak = False
            self.voise_epng = "english+f5"

            try:
                from piper.voice import PiperVoice  
                self.piper_model =  self.config.VOICES_PATH + params["LINUX"]["voice"] + ".onnx" 
                self.voice_engine = PiperVoice.load(self.piper_model) 
                self.piper = True
      
            except Exception as e: 
                print("Piper ERROR")
                t_error = open(self.config.LOGS_PATH +  "error.piper.log", "a")
                t_error.write(str(e))
                t_error.close() 
                self.piper = False

            if   self.piper == False:
                try:
                    import espeakng  
                    voice_engine = espeakng.Speaker()
                    ## english+f5
                    voice_engine.voice = "en"  
                    voice_engine.pitch = params["LINUX"]["pitch"]
                    voice_engine.wordgap = .5
                    voice_engine.amplitude = 80
                    voice_engine.wpm = 90
                    self.voice_engine = voice_engine 
                    self.espeak = True
                except:
                    print("ESpeak ERROR")
            
        elif self.os == "OSX": 
            self.voice_engine = None
            #from  AppKit import NSSpeechSynthesizer 
            #nssp = NSSpeechSynthesizer
            #self.voice_engine = nssp.alloc().init()  
            #if len(self.voice_param ) > 0:
            #    self.voice_engine.setVoice_(self.voice_param["voice"])
            #    self.voice_engine.setRate_(self.voice_param["rate"]) 
            #    self.voice_engine.setVolume_(self.voice_param["volume"])
               
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
            time.sleep(.1)
  
           
           
    def speak(self, message ): 
        """
        
        """
        message =  message.replace("`", "") 
        message =  message.replace("'", "").replace('"', "")
        message =  message.replace("[", "").replace("]", "")
        message =  message.replace("<", "").replace(">", "") 
        message =  message.replace("(", "").replace(")", "") 
        message =  message.replace("@", "").replace("%", "") 
        message =  message.replace("~", "").replace(":", "") 

        if self.os == "LINUX":

            if self.piper:
                
               #os.system("echo '" + message + "' | piper --model " + self.piper_model + " --output-raw | aplay -r 22050 -f S16_LE -t raw -")
    
               p = pyaudio.PyAudio() 
               SAMPLE_BIT_DETH = pyaudio.paInt16 
               rate_reduction = 1
               rate = int(rate_reduction*self.voice_engine.config.sample_rate)
               
               self.stream = p.open(format=SAMPLE_BIT_DETH,
                                      channels=1,
                                      rate=rate,
                                      output=True) 
               
               synthesize_args = {
                    "length_scale": 0.0,
                    "sentence_silence": 0.0,
               }
               """" 
               message_audio_stream = self.voice_engine.synthesize_stream_raw(message,
                                                                   **synthesize_args)
                
               latest_chunk = bytes(message_audio_stream)
               ##if  latest_chunk > 2048:
               self.stream.write(latest_chunk) 
               else:
               """ 
               if 1 == 1:
                   
                   CHUNK_SIZE =  512 #1024 #2048   # 4096
                   message_audio = bytearray()
    
                   SILENCE = chr(0)*CHUNK_SIZE*1*2 
    
                   for audio_bytes in self.voice_engine.synthesize_stream_raw(message):
                   #for audio_bytes in message_audio_stream:
                      message_audio += audio_bytes
                      while len(message_audio) > CHUNK_SIZE:
                         latest_chunk = bytes(message_audio[:CHUNK_SIZE])
                         message_audio = message_audio[CHUNK_SIZE:]
                         self.stream.write(latest_chunk) 
                         #time.sleep(.01) 
                         
                   self.stream.write(bytes(message_audio)) 
                   '''
                   free = self.stream.get_write_available()
                   if free > CHUNK_SIZE :
                        tofill = free - CHUNK_SIZE
                        SILENCE = chr(0)*1*2 
                        self.stream.write(SILENCE * tofill)
                   '''
                   if self.log:
                      f_log = open(self.config.LOGS_PATH + "error.piper.log", "a")
                      f_log.write("### message       #####\n")
                      f_log.write(str(message) + "\n")  
               self.stream.close()
               p.terminate()

            elif self.espeak: 
                self.voice_engine.say(message)  

            
        elif self.os == "OSX": 
            try:
                message = message.replace("'", "")
                message = message.replace("`", "")
                message = message.replace('"', "")
                message = message.strip()
               # system('say "' + message + "'")

                outfile = open( "none" , "w")
                subp = subprocess.Popen("say " + message ,  
                                        stdout=outfile ,
                                        shell=True)
            except Exception as e :
                print("OSX SPEAK ERROR")
                print(str(e))
            #self.voice_engine.startSpeakingString_(message) 
            # self.voice_engine.startSpeaking(message) 
    
    def wait(self): 
        """
        
        """
        if self.os == "LINUX":
            
            if self.piper:
                pass
            else:
                self.voice_engine.wait() 

        elif self.os == "OSX":
           
           if self.voice_engine == None:
               pass
           else:
               i_cnt = 0
               while not self.voice_engine.isSpeaking():
                   i_cnt += 1
                   if i_cnt > 1200:
                       break
                   time.sleep(.1)
 
    
    def serve_forever(self): 
        """
        
        """
        b_flip = True

        while True:
           
           if b_flip:
             #  print("\r listing | ", end = "")
               b_flip = False
           else:
              # print("\r listing - ", end = "")
               b_flip = True
           new, cmds = self.nerves.pop(self.module) 
           if new:
               acmds = cmds.split(";")  
               if len(acmds) < 2:
                   continue 
                   
               if  acmds[0] == "speak" and acmds[2] == "":
                   continue 

               if acmds[0] == "speak-w":
                   
                   found, val = self.nerves.pop("spoke" ) 
                   self.speak(acmds[2])  
                   self.wait()     
                   self.nerves.set("spoke", "Done")   

               elif acmds[0] == "speak":
                     
                   self.speak(acmds[2])  
 

           time.sleep(self.polling_rate)

if __name__ == "__main__":
    """ 
    
    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot   


    voice  = Voice(robot,  ('/dev/cu.usbmodem14201',"113") )
    if mode == "serve":
     
        voice.serve_forever()
