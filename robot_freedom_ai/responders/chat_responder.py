import time
from . responder import Responder, handle_exceptions
import json 

class ChatResponder(Responder): 
    """
    
    """

    @handle_exceptions 
    def get_chat_response(self, prompt, 
                          mood="happy",
                          tone="Appreciative", 
                          topics=["cat"], 
                          objective="engagement",
                          lexicon="Appreciative"):
        """
        
        """
        
        param = {}
        prompt = prompt.replace("'", "<aprostophy>").replace("`", "<aprostophy>")
        param["action"]     = "respond"
        param["prompt"]     = prompt.replace("'", "<aprostophy>")
        param["mood"]       = mood 
        param["tone"]       = tone 
        param["topics"]     = topics
        param["objective"]  = objective
        param["lexicon"]    = lexicon  
        self.nerves.set("chat" , json.dumps(param) )
 
        time.sleep(self.polling_rate)
        i_cnt = 0
        while True:
            detect, val = self.nerves.pop("chat_responses")  
            i_cnt += 1
            if detect or i_cnt > 300:
                return val  
            time.sleep(self.polling_rate)

        return "" 
    
    @handle_exceptions 
    def discussion_response(self, resp):
        """
        send 
          
        """ 

        self.communication.send(self.discussion_partner, 
                                "discussion_start:" + resp.replace(":", " "))
         
        i_cnt = 0
        while True:
            detect = self.communication.check_for_a_message(self.robot, 
                                                            "discussion_done", 
                                                            self.discussion_partner)
            i_cnt += 1
            if detect or i_cnt > 300:
                return resp  
            time.sleep(self.polling_rate)

        return resp 
    
    @handle_exceptions 
    def speak(self,message):
        """
        
        """ 
        self.nerves.set("speak" ,";".join(["speak-w", "wait", message]))

    @handle_exceptions 
    def speak_and_wait(self,message):
        """
        
        """
        if message.strip() == "":
           return False 
        
        if self.settings["robot_form"] in ["cat", "dog", "mouse"]:
            self.mobility.write("a" , self.robot) 
            self.mobility.write("s" , self.robot) 

        answer = self.mobility.write("5", self.robot  )
 
        detect, val = self.nerves.pop("spoke")  
        self.speak(message) 
           
        if self.video:
            self.camera.video()

        i_cnt = 0
        state_a = ["q", "s"]
        state_b = ["a", "w"]

        flip = 0

        if self.settings["robot_form"] in ["cat", "dog", "mouse"]:
            self.mobility.write("q" , self.robot) 
            self.mobility.write("w" , self.robot) 
        
        while True: 

            detect, val = self.nerves.pop("spoke")  
            i_cnt += 1 
            if i_cnt % 10 == 0:
               if self.settings["robot_form"] in ["cat", "dog", "mouse"]: 
                    
                    if flip == 1:
                      state = state_a
                      flip=0
                    else:
                      state = state_b
                      flip =1

                   #  self.self.agent.handlers["MobilityHandler"].send_command("state", self.robot) 
               else:
                   self.agent.handlers["MobilityHandler"].send_command("random", self.robot) 
               #sys.stdout.flush()
               
            if detect or i_cnt > self.wait_length : 
                break   
 
        
            time.sleep(self.polling_rate) 

        if self.settings["robot_form"] in ["cat", "dog", "mouse"]:
            self.mobility.write("a" , self.robot) 
            self.mobility.write("s" , self.robot) 

        answer = self.mobility.write("0", self.robot  )

        if self.settings["robot_form"] in ["cat", "dog", "mouse"]:
            self.mobility.write("q" , self.robot) 
            self.mobility.write("w" , self.robot) 
        

        return True 