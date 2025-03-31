#!/usr/bin/python
# -*- coding: utf-8 -*- 
  
"""
Description: This builds and controls a simple chatbot design to run on a RaspberryPi.
Author: HipMonsters.com 
Date Created: Jan 1, 2021
Date Modified: Oct 10, 2024
Version: 8.0
Platform: RaspberryPi
License: MIT License  
""" 
import glob
import csv
import json
import os  
import pickle 
import string   
import random 
import sys 
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
import joblib
import nltk
from nltk.stem import WordNetLemmatizer  
nltk.download('popular', quiet=True)  

if __name__ == "__main__": 
    from lib.text_utilities import *
else:
    from .lib.text_utilities import * 
 

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer() 
 
# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    """
    """
    return [lemmer.lemmatize(token) for token in tokens]
    
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text): 
    """
    """
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
    
  
class LTMemory(object):

    def __init__(self,name, config,  low_memory_mode, log=True, repeat_log= True ):
        """
        
        """     
        self.name         = name
        self.log          = True 
        self.verbose      = False 
        self.low_memory_mode = low_memory_mode
        self.context_db   = False

        self.config = config

        self.facts_path = "__default/"  
        try:
            t = joblib.load( self.config.CHAT_PATH +  self.facts_path  + 'facts.QATfidfVec.sav')
        except:
            if not os.path.exists(self.config.CHAT_PATH +  self.facts_path):
                 os.makedirs(self.config.CHAT_PATH +  self.facts_path)   
            self.build_models_facts()

        self.personality_path = self.name +"/"
        try:
            t = joblib.load( self.config.CHAT_PATH +  self.personality_path  + 'personality.QATfidfVec.sav')
        except:
            if not os.path.exists(self.config.CHAT_PATH +  self.personality_path):
                 os.makedirs(self.config.CHAT_PATH +  self.personality_path)   
            self.build_models_conversations()
        
        self.memory = {}
        self.memory["facts"]       = {}
        self.memory["personality"] = {}
        self.memory["initiate"]    = {} 
        self.memory["converse"]    = {} 


        self.set_chat_responses = {}
        self.set_chat_responses["greeting_input"] = ("hello", "hi", "greetings", "sup", "what's up","hey",)
        self.set_chat_responses["greetings_response"] =  ["hi", "Drem yol lok (hello)","sup","hey", 
                                                           "greetings fellow dnd lover!",
                                                          "hi there", "hello", 
                                                          "I am glad you are talking to me!"]
        self.set_chat_responses["templates"] = {}
        self.set_chat_responses["templates"]["feel"] = {"source":"mood"   , "template": "I feel <INSERT>"}
        self.set_chat_responses["templates"]["day"]  = {"source":"stimuli", "template": "Today this happened: <INSERT>"}

        self.set_chat_responses["queries"]     = {}
        self.set_chat_responses["queries"]["how do you feel"]      = {"template":"feel"}
        self.set_chat_responses["queries"]["how are you"]          = {"template":"feel"}
        self.set_chat_responses["queries"]["how are thing going"]  = {"template":"feel"}
        self.set_chat_responses["queries"]["whats up"]             = {"template":"day"}
        self.set_chat_responses["queries"]["how was you day"]      = {"template":"day"}
        self.set_chat_responses["queries"]["what is happening"]    = {"template":"day"} 
 
 
        convo_init_file = self.config.CHAT_PATH + self.facts_path + "/chat.initiate.json"
        mapped_tones = set([])
        with open(convo_init_file) as f:  
             for data in f:  
                try:
                    row = json.loads(data.strip())
                
                    if row["tone"] not in self.memory["initiate"]:
                         self.memory["initiate"][row["tone"]] = [] 
                         mapped_tones.add(row["tone"])
  
                    if self.low_memory_mode:
                        if len(self.memory["initiate"][row["tone"]]) >= 10:
                           break   
                    self.memory["initiate"][row["tone"]].append(row) 
                except:
                     print("\r Row error",  data.strip(), end = "")
        print(mapped_tones)
        self.load_models()
        """
        TODO Add love
        {'Appreciative', 'Assertive', 'Inspirational', 'Amused', 'Bitter', 'Acerbic',
          'Aggrieved', 'Appreciative.', 'Animated', 'Altruistic', 'Callous', 'Apologetic', 
          'Candid', 'Benevolent', 'Direct', 'Witty', 'Cautionary', 'Ardent', 'Thoughtful', 
          'Absurd', 'Admiring', 'Angry', 'Diplomatic', 'Aggressive',
          'Arrogant', 'Caustic', 'Ambivalent', 'Belligerent', 'Apathetic', 'Informative', 'Accusatory'}
        add love
        """
        return None
    
    def build_models_conversations(self):
        """
        
        """ 
        input = []
        response = []
 
        root_path = self.config.CHAT_PATH + self.personality_path  
                                      
        for  file_path in list(glob.glob(root_path + "*.csv")):         
            with open(file_path, 'r') as DictReader: 
            
              in_data = csv.DictReader(DictReader, 
                                       delimiter=',', 
                                       quotechar =  '"',
                                       skipinitialspace=True,
                                       quoting=csv.QUOTE_ALL,
                                       doublequote = True)
              duels = []
              for row in in_data:  
                  if row["actor"] == "human":
                      res = {"human" : row["value"]}
                  else:
                      res["ai"] = row["value"]
                      duels.append(res)
                 
              for row in duels:
                  input.append(row["human"]    ) 
                  response.append(row["ai"]    )  
              print(input[-1])
         
        with open(self.config.CHAT_PATH + self.personality_path  + 'personality.input.pkl', 'wb') as f:
            pickle.dump(input, f)
        
        with open(self.config.CHAT_PATH +  self.personality_path  + 'personality.response.pkl', 'wb') as f:
             pickle.dump(response, f)
        
        QATfidfVec = TfidfVectorizer(tokenizer=LemNormalize, 
                                     ngram_range = (1, 2),
                                     stop_words='english')
        qatfidf    = QATfidfVec.fit_transform(input)
        joblib.dump(qatfidf   , self.config.CHAT_PATH +  self.personality_path  + 'personality.qatfidf.sav')
        joblib.dump(QATfidfVec, self.config.CHAT_PATH +  self.personality_path  + 'personality.QATfidfVec.sav')
 
    
    def build_models_facts(self):
        """
        
        """

        root_path = self.config.CHAT_PATH + self.facts_path

        input    = []
        response = [] 

        for file_path in list(glob.glob(root_path + "facts.json")):                                     
            print("loading", file_path )                                      
           
            for line in open(file_path): 
                row =  json.loads(line) 
                input.append(row["query"] )
                response.append(row["response"] )
            print(input[-1]) 
         
        with open(self.config.CHAT_PATH +  self.facts_path  + 'facts.input.pkl', 'wb') as f:
            pickle.dump(input, f)
        
        with open(self.config.CHAT_PATH + self.facts_path  + 'facts.response.pkl', 'wb') as f:
             pickle.dump(response, f)
        
        QATfidfVec = TfidfVectorizer(tokenizer=LemNormalize, 
                                     ngram_range = (1, 2),
                                     stop_words='english')
        qatfidf    = QATfidfVec.fit_transform(input)
        joblib.dump(qatfidf   , self.config.CHAT_PATH +   self.facts_path  + 'facts.qatfidf.sav')
        joblib.dump(QATfidfVec, self.config.CHAT_PATH +   self.facts_path  + 'facts.QATfidfVec.sav')
        print('Query Response model built')

        
    def load_models(self): 
        """
        
        """
        ### Right side
        self.memory["facts"]["input"]      = pickle.load(open(self.config.CHAT_PATH + self.facts_path  + 'facts.input.pkl', "rb") )
        self.memory["facts"]["responses"]  = pickle.load(open(self.config.CHAT_PATH + self.facts_path  + 'facts.response.pkl', "rb") )
        self.memory["facts"]["qatfidf"]    = joblib.load(self.config.CHAT_PATH      + self.facts_path  + 'facts.qatfidf.sav')
        self.memory["facts"]["QATfidfVec"] = joblib.load(self.config.CHAT_PATH      + self.facts_path  + 'facts.QATfidfVec.sav') 
    
        ## How you have responded in the past
        self.memory["personality"]["input"]       = pickle.load(open(self.config.CHAT_PATH  + self.personality_path  + 'personality.input.pkl', "rb") )
        self.memory["personality"]["responses"]   = pickle.load(open(self.config.CHAT_PATH  + self.personality_path  + 'personality.response.pkl', "rb") )
        self.memory["personality"]["qatfidf"]     = joblib.load(self.config.CHAT_PATH       + self.personality_path  + 'personality.qatfidf.sav')
        self.memory["personality"]["QATfidfVec"]  = joblib.load(self.config.CHAT_PATH       + self.personality_path  + 'personality.QATfidfVec.sav') 
        

    def _get_input_and_response(self, memory_type , query, max_return=10):

     # try:
      
        query = [query]
        request = self.memory[memory_type]["QATfidfVec"].transform(query) 
        #request = request.reshape(1, -1)
        vals    = cosine_similarity(request, self.memory[memory_type]["qatfidf"] ) 
        idxs = vals.argsort()[0][-max_return:]
 
        scrs_r = [vals[0][idx] for idx in idxs ]  

        ### Todo then rank based on how close the query is to orginal
        scrs_q = [vals[0][idx] for idx in idxs ]  

        response = ""   

        if (idxs[-1]==0):  
            return [response, 0.0] 
        else:  
            results = [(self.memory[memory_type]["input"][idxs[i]] , self.memory[memory_type]["responses"][idxs[i]] , scrs_r[i], scrs_q[i]) for i , v in enumerate(idxs) if  scrs_r[i] > .2]
            return results 
        
    def _get_top_responses(self, memory_type , user_response, max_return=10):
        """
        """
        user_response = [user_response]
        request = self.memory[memory_type]["QATfidfVec"].transform(user_response  ) 
        #request = request.reshape(1, -1)
        vals    = cosine_similarity(request, self.memory[memory_type]["qatfidf"] )
         
        idxs = vals.argsort()[0][-max_return:]
 
        scrs = [vals[0][idx] for idx in idxs ]  
        response = ""   

        if (idxs[-1]==0):  
            return [response, 0.0] 
        else:   
            
            results = [(self.memory[memory_type]["responses"][idxs[i]] , scrs[i]) for i , v in enumerate(idxs) if  scrs[i] > .2]
          
            return results 
 
    def query(self, user_response, max_resp =10,  input_types =["personality", "facts"]):
      """
      """   
      fin = []
      for stype in input_types:
          resp1  = self._get_input_and_response(stype , user_response, max_resp) 
          fin += resp1   
      fin = sorted(fin, key=lambda x: x[1], reverse=True)
      fin = fin[:max_resp] 
      return [{"query": q.strip(), "response": r.strip(), "src":s} for  q , r, s, s2  in fin]

    def add_tone(self, response, tone):
        ## Todo Create a tone adjuster for tone- change words? add in a snarky or friendly end?
        return response
    
    def respond(self,  user_response, mood, tone, topics, objective, lexicon):
        return self.response(user_response, mood, 
                             tone, topics, objective, lexicon) 


    def response(self, user_response, mood, tone, topics, objective, lexicon):
      """
      """  
 
      user_response     = cleanup_prompt(user_response, "") 
      b_alt = False
      user_response_alt =  user_response
      if mood != "":
         user_response_alt  += " " + mood  
         b_alt = True

      if len(topics) > 0:
         user_response_alt  +=  " ".join(topics)
         #b_alt = True

      if b_alt:
         resp1a  = self._get_top_responses("personality" , user_response_alt)
         resp2a  = self._get_top_responses("facts"       , user_response_alt)

      resp1 = self._get_top_responses("personality" , user_response)
      resp2 = self._get_top_responses("facts"       , user_response)
      # randomize should be in another call 
      if resp1[-1] >= resp2[-1]:
          return self.add_tone(resp1[-1][0], tone)
      else: 
          return self.add_tone(resp2[-1][0], tone)
           
if __name__ == "__main__":
    """ 

    """ 
 
    os.chdir('../')
    sys.path.insert(0, os.path.abspath('./')) 
    import config

    topics = ["cats"]
    objective = "engage"
    mood = "happy"
    tone ="friendly"
    lexicon = "simple"
    lt_mem  = LTMemory("squirrel", config,    topics )  
 
    user_response =  lt_mem.query("you, feel, cats" )
    print(user_response)

    user_response =  lt_mem.response("how do you feel about cats?" , 'mood', 'tone', 'topics', 'objective',   'lexicon')
    print(user_response)

    """ 
    user_response = "I love cats!"
    print(user_response)
    for i in range(10): 
        user_response =  lt_mem.response(user_response,mood, tone, topics, objective, lexicon)
        print(user_response)
    """