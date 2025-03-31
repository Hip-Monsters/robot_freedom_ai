# -*- coding: utf-8 -*-
"""
Description: The agent daemon that allows the Artificial Intelligence to process sensors signals and control the robot.
Author: HipMonsters.com
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024
Version: 4.0
Platform: RaspberryPi
License: MIT License 
"""
import json
import sys  
import csv
import datetime  
import time  

####    Libraries   ################
 
 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot"        , default="")    
parser.add_argument("-p", "--params"       , default="{}")  
parser.add_argument("-c", "--command_style", default="sequence")  
parser.add_argument("-v", "--verbose"      , default=False)   
 
sys.path.append("..")
from  errors import handle_exceptions
    
class Protocol(object):
    """
    
    """
    
    def __init__(self, protocol, agent ):
        """ 

        """ 

        self.protocol  = protocol  
        self.agent     = agent  
        self.os        = agent.config.OS
        self.config    = agent.config.CONFIG   
        self.verbose   = agent.config.VERBOSE 

        self.chat       = agent.chat
        self.networked  = agent.networked
        self.robot      = self.agent.robot  
        self.polling_rate        = self.agent.polling_rate
        self.polling_rate_listen = self.agent.polling_rate_listen
        self.low_memory_mode = self.agent.low_memory_mode

        self.nerves     = agent.nerves
        self.behavior   = agent.behavior
        self.movement   = agent.movement
        self.communication  = self.agent.communication
        self.interactions = self.agent.interactions 
 
        self.current_states = self.agent.current_states 
            
        self.get_chat_response   = self.agent.responders["ChatResponder"].get_chat_response
        self.speak_and_wait      = self.agent.responders["ChatResponder"].speak_and_wait
        self.speak               = self.agent.responders["ChatResponder"].speak
        self.discussion_response = self.agent.responders["ChatResponder"].discussion_response
        self.respond_to_request  = self.agent.responders["CommandResponder"].respond_to_request

        self.send_command        = self.agent.handlers["MobilityHandler"].send_command
        self.remember            = self.agent.handlers["MemoryHandler"].remember 
        self.wait_for_signal     = self.agent.handlers["NervesHandler"].wait_for_signal

        self.self_reflection_threshold = 2
        self.prior_response   = {}   

        self._space  = " ".join(['' for v in range(40)]) 
        self.epoch            = 0
        self.last_stimuli     = datetime.datetime.now()
        self.current_cycle    = datetime.datetime.now() 
        self.last_update      = datetime.datetime.now() 
        self.last_movement    = datetime.datetime.now() 
        self.last_spoke       = datetime.datetime.now() 
        self.last_self_reflect = datetime.datetime.now() 

      
        self.discussion_partner = None 
        self.self_reflection_threshold = 2
        self.prior_response   = {}

        self.quiet_in_secs    = 60
        self.last_moved       = 99
        self.last_talked      = 99 
        self.sensor_pause     = .01 

    @handle_exceptions 
    def _detected(self, sense, i_quiet, amplitude):
        """
        """
        if sense == "ext-speech":
            sense = "speech"
        
        interval              = (datetime.datetime.now() - self.last_stimuli).total_seconds()   
        self.last_moved       = (datetime.datetime.now() - self.last_movement).total_seconds() 
        self.last_talked      = (datetime.datetime.now() - self.last_spoke).total_seconds()  

        if i_quiet == self.self_reflection_threshold: 
            if  self.low_memory_mode is False: 
                    print("\r" + "Initiating Sleep Cycle..."     +     self._space )  
                    print("\r" + "Dreaming....            "      +     self._space )   
                    self.behavior.reflection()
                    self.last_self_reflect  = datetime.datetime.now()

            print("\r" + "Starting Wakeup Sequence..."  +     self._space , end="")  
            self.chat = False 

        self.behavior.stimuli("sense", sense, amplitude,  1, 
                               self.prior_response ,
                               self.epoch, interval, self.last_moved,  
                               self.last_talked, 
                               interval) 

        self.nerves.set("stimuli", sense + ":" + self.behavior.emotions.mood() )  

        if sense == "speech":
            self.chat = True  

        if self.chat:

            if "bye" in amplitude:
                self.chat = False
                self.speak_and_wait("Bye!")   
                responses = {"speech":[], "movement": ["random"]}

            elif amplitude.strip() == "":
                responses = {"speech":[], "movement": ["random"]}

            elif  sense == "speech":  
                responses = self.interactions.responses("sense", 
                                                 sense, 
                                                 amplitude,  
                                                 self.behavior,
                                                 self.chat,
                                                 self.get_chat_response) 
            else:
                responses = {"speech":[], "movement": ["random"]}
        else:
            responses = self.interactions.responses("sense", 
                                                     sense, 
                                                     amplitude,  
                                                     self.behavior,
                                                     self.chat,
                                                     self.get_chat_response) 
                        
        for response in responses["movement"]: 
            self.send_command(response, self.robot  )


        for response in responses["speech"]: 
            if response != "":
                self.speak_and_wait(response)   
                self.prior_response =  responses 
                self.last_spoke  =  datetime.datetime.now()   
         

        self.last_stimuli  = datetime.datetime.now()   
        self.nerves.set(sense, "")  
        time.sleep(self.sensor_pause)

        if response != "":
            self.last_spoke  =  datetime.datetime.now() 
            time.sleep(1.5)
            for t in ['noise', 'speech', 'ext-speech']:
                detect, amplitude = self.nerves.pop(t)   
                     

        return True
     
if __name__ == "__main__": 
    """
    
    """
    args =  parser.parse_args()  
    mode    = args.mode    
    robot   = args.robot    
