# -*- coding: utf-8 -*-
  
"""
Description: This builds and controls a simple chatbot design to run on a RaspberryPi.
Author: HipMonsters.com 
Date Created: Jan 1, 2021
Date Modified: Oct 10, 2024
Version: 8.0
Plaftorm: RaspberryPi
License: MIT License  
"""
import os
import sys 
import time 
import json    
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-d", "--devices", default="")  
parser.add_argument("-p", "--param", default="")  
 

class Response(object): 

    def __init__(self, robot, nerves, config, settings, cognitive_control = None, personality =None,
                      lt_memory = None, st_memory=None, params =None, polling_rate = .1, fit=False):
        """
        
        """ 
        self.robot     = robot 
        self.nerves   = nerves
        self.module   = "chat"  
        self.config   = config
        self.settings = settings  
        self.os       = self.config.OS
        self.st_memory = st_memory
        self.lt_memory = lt_memory
        self.polling_rate = polling_rate

        self.low_memory_mode = False
        if self.config.CONFIG["low_memory_mode"] ==1: 
            self.low_memory_mode = True

        if lt_memory is None:
              from memory.lt_memory import LTMemory  
              lt_memory       = LTMemory(robot, config, self.low_memory_mode)  

        if st_memory is None:
              from memory.st_memory import STMemory  
              st_memory       = STMemory(robot, config, self.low_memory_mode)  

        if personality is None: 
              from .personality import Personality  
              personality       = Personality(robot,  config, settings)  
              
        if cognitive_control is None: 
              from .cognitive_control import CognitiveControl  
              cognitive_control       = CognitiveControl(robot,  config, settings, personality, self.low_memory_mode)

        self.cognitive_control = cognitive_control
        self.personality       = personality
        self.lt_memory = lt_memory
        self.st_memory = st_memory
 
        if 'chat' not in self.settings: 
           self.chat_params = {"type":"CSim"}
        else:
           self.chat_params = self.settings["chat"] 


        ## How to Formulate a verbal response    
        if self.chat_params["type"] == "CSim": 
            self.bot = self.lt_memory
            self.type = "CSim"

        elif self.chat_params["type"] == "Ollama":
            from  .models.ollama_rf import  OllamaRF

           # config, cognitive_control, personality, lt_memory, st_memory, full_name, name ,topics , tones=["Appreciative"], 
            #      params= {},   log=True, repeat_log= True
            self.bot = OllamaRF(config, self.cognitive_control, self.personality, self.lt_memory, self.st_memory, robot.replace("_", " "), robot,  ["cats"],  log=True)
            self.type = "Ollama"

        elif self.chat_params["type"] == "Llama":
            from .models.llama_cpp  import Llama
            self.bot = Llama(settings.DATA_PATH + "llama.2g.llm") 
            self.type = "Llama"
 
        return None     
        
    def serve_forever(self): 
        """ 

        """

        while True:
 
           new, cmds = self.nerves.pop(self.module) 
           if new:
               
              # acmds = cmds.split(">") 
               dcmds = json.loads(cmds.strip()) 

               if dcmds["action"] == "respond":
                  if dcmds["topics"] == "sense":
                      dcmds["topics"] = []

                  if dcmds["tone"] == "quiet":
                      dcmds["tone"]     = "Benevolent"
                      dcmds["lexicon"]  = "Benevolent"

                  response =  self.bot.respond(dcmds["prompt"].replace("<aprostophy>", "'"),
                                               dcmds["mood"], 
                                               dcmds["tone"], 
                                               dcmds["topics"],
                                               dcmds["objective"],
                                               dcmds["lexicon"] )
                  
                  self.nerves.set(self.module + "_responses", response )   

               self.nerves.set(self.module, "")  
 
           time.sleep(self.polling_rate)
           
if __name__ == "__main__":
    """

    """
    args    =  parser.parse_args()  
    mode    = args.mode 
    robot   = args.robot   
 
    os.chdir('../')
    sys.path.insert(0, os.path.abspath('./')) 
    import config 
    from communication.nerves import Nerves 
    from memory.lt_memory import LTMemory
    from memory.st_memory import STMemory
    from ai.cognitive_control import CognitiveControl 

    cognitive_control       = CognitiveControl(robot,  config, {}, False) 
    lt_memory       = LTMemory(robot, config) 
    st_memory       = STMemory(robot, config) 

    nerves  = Nerves(robot) 

    with open(config.DATA_PATH + robot + "/settings.json") as f:
           data = ''
           for row in f:
              data += row  
           settings = json.loads(data)

    chat = Response( robot, nerves, config, settings,cognitive_control, lt_memory, st_memory) 

    if mode == "serve": 
        chat.serve_forever()

    elif mode == "test":  
       chat  = Response(robot  ) 

    elif mode == "fit":  
       chat.build_models(args.param)