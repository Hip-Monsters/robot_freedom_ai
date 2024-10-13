#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Description: AI interactions lookup.
Author: HipMonsters.com  
License: MIT License  
"""

import random 
import json
 
# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES =  ["hi", "Drem yol lok (hello)","sup","hey", 
                      "greetings fellow dnd lover!",
                        "hi there", "hello", 
                        "I am glad you are talking to me!"]
TEMPLATES = {}
TEMPLATES["feel"] = {"source":"mood"   , "template": "I feel <INSERT>"}
TEMPLATES["day"]  = {"source":"stimuli", "template": "Today this happened: <INSERT>"}

QUERIES     = {}
QUERIES["how do you feel"]      = {"template":"feel"}
QUERIES["how are you"]          = {"template":"feel"}
QUERIES["how are thing going"]  = {"template":"feel"}
QUERIES["whats up"]             = {"template":"day"}
QUERIES["how was you day"]      = {"template":"day"}
QUERIES["what is happening"]    = {"template":"day"} 


def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

class Interactions(object):
   ""


   ""

   def __init__(self, name, knowledge, config =None, llm=False):
      """
      
      """
      self.name = name
      self.b_llm = llm
      self.knowledge =  knowledge 

      if self.b_llm:
          from llama_cpp  import Llama
          self.llm = Llama("./data/llama.2g.llm")
 
      with open("./data/" + self.name + "/interactions.json") as f:
           data = ''
           for row in f:
              data += row  
           data = json.loads(data)
   
      self.vocalization  = data["vocalization"]
      self.movement      = data["movement"]

      ## erro check
      self.mapped_strategies =  ['Diplomatic', 'Animated', 'Callous', 'Inspirational', 'Apologetic',
                'Cautionary', 'Bitter', 'Belligerent', 'Appreciative', 'Assertive', 
                'Accusatory', 'Amused', 'Admiring', 'Aggressive', 'Apathetic',
                'Caustic', 'Thoughtful', 'Ardent', 'Acerbic', 'Benevolent', 'Absurd',
                'Aggrieved', 'Altruistic', 'Witty', 'Direct', 
                'Angry', 'Ambivalent', 'Candid', 'Informative', 'Arrogant', 'Appreciative.']

      self.chat = {} 
      self.chat["initiate"]= {} 
      self.chat["converse"] = {} 

      with open("./data/" + self.name + "/chat.initiate.json") as f: 
           for data in f:  
              try:
                  row = json.loads(data.strip())
              
                  if row["tone"] not in self.chat["initiate"]:
                       self.chat["initiate"][row["tone"]] = []

                  self.chat["initiate"][row["tone"]].append(row)
              except:
                  print("\r Row error", end = "")

   def get_stimuli_summary(self,  behavior):
       """

       """ 

       stimuli = {}
       for dt , details in behavior.short_term_memory["stimuli"].items():
           stim =   details["stimuli"]
           if stim not in  stimuli:
               stimuli[stim ] = 1
           else:
               stimuli[stim ] = stimuli[stim ] + 1
 
       return stimuli 
    
   def return_self_eval(self, behavior, mood, template_id):
            """
            """
       
            template =  TEMPLATES[template_id]
            
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
   
   def responses(self, topic, catogory, prompt,  behavior, chat, get_chat_response):
       """ 
       """

       response  = {"speach" : "", "movement":[]}
       mood      = behavior.emotions.mood()
       objective = behavior.objective
       strategy  = behavior.strategy 
       
      # print("  " + mood + " " + objective + " "  + strategy + " " + str(chat))

       b_chat = False
       b_set_response = False
       set_response = {}
    
       if type(prompt)  == str:
         if len(prompt)   > 1:
           for query, details in QUERIES.items(): 
             matches = [1 for w in prompt.split() if w in query.split()] 
             if len(matches) / float(len(query.split())) > .7:
                set_response = details
                b_set_response = True
                continue  
             
       if strategy == "quiet":
            rnd =  random.randint(0, 10) 
            response["speach"] = [ ""]
            print("\r I am singing the quiet song! The quiet song! The queit song!", end = "")

       elif b_set_response: 
            
            template_id = set_response["template"] 
            response["speach"] = self.return_self_eval( behavior, mood, template_id)
 
       elif chat:
           resp = get_chat_response(prompt)   

           if resp == "": 
              rnd =  random.randint(0, 10)
              if rnd < 4:
                 i_max = len(self.chat["initiate"][strategy]) -1 
                 i_index = random.randint(0, i_max) 
                 response["speach"]  = self.chat["initiate"][strategy][i_index]["response"]
              else:
                  i_max = len(TEMPLATES.keys()) -1 
                  rnd_id = random.randint(0, i_max)  
                  template_id = list(TEMPLATES.keys())[rnd_id]
                  response["speach"] = self.return_self_eval( behavior, mood, template_id)

           else:
              response["speach"]  =  [resp]


       else: 

           if strategy  in self.chat["initiate"] and b_chat is False:
              
              ## eventually filter be topics - experience will do mood
              i_max = len(self.chat["initiate"][strategy]) -1 
              i_index = random.randint(0, i_max) 
              response["speach"]  = self.chat["initiate"][strategy][i_index]["response"]
               
           else:   
              if strategy not in self.vocalization:
                  print("We are missing a stratgey for basic_interaction " + strategy )
                  strategy = list(self.vocalization.keys())[0]
                  
              i_max = len(self.vocalization[strategy]) - 1  

              if i_max < 0:
                  response["speach"]  = []
              else:
                  i_index = random.randint(0,i_max)
                  response["speach"]  =  [self.vocalization[strategy][i_index]]

           self.chat

       i_max = len(self.movement[objective]) -1
       i_index = random.randint(0,i_max)
       response["movement"] =  [self.movement[objective][i_index]]
     #  print(response["movement"] )

       with open("./data/" + self.name + "/actions.json", "a") as f:
           f.write(json.dumps({"topic": topic,
                                "catogory ":catogory ,
                                "mood ":mood ,
                                "objective ":objective ,
                                "prompt":prompt ,
                                "stimui_time" : str(behavior.stimui_time),
                                "response":response  }) + "\n")
           
       return  response
   
   def command_responses(self, prompt): 
                """
                
                """
                response = {"speach" : "", "movement":[]} 
                if  prompt.startswith('roll 20d'):
                    response["speach"] = [str(random.randint(1, 20)) ]
                elif  prompt.startswith('roll 12d'):
                    response["speach"] = [str(random.randint(1, 12)) ]
                elif  prompt.startswith('roll 6d'):
                    response["speach"] = [str(random.randint(1, 6)) ]
                elif  prompt.startswith('roll 10d'):
                    response["speach"] = [str(random.randint(1, 10)) ]
                elif  prompt.startswith('roll 4d'):
                    response["speach"] = [str(random.randint(1, 4)) ]
                elif  prompt.startswith('roll 100d'):
                    response["speach"] = [str(random.randint(1, 100)) ]
                elif  prompt.startswith('flip'):
                    response["speach"] = [str(random.randint(1, 2)) ]
                elif  prompt.startswith('roll 8d'):
                    response["speach"] = [str(random.randint(1, 8)) ]
                elif  prompt.startswith(':hello'):
                    response["speach"] = ["Hi there!\nMay the dice be with you!" ]
                elif  prompt.startswith(':iamcool'):
                    response["speach"] = ["Keyleth and Synthrin are awesome!" ]
                elif  prompt.startswith(':i am cool'):
                    response["speach"] = ["Sky of a Sunset and Xylxina are awesome!" ]
                elif  prompt.startswith(':Cinder'):
                    response["speach"] = ["Cinder is a cute cat!" ]
                elif  prompt.startswith(':Maddie'):
                    response["speach"] = ["Maddie is an amazing kitten!" ]
                elif  prompt.startswith(':you can say that again'):
                    response["speach"] = ["keyleth and synthrin are awesome!" ]
                elif  prompt.startswith(':you can say that again!'):
                    response["speach"] = ["sky of a sunset and xylxina are awesome!" ]
                    
                return response