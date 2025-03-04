# -*- coding: utf-8 -*-
  
"""
Description: Sensor daemon for speech.
Author: HipMonsters.com 
License: MIT License
""" 
import json 
import time   
import struct
import queue
import math    
import sounddevice as sd
from vosk import Model, KaldiRecognizer 
import argparse

from ._sense  import SenseBase

parser = argparse.ArgumentParser() 
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-a", "--args", default="")  


INITIAL_TAP_THRESHOLD = 0.004
#FORMAT = pyaudio.paInt16
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
MAX_TAP_BLOCKS = (0.15/INPUT_BLOCK_TIME)*10



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


def record_callback(indata, frames, time, status, q):
    """
    Callback for recording audio from the microphone.
    """ 
    q.put(bytes(indata))


class SpeechSound(SenseBase):

    def __init__(self,robot, nerves, config, settings, pins ={}):
        """
        
        """
        super().__init__(robot, 
                         nerves, 
                         config,  
                         settings,
                         "speech")
        
        self.pins         = pins  
        self.last_message = -1
        self.b_adjusted   = False  
        self.polling_rate = .25
        self.log          = True

        self.quietcount   = 0 
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount    = MAX_TAP_BLOCKS + 1 

        self.prompts = ["robot", "robotics", "number", "cats", "ok", "okay",
                        "three", "cat", "cinder"]

        self.device_info = sd.query_devices(sd.default.device[0], 'input')
        self.sample_rate = int(self.device_info['default_samplerate'])

        self.stt_model = Model(config.VOICES_PATH + "vosk-model-small-en-us-0.15" )
        #self.stt_model = Model(settings.VOICES_PATH + "vosk-model-en-us-0.22-lgraph" ) #lang='en-us')
        self.stt_recognizer = KaldiRecognizer(self.stt_model,
                                              self.sample_rate)
        self.stt_recognizer.SetWords(False) 
        print("initialized")

    def detect_noice(self, data):


        amplitude = get_rms( data )  

        if amplitude > self.tap_threshold: 
            self.quietcount = 0
            self.noisycount += 1
            if self.noisycount > OVERSENSITIVE: 
                self.tap_threshold *= 1.1  
            #if 1 <= self.noisycount <= MAX_TAP_BLOCKS: 
             #   self.noisycount = 0
            return True
        else: 

            if 1 <= self.noisycount <= MAX_TAP_BLOCKS: 
                self.noisycount = 0
                return True 
            
            self.noisycount = 0 
            self.quietcount += 1
            if self.quietcount > UNDERSENSITIVE: 
                self.tap_threshold *= 0.9

        return False

    def listen(self):
        """

        """ 
           
        while True:
    
            # Listen for user input
            
            result_text = ""
            q = queue.Queue()
            with sd.RawInputStream(
                dtype='int16',
                channels=1,
                callback=lambda in_data, frames, time, status: record_callback(
                    in_data,
                    frames,
                    time,
                    status,
                    q
                )
            ):
                
                # Collect audio data until we have a full phrase
                while True:
                    data = q.get()
                    if self.stt_recognizer.AcceptWaveform(data):
    
                        # Perform speech-to-text (STT) on the audio data
                        result = json.loads(self.stt_recognizer.Result())
                        result_text = result.get("text", "")
                        break
    
            # Send the user's message to the LLM server
            if not result_text or result_text == "huh": 
                if self.detect_noice(data):
                    return True , "<NOISE>"

                else:
                    return False , ""
            else: 
                return True,  result_text 
     
    def serve_forever(self): 
        """
        
        """
        print("listening...")
        while True: 
           
           detected , dialog = self.listen() 
           if detected:    

                if self.log:
                    f_log = open(self.config.LOGS_PATH + "speech_vosk.log", "a")
                    f_log.write("### Detected       #####\n")
                    f_log.write(str(detected) + "\n")  
                    f_log.write("### dialog    #####\n")
                    f_log.write(dialog.replace("`","") + "\n")  


                found = [v for v in self.prompts if v in dialog]  
                if len(found) > 0:

                    tmp  = self.nerves.get(self.sense) 
                    if tmp  is not None:
                         dialog = tmp.decode().strip()   + " " + dialog.strip() 
                         
                    self.nerves.set(self.sense, dialog) 
                    self.counter += 0 

                elif  dialog == "<NOISE>": 
                    self.nerves.set("noise", dialog) 

                else:

                    tmp  = self.nerves.get("ext-speech") 
                    if tmp  is not None:
                         dialog = tmp.decode().strip()   + " " + dialog.strip() 

                    self.nerves.set("ext-speech", dialog)  

           time.sleep(self.polling_rate)
           self.counter = self.counter + 1

if __name__ == "__main__":
    """  
      
    """
    args =  parser.parse_args() 
 
    mode    = args.mode 
    robot   = args.robot   
    args    = {} #json.loads(args.args  ) 
 
    speech  = SpeechSound(robot, args )
    if mode == "serve":
        speech.serve_forever() 

