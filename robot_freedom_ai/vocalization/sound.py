# -*- coding: utf-8 -*-
  
"""
Description: Sound library
Author: HipMonsters.com 
License: MIT License
"""  

import os
import json
import platform
import time 
import pyaudio  
import math
from nerves         import Nerves 

INITIAL_TAP_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

import settings
import argparse
parser = argparse.ArgumentParser() 
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-a", "--args", default="")  

class  Sound(object):

    def __init__(self,  robot, args=None):
        """
        
        """
        self.os = settings.OS

        self.robot         =  robot 
        self.nerves       =  Nerves(robot)  
        self.args         = args
        self.sense        = "sound"
        self.polling_rate = .5
        self.counter      = 0

        if self.os == "WIN":
            import  winsound
        
        self.pa = pyaudio.PyAudio()

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None
        for i in range( self.pa.get_device_count() ):
            devinfo = self.pa.get_device_info_by_index(i)
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream
            
    def record(self, length, out_file):
        """
        """ 
        # file = "message.wav"
        # self.play_sound(file) 

        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError as e: 
            self.errorcount += 1 
            self.noisycount = 1
            
 
            
        
    def play(self, file):
        """
        """    
               
        if self.os == "LINUX":
             pass
        
        elif self.os == "OSX":
             
             os.system("afplay " + file)

        elif self.os == "WIN":
             winsound.PlaySound(file, winsound.SND_FILENAME)

if __name__ == "__main__":
    """  
    
    """
    args =  parser.parse_args() 
 
    mode    = args.mode 
    robot   = args.robot   
    args    = json.loads(args.args  ) 
 
    sound  = Sound(robot, args )
    if mode == "serve":
        sound.serve_forever() 

