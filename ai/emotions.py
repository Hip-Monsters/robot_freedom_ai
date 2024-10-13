#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Description: AI Emotions interface.
Author: HipMonsters.com  
License: MIT License  
"""
import os
import datetime 
import json
 

class Emotions():

   def __init__(self, name , short_term_memory):
       """
       
       """
       self.name              = name
       self.short_term_memory = short_term_memory  

       if "emotions" not in   self.short_term_memory  : 
            self.short_term_memory["emotions"] = {}  

       data = []

       if not os.path.exists("./data/" + self.name + "/moods.json"):
          f =  open("./data/" + self.name + "/moods.json", 'w')   
          f.close()

       with open("./data/" + self.name + "/moods.json") as f:
          
           for line in f: 
               try:
                   row = json.loads(line)
                   data.append(row) 
                   self.short_term_memory["emotions"][row["stimui_time"]]  =  row 
               except: 
                  print("Warning a moods memory is corrupt!")
 
       self.moods         = {}
       if len(data) == 0:
          self.moods = {"happy": 0.5, "sad": 0.0, "fear": 0.0, "disgust" : 0.0, "anger" : 0.0, 
                        "bored": 0.0, "surprised" : 0.0, "stimui_time" : "initial"  , "epoch" : -1}
       else:
          self.moods = data[-1] 
       # {"happy": 0.5, "sad": 0.0, "fear": 0.0, "disgust" : 0.0, "anger" : 0.0, 
       # "bored": 0.0, "surprised" : 0.0, "stimui_time" : "initial"  , "epoch" : -1}


       self.emotion_factors = {}
       self.emotion_factors["sense"] = {}
       self.emotion_factors["sense"]["noise"]     = {"sad": [0   ,.05] , "surprised": [1 , .05] , "bored": [-1, .01] , "fear": [1  ,.05] , "happy": [0, .05] , "disgust": [0 , .05]  } 
       self.emotion_factors["sense"]["speech"]    = {"sad": [-1  ,.05] , "surprised": [0 , .05] , "bored": [-1, .01] , "fear": [-1 ,.05] , "happy": [1, .05] , "disgust": [0 , .05]  }
       self.emotion_factors["sense"]["quiet"]     = {"sad": [1   ,.05] , "surprised": [-1, .05] , "bored": [ 1, .05] , "fear": [0  ,.05] , "happy": [-1, .05], "disgust": [1 , .05]  }
       self.emotion_factors["sense"]["movement"]  = {"sad": [0   ,.05] , "surprised": [1 , .05] , "bored": [-1, .05] , "fear": [1  ,.05] , "happy": [0, .05] , "disgust": [0 , .05]  }
       self.emotion_factors["sense"]["distance"]  = {"sad": [1   ,.05] , "surprised": [-1, .05] , "bored": [-1, .05] , "fear": [-1 ,.05] , "happy": [1, .05] , "disgust": [-1, .05]  }
       self.emotion_factors["sense"]["tempature"] = {"sad": [-1  ,.05] , "bored": [1, .05] }
       self.emotion_factors["sense"]["humidity"]  = {"sad": [-1  ,.05] , "bored": [1, .05] }
       self.emotion_factors["sense"]["touch"]     = {"sad": [-1  ,.05] , "bored": [1, .05] }
       self.emotion_factors["sense"]["balence"]   = {"sad": [-1  ,.05] , "surprised": [1, .05] , "bored": [1, .05] }
       self.emotion_factors["sense"]["light"]     = {"sad": [-1  ,.05] , "bored": [1, .05] }
     

   def save(self , stimui_time , epoch ):
      """
      
      """
      str_stimui_time = str(stimui_time)
      self.moods["stimui_time"] = str_stimui_time  
      self.moods["epoch"]       = epoch  

      if "emotions" not in self.short_term_memory:
          self.short_term_memory["emotions" ] = {}

      self.short_term_memory["emotions"][str_stimui_time] = self.moods 
    
      with open("./data/" + self.name + "/moods.json", "a" ) as f:
          f.write(json.dumps(self.moods  )  + "\n")
       
   def stimuli(self, stimuli , stimuli_class, amplitude ,emotional_surpressors  ):
       """
       
       """


       for mood, factor in self.emotion_factors[stimuli][stimuli_class].items(): 
              if factor[0] == 1:
                 self.moods[mood] = self.moods[mood]  +  amplitude*factor[1]
              else:
                 self.moods[mood] = self.moods[mood]  -  amplitude*factor[1]

              self.moods[mood]  = round( self.moods[mood], 2)  
              if  self.moods[mood] <0:
                   self.moods[mood] = 0
              if  self.moods[mood] > 100:
                   self.moods[mood] = 100
       
                      

       for factor, wieght in emotional_surpressors.items():  
          
          if factor in  self.moods:
              mood = factor
              self.moods[mood] = self.moods[mood]  +  self.moods[mood]*wieght  
              self.moods[mood]  = round( self.moods[mood], 2)  
              if  self.moods[mood] < 0:
                   self.moods[mood] = 0
              if  self.moods[mood] > 100:
                   self.moods[mood] = 100
       
            
            
   def reflection(self, met , unmet ,indif, amplitude  ):
       """
       
       """
       val     = 0.0
       i_met   = len(met)
       i_unmet = len(unmet)
       i_indif = len(indif)
       # should get from experience
       if i_met < i_unmet:
            
          self.moods["fear"]                =  self.moods["fear"]    + amplitude
          self.moods["happy"]               =  self.moods["happy"]   -  amplitude 
       else:
             
          self.moods["fear"]                =  self.moods["fear"]    - amplitude
          self.moods["happy"]               =  self.moods["happy"]   + amplitude

       
       
   def mood(self):
       """
       
       """
       t_moods =  [[key, val] for key, val in self.moods.items() if key not in ['epoch','stimui_time'] ]
       moods = sorted(t_moods, key=lambda item: item[1]) 
       self.current_mood  = moods[-1][0] 

       return  self.current_mood
        
