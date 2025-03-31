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
import sys   
import datetime  
import time  
from .protocol import Protocol
 
 
import argparse
parser = argparse.ArgumentParser() 
parser.add_argument("-r", "--robot"        , default="")    
parser.add_argument("-p", "--protocol"     , default="monitor")   
  

sys.path.append("..")
from  errors import handle_exceptions
    
class Monitor(Protocol):
    """
    
    """
    
    def __init__(self,  protocol,   agent  ):
        """ 

        """ 
        super().__init__(protocol, agent )
 
            
           
    @handle_exceptions  
    def initiate(self, directives):
        """ 
        monitor
        """ 
        self.last_time_user_spoke = datetime.datetime.now()
        i_quiet = 0
        while True:   

            ### Update clocks
            self.epoch          += 1
            self.current_cycle  =  datetime.datetime.now()

            ## Robot to Robot communication via Web
          
            if self.low_memory_mode or self.networked == -1:
                have_message, commands = False , ""
            else:  
                have_message, commands = self.communication.check_messages() 
 
            if have_message:  
                if commands.find("@" + self.robot ) > -1:   
                       commands =  commands.find("@" + self.robot   , "")
                       self.respond_to_request(commands) 
                       continue 
                
                elif commands.find("remote_cmd") > -1:  
                    self.respond_to_request(commands) 
                    continue 

                elif commands.find("direct_cmd") > -1:  
                     by_pass =True 
                     acommands = commands.split(":")[1].split(',')
                     if len(acommands) == 1:
                         self._detected(acommands[0], i_quiet, "")
                     else:    
                         self._detected(acommands[0], i_quiet, acommands[1])
                     continue
                     

                elif commands.find("announcement") > -1:  
                     continue
                else:
                    print("UNKOWN COMMAND", commands)
        
            detect, commands = self.nerves.pop("remote_cmd") 
            if detect:
                self.respond_to_request(commands) 
                continue 

            if self.chat:
               monitor_sense = ["ext-speech", "speech"]  
                 
            elif self.low_memory_mode:
               monitor_sense = ["distance", "movement"] 

            elif self.movement:
               monitor_sense = ["distance", "movement", "balance"] 
               
            else:
               monitor_sense =  self.behavior.cognitive_control.sense_types["physical"].keys()
                
            for sense in  monitor_sense:
  
                if sense == "quiet": 
                    dur = self.current_cycle - self.last_stimuli 
                    if dur.total_seconds() > self.quiet_in_secs :
                        detect,  amplitude = True, .10* dur.total_seconds()  
                        i_quiet += 1
                    else:
                        detect, amplitude = False, "nothing" 
                else:
                    detect, amplitude = self.nerves.pop(sense)  
  
                slog =  sense.ljust(25, ' ') + " " + str(detect) + self._space  

                print("\r" + slog,  end="") 

                if detect:  
                    if sense != "quiet":
                         i_quiet = 0 

                    result  = self._detected(sense, i_quiet, amplitude)

                   # if i_quiet >= self.self_reflection_threshold:
                   #     i_quiet = 0

                time.sleep(self.polling_rate) 
            time.sleep(self.polling_rate) 
 
if __name__ == "__main__":

    """ 

    """
    args =  parser.parse_args()  
    protocol    = args.protocol    
    robot       = args.robot    
