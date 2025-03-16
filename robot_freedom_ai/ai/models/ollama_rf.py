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
import warnings
warnings.filterwarnings("ignore") 
import csv
import time  
import os    
import random  
import shutil  
import sys 

if __name__ == "__main__":  
    from lib.text_utilities import *
else:
    from .lib.text_utilities import *
 

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM  
from sklearn.metrics.pairwise import cosine_similarity 
import nltk 

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
try:
   nltk.download('popular', quiet=True)    
except:
    pass

import yake 
kw_extractor = yake.KeywordExtractor(lan="en",n=1) 


is_noun = lambda pos: pos[:2] == 'NN'  
ROBOT_ROLES = ["interviewing", "educating", "conversing"]   
ROLES       =  ["ai","response", "robot" , "assistant" ,  "machine" , "two", "three", "four", "with",
                "stranger",   "man", "human", "system", ]  
 
def input_cleanup(input):
    """
    
    """
    return input 

class OllamaRF(object):
    """
    
    """ 

    def __init__(self, config, cognitive_control, personality, lt_memory, st_memory, 
                 full_name, name ,topics , tones=["Appreciative"], 
                  params= {},   log=True, repeat_log= True):
        """
 
        """ 
        self.log          = True
        self.tones        = tones
        self.verbose      = False 
        self.low_mem_mode = False
        self.context_db   = False
        self.config       = config
        self.cognitive_control    = cognitive_control
        self.personality  = personality
        self.persona      = personality.persona
        self.st_memory    = st_memory
        self.lt_memory    = lt_memory

        self.memory        = self.lt_memory.memory  
        self.model_path    = name  

        self.os            = self.config.OS 
        self.roles         = ROLES  

        self.resp_fit_threshold = .7
        self.llm_tries = 6
        self.assure_question = True
        self.min_resp_len = 2
        self.min_overlap = .55
        self.min_key_wrd_scr = .04


        if 'input_cleanup' in params: 
           self.input_cleanup =  params["input_cleanup"] 
        else:
           self.input_cleanup = input_cleanup 

        self.cleanup       = ["'",  "`",  '"']

        self.p_topics   = []
        self.p_topics_2 = []
        self.r_topics_2 = []
        self.r_topics   = []

        if self.os == 'LINUX': 
            self.verbose = False
            self.low_mem_mode = True
 
        self.base_template = [ {'role': "system", 
                        'content': "You are a {mood} robot {tone}.  {persona} {situation} Your name is " + full_name +"." },
                        ]    
        
        self.just_the_facts_template =  [("system", "You are a robot who responds quickly" ),
                                         ("human", "{topic}"),
                                         ("ai", "")
                                       ]    
        if len(topics) > 0: 
            self.base_template = [ {'role': "human", 
                          'content': "Please try to stay on the topic of " + topics[0].replace('_', " ")  +"." },
                        ] 
            self.base_template = [ {'role': "ai", 
                          'content': "I will try and stay on the topic of " + topics[0].replace('_', " ")  },
                        ] 

 
        self.log_name = "chat_ollama.log"
        if repeat_log == False:
            if os.path.exists(self.log_name): 
                 _log_name = "chat_ollama." + self.config.START_DT_F + ".log"
                 dest = shutil.move(self.log_name, _log_name)   

        f_log = open(self.config.LOGS_PATH + self.log_name, "a")
        f_log.write("Started new session\n")  
        f_log.close()

        self.load_models(name , params, topics, tones)
        
        
    def load_models(self,robot, params, topics, tones=[]): 
        """
        
        """     
        self.prompts_end  = []
        self.prompts_end.append( ("human", "{topic}"))
        self.prompts_end.append( ("ai", "")) 

        self.model_just_the_facts   = OllamaLLM(model="just_the_facts", 
                                                temperature=0.8,  
                                                 num_predict=19) 
        
        self.prompt_just_the_facts = ChatPromptTemplate(self.just_the_facts_template )
        self.chain_just_the_facts = self.prompt_just_the_facts | self.model_just_the_facts
        
        self.reset_prompt(robot, params, topics, tones)

    def reset_prompt(self,robot, params, topics, tones=[]): 
        """
        
        """    
        self.tones  = tones
        self.topics = topics
        self.params = params
        self.robot  = robot 

        prompts = []
        for message in self.base_template:
            prompts.append( (message["role"], message["content"]) )

        human_resp =["Hello. How are you?",  
                     "What are you thinking about?",
                     "What did you say?",
                     "Do you have any thoughts?"
                     "How are you?",
                     "It is a great day!",
                     "How do you feel?",
                     "Any ideas?",
                     "I feel happy.",
                     "Lets do something!"]
        i_starts = len(human_resp) - 1
        i_num = 0
        if len(tones)  > 0 :
            for tone in tones: 
               for row in self.memory["initiate"][tone]:
                   i = random.randint(0, i_starts)
                   prompts.append( ("human", human_resp[i]) )  
                   prompts.append( ("ai", row["response"][0]) ) 
                   i_num += 1
                   if i_num > 1:
                       break
                        
        self.prompts = prompts  
        self.prompt  = ChatPromptTemplate(self.prompts + self.prompts_end )

        if self.low_mem_mode:  
            self.model  = OllamaLLM(model="tinyllama", 
                               temperature=0.8,  
                               num_predict=19) 

        else:  
            arg = self.config.CHAT_PATH +  self.model_path  + "/" + robot + ".base.csv" 
            with open(arg, 'r') as DictReader:  
                    in_data = csv.DictReader(DictReader, 
                                             delimiter=',', 
                                             quotechar =  '"',
                                             skipinitialspace=True,
                                             quoting=csv.QUOTE_ALL,
                                             doublequote = True)
                   
                    for row in in_data: 
                        prompts.append( (row["actor"], row["value"]) )  

            if len(topics) > 0: 
  
                for topic in topics:
                    topic = "stuffed_animals"  
                    arg = self.config.CHAT_PATH +  self.model_path  + "/" + robot + "." + topic + ".csv"

                    if os.path.exists(arg) is False: 

                        in_data = self.lt_memory.query(topic)
                        for row in in_data: 
                             prompts.append( ("human", self.input_cleanup(row["query"]) ))  
                             prompts.append( ("ai"   , self.input_cleanup(row["response"])) )  

                    else:
                        with open(arg, 'r') as DictReader:  
                            in_data = csv.DictReader(DictReader, 
                                                     delimiter=',', 
                                                     quotechar='"',
                                                     skipinitialspace=True,
                                                     quoting=csv.QUOTE_ALL,
                                                     doublequote=True)
                       
                            for row in in_data: 
                                prompts.append( (self.input_cleanup(row["actor"]), 
                                                 self.input_cleanup(row["value"])) )  
            print(prompts)
          
            self.prompts = prompts  
            self.prompt = ChatPromptTemplate(self.prompts + self.prompts_end ) 
            self.model  = OllamaLLM(model="tinyllama", 
                                    temperature=0.9,  
                                    num_predict=130)
 
        self.chain = self.prompt | self.model
        return True   
  
    
    def parse_response(self, response):
        """
        
        """
        _response = ""
        resp      = ""

        if response.find(":") > -1:
           parsed =  parser(response) 
           for role in self.roles:  
               if role in parsed: 
                   _response = return_sentence(parsed[role], self.p_topics)   
                   if len(_response.split(" ")) > 3:
                       resp      = _response  
                       break    
        else:
            resp = return_sentence(response, self.p_topics) 
     
        if resp == "" or resp.lower().startswith('system:'): 
            resp = "I am sorry could you repeat what you said?" 

        return resp
     
    def respond(self, user_response,
                   mood="happy",
                   tone="Appreciative",
                   user_topics=[],
                   objective ="relax",
                   lexicon="Appreciative",
                   situation = "You are having a chat with your friends."  ): 
      
      org_user_response = user_response  
      user_response     = cleanup_prompt(user_response, "")
      
      objective_to_situation   =   {"enguagement":  "You want to encourage the conversation forward.", 
                                    "defuse": "You are helping a friend with a problem." , 
                                    "inspire" :  "You want to insipre people.",
                                    "relax" : "You want to keep everyone calm.",  
                                    "disenguagement":  "You are trying to get someone to relax." ,  
                                    "quiet":  "You are trying to get someone to be quiet." } 
       
      situation = objective_to_situation[objective]
           
      if self.verbose:
            print( mood ,tone , user_topics ,objective  , lexicon ,  situation  )

      if len(user_topics) == 0:
          if len(self.tones) >  0:
              if  tone != self.tones[0]:  
                  self.reset_prompt(self.robot, self.params, self.topics, [tone]) 
        
      elif user_topics[0] != self.topics[0] or  tone != self.tones[0]:   
          self.reset_prompt(self.robot, self.params, user_topics, [tone]) 

      try:
        
          if self.verbose: 
             start = time.time() 
          
          if len(user_topics) == 0 and  self.low_mem_mode is False:
              keywords = kw_extractor.extract_keywords(user_response)    

              self.p_topics_2 = self.p_topics 
              if len(keywords) > 0: 
                   self.p_topics = list(set([wrd for wrd , scr in keywords if scr > self.min_key_wrd_scr ] ))

              if len(self.p_topics) ==0:
                  self.p_topics = ["cats"]  
 
              tokenized = nltk.word_tokenize(" ".join(self.p_topics))
              _p = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
              if len(_p) > 0:
                  self.p_topics = _p  
          else:
              self.p_topics = user_topics

          if self.verbose: 
             end = time.time()
             print(end - start) 
             print(mood, tone, self.persona, situation, self.p_topics)

          if self.context_db:
              memory =  self.lt_memory.query(self.p_topics) 
              if len(memory) > 0:
                  self.prompt = ChatPromptTemplate(self.prompts + self.prompts_end )
                  self.chain = self.prompt | self.model  
                

          user_response  = user_response.strip()

          if user_response[-1] not in [".", "!" ,"?"]: 
              user_response = user_response + "."

          if user_response[-1] != "?" and self.assure_question:
              user_response = user_response + " What are your thoughts?"  

          if self.low_mem_mode:      
              response = self.chain.invoke({"topic":user_response ,
                                             "mood":mood,
                                             "tone":tone,
                                             "persona":self.persona,
                                             "situation":situation})
                                               # "lexicon":lexicon   }) 
              ai_response = self.parse_response(response)
              
          else:  

              _res =  [-1, "I dont understand", "Error"] 
              
              all = []
              persona = self.persona
              _tone = f"who responds in a {tone} manner"  
             # print(user_response)
              for i in range(self.llm_tries): 
                  
                  if i == 2:
                       persona = ""

                  if i == 3:
                       situation = ""

                  if i == 4:
                       _tone  = "" 
  
                  if 3==4:#i == self.llm_tries - 1:
                      t_user_response = "Please provide a response on the followig topics:  " + ",".join(self.p_topics) +"."
                      response = self.chain_just_the_facts.invoke({"topic":t_user_response})
                      
                  else:
                      response = self.chain.invoke({"topic":user_response ,
                                                      "mood":mood,
                                                      "tone":_tone,
                                                      "persona": persona,
                                                      "situation":situation })#,
                                                     #"lexicon":lexicon   } )  
                  ai_response = self.parse_response(response)  
              #    print(ai_response)
                  i_len_rsp = len(ai_response)
                  adj   = 1/float(i_len_rsp)
                  
                  if i_len_rsp < self.min_resp_len : 
                       ai_response = "I am not sure I am following what you said."  
                       all.append([ai_response, response, -1])
                       continue 
                  
                  mx_src = -1  
                  
                  for topics in  [self.p_topics]: 
                     if len(topics) > 0:
                         fnd = 0  
                         for topic in topics:
                             if  ai_response.lower().find(topic) > -1: 
                                 fnd += 1.0 
                         t = float(fnd) / float(len(topics))  
                         t = t*adj  
                         if t > mx_src:
                              mx_src = t  
                         if t > self.resp_fit_threshold:
                              break  
                         
                  all.append([ai_response, response, mx_src])
                  if mx_src > self.resp_fit_threshold:
                       break   
                  
              all = sorted(all, key = lambda x : x[2] , reverse =True )  

              ai_response = all[0][0]  
              response    = all[0][1]   
               
              self.prompts.append(('ai', ai_response)) 
              self.prompt = ChatPromptTemplate(self.prompts + self.prompts_end )
              self.chain = self.prompt | self.model

              keywords = kw_extractor.extract_keywords(ai_response)    
              self.r_topics_2 = self.r_topics 

              if len(keywords) > 0: 
                   self.r_topics = list(set([wrd for wrd, scr in keywords if scr > self.min_key_wrd_scr]))
                   
                   tokenized = nltk.word_tokenize(" ".join(self.r_topics))
                   _p = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
                   if len(_p) > 0:
                        self.r_topics = _p  

                         
          if self.log:
              f_log = open(self.config.LOGS_PATH + self.log_name, "a")  

              org_user_response.replace('"', "'") 
              for rule in self.cleanup:
                  org_user_response.replace(rule, "") 
                  user_response.replace(rule, "") 
                  ai_response.replace(rule, "")
                  response.replace(rule, "") 
  
              f_log.write('human,speak,"'   + user_response + '"\n')   
              f_log.write('ai,speak,"'      + ai_response  + '"\n')  
              f_log.write("<topics> " + ','.join(self.p_topics) + ";" + ','.join(self.r_topics) +"</topics>\n")
              f_log.write("<full_prompt>" + org_user_response + "</full_prompt>\n")  
              f_log.write("<full_response>" + response + "</full_response>\n\n")  
            
          return ai_response  
          
      except Exception as e:
           print(e) 
           print(response)
           print(ai_response)   
         
           return "Error in LLM" 
           
if __name__ == "__main__": 
    """ 

    """ 
    os.chdir('../../')
    sys.path.insert(0, os.path.abspath('./')) 
    import config
    from ai.cognitive_control import CognitiveControl 
    from ai.personality import Personality 
    from memory.st_memory import STMemory
    from memory.lt_memory import LTMemory

    st_mem     =  STMemory("squirrel", config, False)
    mem        =  LTMemory("squirrel", config, False) 
    personality   = Personality("squirrel", config, {} )
    cognitive_control  = CognitiveControl("squirrel", config, {}, personality,False) 
    chat  = OllamaRF(config, cognitive_control , personality , mem , st_mem , 
                     "Sqirrel" , 'squirrel', [],  [] , True, repeat_log=False)
  
    for user_input in [ "what pet do you like?" , 
                       "i live in san francisco.", 
                       'i like cats.', 
                       'where is the screw driver.', 
                       'where do i live?',
                       'what pets do i like?',
                       'Where is the capital of France?']:
 
        print('CHAT: ' + user_input)
        resp = chat.respond(user_input)  
        print("RESP : " + resp) 

    while True:
         
       user_input = input('CHAT: ') 
       resp = chat.respond(user_input) 
       print("RESP : " + resp)  
     
  