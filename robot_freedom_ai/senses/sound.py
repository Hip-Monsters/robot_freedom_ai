# -*- coding: utf-8 -*-
  
"""
Description: Sensor daemon for sound.
Author: HipMonsters.com 
License: MIT License
"""

import json 
from ._sense  import SenseBase

import time 
import struct
import math 
 
import speech_recognition as sr  
import pyaudio   


import argparse
parser = argparse.ArgumentParser() 
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-a", "--args", default="")  

INITIAL_TAP_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100 # 44100
INPUT_BLOCK_TIME = 0.1# 0.05
INPUT_FRAMES_PER_BLOCK =   int(RATE*INPUT_BLOCK_TIME) 
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME



def get_rms( block ):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )


class  Sound(SenseBase):

    def __init__(self,  robot, nerves, config, settings, pins ={}):
        """
        
        """
        super().__init__(robot, nerves, config, settings, "noise")
             
        self.pins          = pins 
        self.last_message  = -1
        self.b_adjusted    = False 
        self.recognizer    = sr.Recognizer()   
        self.pa            = pyaudio.PyAudio()
        self.stream        = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount    = MAX_TAP_BLOCKS + 1 

        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("\rMicrophone with name \"{1}\" found for         `Microphone(device_index={0})`".format(index, name), end="")
             

    def stop(self):
        """
        
        """
        self.stream.close()

    def find_input_device(self):
        """

        """
        device_index = None
        for i in range( self.pa.get_device_count() ):
            devinfo = self.pa.get_device_info_by_index(i)
            print( "\rDevice %d: %s"%(i,devinfo["name"]) , end="")

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "\rFound an input: device %d - %s"%(i,devinfo["name"])  , end="")
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        """
        
        """
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def tapDetected(self, source2): 
        """
        
        """ 
        pass

    def poll(self):
        """
        
        """
             
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)
        except IOError as e: 
            self.errorcount += 1 
            self.noisycount = 1 
            self.stream = self.open_mic_stream()
            return False

        amplitude = get_rms( block ) 

        if amplitude > self.tap_threshold: 
            self.quietcount = 0
            self.noisycount += 1
            if self.noisycount > OVERSENSITIVE: 
                self.tap_threshold *= 1.1
        else: 

            if 1 <= self.noisycount <= MAX_TAP_BLOCKS:
                self.tapDetected(None) #sr.Microphone() ) 
                return True
            
            self.noisycount = 0
            self.quietcount += 1
            if self.quietcount > UNDERSENSITIVE: 
                self.tap_threshold *= 0.9

        return False

    def listen(self):
        """

        """ 
               
        with sr.Microphone() as source:

            if source is None:
                return "I am having problems hearing. My Microphone is off."
         
            if self.b_adjusted is False:
              self.recognizer.adjust_for_ambient_noise(source , duration=0.5)
              self.b_adjusted = True

            try:    
               audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)

            except sr.WaitTimeoutError:
               return "Timed out waiting for a reponce"
             
            response  = ""
 
            try:
                response = self.recognizer.recognize_sphinx(audio)  
                
            except sr.UnknownValueError:
                print("/rCould not understand audio", end="")
                
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e), end="")
             
            response = response.lower()  

            return   response
                    
    
    def serve_forever(self): 
        """
        
        """

        while True:
           detected  = self.poll()

           if detected:
                val = "Noise" #self.listen()
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
 
    sound  =  Sound(robot, args )
    if mode == "serve":
        sound.serve_forever() 

