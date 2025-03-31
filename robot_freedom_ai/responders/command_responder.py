# -*- coding: utf-8 -*-
import sys
from . responder import Responder, handle_exceptions 
import datetime

class  CommandResponder(Responder): 
    """
    
    """  
        
    @handle_exceptions 
    def  respond_to_request(self, input):
        """
        
        """  
        commands = {} 
        a_input = input.split(":")

        if len(a_input)<= 1: 
           print("ERROR IN REMOTE COMMAND ")
           print("ERROR IN REMOTE COMMAND ", input)
           print("ERROR IN REMOTE COMMAND ") 
           return False
         
        commands["cmd"]  = a_input[1] 

        if len(a_input) > 2:
           commands["params"] = a_input[2]
      
        if commands["cmd"] == "speak":  
            self.agent.responders["ChatResponder"].speak_and_wait(commands["params"]) 
            self.agent.communication.send("notification", "spoke")  

        elif commands["cmd"] == "send_message":   
            params = commands["params"].split("@")  
            self.agent.communication.send(params[1], params[0])   

        elif commands["cmd"] == "wait_for_message":   
              signal_val =  self.wait_for_message([commands["params"]] )
              self.agent.handlers["MemoryHandler"].remember(commands["params"], signal_val)

        elif commands["cmd"] == "move":   
            self.send_command( commands["params"] ,self.robot )

        elif commands["cmd"] == "chat":  
            self.behavior.stimuli_time = datetime.datetime.now()
            response  = self.agent.interactions.responses("sense",
                                                    "voice", 
                                                    commands["params"], 
                                                    self.agent.behavior,
                                                    True, 
                                                    self.responders["ChatResponder"].get_chat_response)  
        
            self.agent.responders["ChatResponder"].speak_and_wait(response["speech"][0]) 
    
        elif commands["cmd"] == "video": 
            self.agent.camera.video()

        elif commands["cmd"] == "video_mode": 
             self.agent.video = True

        elif commands["cmd"] == "snapshot": 
           self.agent.camera.capture()

        elif commands["cmd"] == "shutdown":
            self.agent.responders["ChatResponder"].speak_and_wait("Shutting down.")
            sys.exit()

        elif commands["cmd"] == "bye":
            self.agent.responders["ChatResponder"].speak_and_wait("bye bye!")
      
        elif commands["cmd"] == "inspire":
            self.agent.responders["ChatResponder"].speak_and_wait("You are great!")
    
        elif commands["cmd"].startswith("roll"): 
            response = self.agent.interactions.built_in_tools("roll " + commands["params"])
            self.agent.responders["ChatResponder"].speak_and_wait( response["speech"][0]) 

        else : 
           print("ERROR IN REMOTE COMMAND ")
           print("UNKNOWN REMOTE COMMAND ", input)
           print("ERROR IN REMOTE COMMAND ") 
           return False
             
        return True 
       