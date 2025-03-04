# -*- coding: utf-8 -*-
"""
Description: Sensor daemon for speech.
Author: HipMonsters.com 
License: MIT License
"""
import json  
import time 

from pocketsphinx import LiveSpeech
import speech_recognition as sr  

from ._sense  import SenseBase

import argparse
parser = argparse.ArgumentParser() 
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-a", "--args", default="")  


class   Speech(SenseBase):

    def __init__(self, robot, nerves, config, settings, pins ={}):
        """
        
        """
        super().__init__(robot, nerves, config, settings,"speech")
             
        self.pins         = pins  
        self.last_message = -1
        self.b_adjusted   = False 
        self.recognizer   = sr.Recognizer() 
        self.polling_rate = .05  
        
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("\rMicrophone with name \"{1}\" found for         `Microphone(device_index={0})`".format(index, name), end="")
  
    def poll_and_wait(self, phrase):
        """
        """
        print("\rListening!                                      ",   end="")
       # file = "message.wav"
       # self.play_sound(file)
           
        speech = LiveSpeech(keyphrase= phrase, 
                            kws_threshold=1e-20)
          
        if speech is None:
             return False
             
        for phrase in speech:
             return True
            
        return False 
        
    def poll(self):
        """
        """ 
        print("\rListening!", end="")
        prompts = " ".join(self.args["prompts"]) 
        from pocketsphinx import LiveSpeech
        try:
            speech = LiveSpeech(keyphrase='robotics', kws_threshold=1e-30)
            for prompt in   speech:   
                print("\rHello!", end="")
                return True 
        except:
            pass 

        return False
        

    def listen(self):
        """

        """ 

        try:       
          with sr.Microphone() as source:
            
            if source is None:
                return "I am having problems hearing. My Microphone is off."
         
            if self.b_adjusted is False:
                self.recognizer.adjust_for_ambient_noise(source , duration=0.5)
                self.b_adjusted = True

            try:    
               audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=8)

            except sr.WaitTimeoutError:
               return "Timed out waiting for a responce"
             
            response  = "" 
            try:
                tmp = self.recognizer.recognize_sphinx(audio)  
                response = tmp 
            except sr.UnknownValueError:
                print("/rCould not understand audio", end="")
                
            except sr.RequestError as e:
                print("/r Could not request results; {0}".format(e), end="")
             
            response = response.lower()   

            return response
          
        except:
           return "I am having problems hearing. My Microphone is off."                
    
    def serve_forever(self): 
        """
        
        """

        while True: 
           
           detected  = self.poll()
    
           if detected: 
                val = self.listen()
                if val == "":
                     val = "Error" 
                self.nerves.set(self.sense, val) 
                self.counter = 0


           time.sleep(self.polling_rate)
           self.counter = self.counter + 1

if __name__ == "__main__":
    """ 
   
    """
    args =  parser.parse_args() 
 
    mode    = args.mode 
    robot   = args.robot   
    args    = json.loads(args.args  ) 
 
    speech  = Speech(robot, args )
    if mode == "serve":
        speech.serve_forever() 

