#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Description: AI interactions lookup.
Author: HipMonsters.com  
License: MIT License  
"""

import random 
import json
  


class Interactions(object):
   ""


   ""

   def __init__(self, robot, config, cognitive_control, lt_memory,  low_memory_mode,  llm=False):
      """
      
      """
      self.robot              = robot
      self.config             = config
      self.low_memory_mode    = low_memory_mode
      self.b_llm              = llm
      self.cognitive_control  = cognitive_control  
      self.mapped_strategies  = self.cognitive_control.mapped_strategies
      self.vocalization       = self.cognitive_control.vocalization
      self.movement           = self.cognitive_control.movement

      self.lt_memory          = lt_memory  
      self.set_chat_responses = self.lt_memory.set_chat_responses 
      self.chat               = self.lt_memory.memory 

 
 
   def greeting(self, sentence): 
        """
        If user's input is a greeting, return a greeting response
        """
        for word in sentence.split():
            if word.lower() in self.set_chat_responses["greeting_inputs"]:
                return random.choice(self.set_chat_responses["greeting_responses"])

   def get_stimuli_summary(self,  behavior):
       """

       """ 

       stimuli = {}
       for dt , details in behavior.st_memory.memory["stimuli"].items():
           stim =   details["stimuli"]
           if stim not in  stimuli:
               stimuli[stim ] = 1
           else:
               stimuli[stim ] = stimuli[stim ] + 1
 
       return stimuli 
    
   def return_self_eval(self, behavior, mood, template_id):
            """
            """
       
            template =  self.set_chat_responses["templates"][template_id]
            
            if template["source"] == "mood":
               resp = template["template"]
               response = [resp.replace("<INSERT>", mood )]

            elif template["source"] =="stimuli":
               resp = template["template"]
               stimuli = self.get_stimuli_summary(behavior)
               resp1 = " I experienced "
               for stim, cnt in stimuli.items():
                   resp1 +=  stim + " " + str(cnt) + " times today, "
               response  = [resp.replace("<INSERT>", resp1 ) ]

            return response
   
   def responses(self, topic, catogory, prompt,  behavior, interactive, get_chat_response):
       """ 

       """ 

       mood      = behavior.emotions.mood()
       objective = behavior.objective
       strategy  = behavior.strategy  
       result = {}
       result["topic"]          =  topic 
       result["catogory"]       =  catogory     
       result["stimui"]         =  behavior.stimui       
       result["stimuli_class"]  =  behavior.stimuli_class
       result["amplitude"]      =  behavior.amplitude   
       result["stimui_time"]    =  behavior.stimui_time  
       result["scrs"]           =  behavior.scrs 
       result["scr"]            =  behavior.scr   
       result["met"]            =  behavior.met  
       result["umet"]           =  behavior.umet   
       result["indif"]          =  behavior.indif   
       result["mood"]           =  behavior.mood   
       result["objective"]      =  behavior.objective    
       result["strategyv"]      =  behavior.strategy    
       result["stimui_time"]    = str(behavior.stimui_time) 

       if self.b_llm:
           response = self.__responses_llm(topic, catogory, prompt,  behavior, interactive, get_chat_response)
       else:
           response = self.__responses_csim(topic, catogory, prompt,  behavior, interactive, get_chat_response)
       
       if len(response["speech"]) > 0 or  len(response["movement"]) > 0:
           result["prompt"]         = prompt
           result["response"]       = response
           with open(self.config.DATA_PATH + self.robot + "/actions.json", "a") as f:
                f.write(json.dumps(result) + "\n")

       return response    
   
   def __responses_llm(self, topics, catogory, prompt,  behavior, interactive, get_chat_response):
       """
       
       """
       
       response  = {"speech" : "", "movement":[]}
       mood      = behavior.emotions.mood()
       objective = behavior.objective
       strategy  = behavior.strategy  
       """
       if prompt == "":
           prompt = "Hi there!"
       resp = get_chat_response(prompt, mood, strategy, topics ,
                                             objective, strategy ) 
       resp = [resp]  
       print(prompt, mood, strategy, topics ,  objective, strategy )
       """ 
         
       if interactive:
           """
           Self Reflection
           """
           if prompt.strip() == "":
               resp = ["hello? Anyone there?"]
           else:
               b_self_reflect = False
               for query, details in self.set_chat_responses["queries"].items(): 
                 matches = [1 for w in prompt.split() if w in query.split()] 
                 if len(matches) / float(len(query.split())) > .7: 
                    template_id = details["template"] 
                    resp = self.return_self_eval( behavior, mood, template_id)
                    b_self_reflect = True
    
               if  b_self_reflect is False:
                   resp = get_chat_response(prompt, mood, strategy, topics ,
                                             objective, strategy ) 
                   resp = [resp] 

           response["speech"]  =  resp

       elif strategy == "quiet": 
            response["speech"] = [""] 
       else: 

           i_index = random.randint(0,10)  
           if  i_index <= 5:
              i_max = len(self.chat["initiate"][strategy]) - 1  
              i_index = random.randint(0, i_max) 
              init_response  = self.chat["initiate"][strategy][i_index]["response"]
             # prompt  = init_response[0]  
            #  resp = get_chat_response(prompt)   
              #resp = [resp]
              resp = init_response
           else:     
              i_max = len(self.set_chat_responses["queries"].keys()) - 1   
              i_index = random.randint(0, i_max) 
              details  = self.set_chat_responses["queries"][list(self.set_chat_responses["queries"].keys())[i_index]]
              template_id = details["template"] 

              resp = self.return_self_eval( behavior, mood, template_id)
             
           response["speech"]  =  resp 
            
       i_max = len(self.movement[objective]) -1
       i_index = random.randint(0,i_max)
       response["movement"] =  [self.movement[objective][i_index]]  

       return  response
   
   def __responses_csim(self, topics, catogory, prompt,  behavior, chat, get_chat_response):
       """
       
       """
       response  = {"speech" : "", "movement":[]}
       mood      = behavior.emotions.mood()
       objective = behavior.objective
       strategy  = behavior.strategy  
 
       if chat and strategy != "quiet": 
             
           if prompt.strip() == "":
               resp = ["Hello? Anyone there?"]
           else:
                b_self_reflect = False
                for query, details in self.set_chat_responses["queries"].items(): 
                 matches = [1 for w in prompt.split() if w in query.split()] 
                 if len(matches) / float(len(query.split())) > .7:
                    set_response = details 
                    template_id = set_response["template"] 
                    resp = self.return_self_eval( behavior, mood, template_id)   
                    b_self_reflect = True

                if b_self_reflect is False: 
                    resp = get_chat_response(prompt)    
                    resp = [resp]

           if resp[0] == "": 
               response["speech"]  =  ["I could not hear you."]
           else:
              response["speech"]   =  resp

       elif strategy == "quiet": 
            response["speech"] = [ ""] 
       else: 
 
           i_max = len(self.chat["initiate"][strategy]) -1 
           i_index = random.randint(0, i_max) 
           init_response  = self.chat["initiate"][strategy][i_index]["response"]
           response["speech"] = [init_response ] 
           
       i_max = len(self.movement[objective]) -1
       i_index = random.randint(0,i_max)
       response["movement"] =  [self.movement[objective][i_index]] 

       return  response
   
   def built_in_tools(self, prompt): 
        """
        
        """
        response = {"speech" : "", "movement":[]} 
        prompt = prompt.lower()

        if  prompt.startswith('roll 20d'):
            response["speech"] = [str(random.randint(1, 20)) ]
        elif  prompt.startswith('roll 12d'):
            response["speech"] = [str(random.randint(1, 12)) ]
        elif  prompt.startswith('roll 6d'):
            response["speech"] = [str(random.randint(1, 6)) ]
        elif  prompt.startswith('roll 10d'):
            response["speech"] = [str(random.randint(1, 10)) ]
        elif  prompt.startswith('roll 4d'):
            response["speech"] = [str(random.randint(1, 4)) ]
        elif  prompt.startswith('roll 100d'):
            response["speech"] = [str(random.randint(1, 100)) ]
        elif  prompt.startswith('flip'):
            response["speech"] = [str(random.randint(1, 2)) ]
        elif  prompt.startswith('roll 8d'):
            response["speech"] = [str(random.randint(1, 8)) ]
        elif  prompt.startswith(':hello'):
            response["speech"] = ["Hi there!\nMay the dice be with you!" ] 
        return response