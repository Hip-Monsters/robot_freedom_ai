# -*- coding: utf-8 -*-
"""
Description: The agent daemon that allows the Artifical Intelligence to process sensors signals and control the robot.
Author: Mood_Relate.org 
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024
Version: 4.0
Plaftorm: RaspberryPi
License: MIT License 
"""
import json 

####    Libraries   ################

import config   
from communication.nerves         import Nerves 
from communication.client         import Client
from communication                import network
from mobility.arduino             import MOBILITY 
from mobility.rpi_gpio            import MOBILITY_GPIO 
from mobility.sequences           import sequences  , FLIPS
from memory.lt_memory import   LemNormalize 

from senses.camera         import Camera 
from security.security     import Security
from assets.logo           import logo 
 
from ai.personality          import Personality
from ai.behavior             import Behavior
from ai.interactions         import Interactions
from ai.cognitive_control    import CognitiveControl
from ai.ethics               import Ethics   

from memory.st_memory        import STMemory   
from memory.lt_memory        import LTMemory   

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--protocol"     , default="monitor")  
parser.add_argument("-r", "--robot"        , default="")    
parser.add_argument("-n", "--networked"    , type=int,  default=1, required=False)     
parser.add_argument("-d", "--directives"      , default="{}")   
parser.add_argument("-v", "--verbose"      , default=False)   
 
from errors import handle_exceptions 
    
class AIAgent(object):
    """
    
    """
   
    def __init__(self, protocol ,  
                  robot = "",   
                  networked = None,
                  sequence_format =True ):
        """ 

        """ 

        self.sequences = sequences  
        self.FLIPS     =  FLIPS
        self.protocol  = protocol   

        if networked is None:
             networked =  config.DEFAULT_2_NETWORKED
        self.networked     = networked
        
        self.os        = config.OS
        self.config    = config  
        self.verbose   = config.VERBOSE 
        self.polling_rate     = .1 
        self.polling_rate_listen = .05 

        self.current_states   = {}

        self._space  = " ".join(['' for v in range(40)]) 

        self.sequence_format = sequence_format

        if robot != "":
            self.robot = robot 
        else:
            self.robot = self.config.CONFIG["robot"]   
        
        with open(self.config.DATA_PATH + self.robot + "/settings.json") as f:
           data = ''
           for row in f:
              data += row  
           self.settings = json.loads(data)

        if self.config.CONFIG["low_memory_mode"] == 1:
            self.low_memory_mode   = True
        else:
            self.low_memory_mode   = False
 
        self.communication_ip   = list(config.NET_CONFIG["hubs"].keys())[0]   
        self.chat     = False
        self.movement = False
        self.video    = False 
        self.b_llm    = False
  
        self.robot_ports = None 
        if self.os == "OSX": 
            self.robot_ports = ('/dev/cu.usbmodem14201',"1")  

        elif self.os == "WIN": 
            self.robot_ports = ('/dev/cu.usbmodem14201',"1")  
        else:
            self.robot_ports = ("/dev/ttyACM0", "1")  
  
        self.nerves     = Nerves(self.robot) 
        self.security   = Security(self.robot,
                                   self.config, 
                                   self.nerves)
 
        print("\r Communication ..."  + self._space , end="")
        
        if self.low_memory_mode == False and self.networked ==1: 
            if self.communication_ip is not None:
                self.communication = Client(self.robot, self.communication_ip)
            else: 
                directives = Client(self.robot)
            
            try:
                self.communication.connect()
                self.communication.send("WORLD", "AWAKE")
            except:
                print("Issue Connecting") 
        else:
                self.communication = self.nerves
 
    
        print("\r Initializing Controler ...."  + self._space , end="")
        self.mobility    =  MOBILITY(self.robot)    
 
        print("\r Initializing Camera..  "  + self._space , end="" ) 
        self.camera       =  Camera(self.robot, 
                                      self.nerves ,
                                      self.config) 

        print("\r Spawning Vocalization...."  + self._space , end="")
        self.nerves.set("speak" ,"Waking up.")  

        self.device_connections = {}   
        print("\r Connecting devices.  " + self._space, end="")
        self.connect_devices()
        
        ## TODO set up actions (Should load from YAML)
        self.handlers = {}
        for module in [ ["handlers.mobility_handler", "MobilityHandler"], 
                        ["handlers.nerves_handler"  , "NervesHandler"], 
                        ["handlers.memory_handler"  , "MemoryHandler"]]: 
            classname = module[1]
            _mod     = __import__(module[0] , fromlist=[None] )  
            self.handlers[classname]  = getattr(_mod, classname )( self ) 
             
        self.responders = {}
        for module in [ ["responders.chat_responder"    ,  "ChatResponder"], 
                        ["responders.command_responder"  , "CommandResponder"]]: 
            classname = module[1]
            _mod     = __import__(module[0] , fromlist=[None] )  
            self.responders[classname]  = getattr(_mod, classname )( self ) 

        
        self.personality    = Personality(self.robot, 
                                         self.config,
                                         self.settings )
        print("\r Loading AI CognitiveControl               " + self._space, end="")
        self.cognitive_control            = CognitiveControl(self.robot, 
                                                  self.config,
                                                  self.settings ,
                                                  self.personality,
                                                  self.low_memory_mode)
        
        self.st_memory       = STMemory(robot, config,self.low_memory_mode) 
        self.lt_memory       = LTMemory(robot, config,self.low_memory_mode)  

        print("\r Loading AI Behavior                " + self._space, end="")
        self.behavior    = Behavior(self.robot               , 
                                    self.config              ,
                                    self.settings            ,
                                    self.personality         ,
                                    self.cognitive_control   ,
                                    self.st_memory           , 
                                    self.lt_memory           ,
                                    self.low_memory_mode) 
  

        if "chat" in self.settings:
            if self.settings["chat"]["type"] in ("Ollama"):
                self.b_llm = True  
        print("\r Loading AI Interactions          " + self._space, end="")
        self.interactions             = Interactions(self.robot, 
                                                     config,
                                                     self.cognitive_control,
                                                     self.lt_memory,
                                                     self.low_memory_mode,
                                                     llm = self.b_llm)

        self.ethics                   = Ethics(self.robot)

        print("\r Robot and AI setup is complete." + self._space + self._space, end="")   
        if self.low_memory_mode == False and self.networked == 1:
            print("Communicating IP    :"    + self.communication.ip  +  self._space )  
            tmp = open(self.config.LOGS_PATH + "inet_addr.log","a" )
            tmp.write(self.communication.ip  + "\n")
            tmp.close() 
 
        ip_addr = network.get_local_ip()
        self.ip_address = ip_addr
        print("Robot's IP Address  :"    + ip_addr) 


    def connect_devices(self):
        """
        
        """ 
        
        self.device_connections = {}
        self.device_connections[self.robot] =  self.robot_ports 

        self.mobility.connect_to_devices(self.device_connections)   

        self.mobility.write("7", self.robot)
        for sig in ["a", "s", "d" , "f", "g", "h", "j", "k"]:
             self.mobility.write(sig, self.robot)
             self.current_states[sig] = True
        self.mobility.write("0", self.robot)
 
    @handle_exceptions 
    def initiate(self, directives):
        """
        
        """ 

        module                  = "protocols." + protocol
        classname               = protocol.title()
        _mod                    = __import__(module , fromlist=[None] )  
        self.current_protocol   = getattr(_mod, classname )(protocol, self ) 

        self.current_protocol.initiate(directives)

        return True
      
     
if __name__ == "__main__":

    """ 
    
    """
    args       = parser.parse_args()  
    protocol   = args.protocol    
    robot      = args.robot   
    networked  = args.networked   
    directives = json.loads(args.directives)

    command_style_sequence = True 
    
 
    agent = AIAgent(robot = robot,
                    protocol=protocol,   
                    networked=networked,
                    sequence_format  = command_style_sequence) 
    agent.initiate(directives)
