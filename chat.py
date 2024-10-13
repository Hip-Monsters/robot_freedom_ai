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
 

import platform
import time 
import json
import os 

from nerves         import Nerves
import pickle 
import string   
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import joblib
import nltk
from nltk.stem import WordNetLemmatizer  
nltk.download('popular', quiet=True)   

import yake 
pyake = yake.KeywordExtractor(lan="en",n=3)

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
    

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-d", "--devices", default="")  
parser.add_argument("-p", "--param", default="")  
 
 
class Chat(object):

    def __init__(self, robot, devices , params =None, polling_rate =.25, fit=False):
        """
        
        """ 
        self.os = "LINUX"
        if platform.system() == 'Windows':
            self.os = "WIN"
        elif platform.system() == 'Darwin': 
            self.os = "OSX" 
 
        self.polling_rate = polling_rate
        self.name     = robot
        self.devices  = devices
        self.nerves   =  Nerves(robot)  
        self.module   = "chat" 

        if fit:
            return None 
        try:
            t = joblib.load( './data/' +  self.name  + '/Query_Response_vec.sav')
        except:
            if not os.path.exists('./data/' +  self.name):
                 os.makedirs('./data/' +  self.name)  
            self.build_models('./data/corpus.json')

        self.load_models()
        return None
    
    def build_models(self, spath):
        """
        
        """
    
        id = 0
        paragraph = ""
        input = []
        response = []
        for line in open(spath):
        
            row =  json.loads(line) 
            input.append(row["query"]    )
            response.append(row["response"]    )
         
        with open('./data/' +  self.name  + '/input.pkl', 'wb') as f:
            pickle.dump(input, f)
        
        with open('./data/' +  self.name  + '/response.pkl', 'wb') as f:
             pickle.dump(response, f)
        print(input)
        QATfidfVec = TfidfVectorizer(tokenizer=LemNormalize, 
                                     ngram_range = (1, 2),
                                     stop_words='english')
        qatfidf    = QATfidfVec.fit_transform(input)
        joblib.dump(qatfidf   , './data/'   +  self.name  + '/Query_Response_vec.sav')
        joblib.dump(QATfidfVec, './data/'   +  self.name  + '/Query_Response_TfidfVec.sav')
        print('Query Response model built')

        
    def load_models(self): 
        """
        
        """
        self.input      = pickle.load(open('./data/' +  self.name  + '/input.pkl', "rb") )
        self.responses  = pickle.load(open('./data/' +  self.name  + '/response.pkl', "rb") )
        self.qatfidf    = joblib.load('./data/' +  self.name  + '/Query_Response_vec.sav')
        self.QATfidfVec = joblib.load('./data/' +  self.name  + '/Query_Response_TfidfVec.sav') 
    
    
    def respond(self, user_response):
      """
      """ 
      try:
        request = self.QATfidfVec.transform([user_response] )
        vals = cosine_similarity(request, self.qatfidf)
         
        idx = vals.argsort()[0][-1]
        flat = vals.flatten()
        flat.sort()
        print("rsp", flat)
        req_tfidf = flat[-1]
        response = "" 

        if(req_tfidf==0): 
            return response
        else: 
            idx = random.randint(1, 20) 
            resp_idx =  vals.argsort()[0][-idx]
            response = response + ' ' + self.responses[resp_idx]  
            return response 
      except:
         return ""
        
    def serve_forever(self): 
        """ 

        """

        while True:
 
           new, cmds = self.nerves.pop(self.module) 
           if new:
               acmds = cmds.split(">") 
               print(acmds)
               if acmds[0] == "respond":
                  response =  self.respond(acmds[1])
                  self.nerves.set(self.module + "_responses", response )  
               self.nerves.set(self.module, "")  

           time.sleep(self.polling_rate)

if __name__ == "__main__":
    """
    python3 chat.py -m serve -r number_3 

    python3 chat.py -m fit -r  number_3 -p ./data/corpus.json 

    python3 chat.py -m test -r number_3 -p "how are you"

    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot   


    if mode == "serve":

        chat  = Chat(robot,  ('/dev/cu.usbmodem14201',"113") ) 
        chat.serve_forever()

    elif mode == "test": 
       
       chat  = Chat(robot,  ('/dev/cu.usbmodem14201',"113") )
       print(chat.respond(args.param ))

    elif mode == "fit": 
       chat  = Chat(robot,  ('/dev/cu.usbmodem14201',"113"), fit=True )
       chat.build_models(args.param)