#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Description: AI Emotions interface.
Author: HipMonsters.com  
License: MIT License  
""" 

class Emotions():

   def __init__(self, robot ,cognitive_control, moods, personality , low_memory_mode):
       """
       
       """
       self.robot        = robot  
       self.personality = personality
       self.discount    = personality.discount
       self.novelty     = 1 - self.discount 
       self.moods       = moods 

       self.cognitive_control   = cognitive_control
       self.G                   = self.cognitive_control.G 
       self.low_memory_mode   = low_memory_mode    
        
       self.emotion_factors =  self.cognitive_control.emotion_factors
       self.emotion_flip    =  self.cognitive_control.emotion_flip

   def save(self , stimuli_time , epoch ):
      """
      
      """
      return None  
       
   def stimuli(self, stimuli , stimuli_class, 
               amplitude ,emotional_suppressors  ):
       """
       
       """ 

       edges = [(u2,v2,e2) for u2,v2,e2  in [self.G.edges(v, data=True ) for u,v,e in self.G.edges("emotion_factors", data=True)  if v == stimuli_class  ][0] if e2["class"] == "emotion_factors"]
       
       ## how much you can control you emotions
       abj_fac = .001
       for frm, trait, prop in edges:
            if frm != stimuli_class: 
               wght = prop["weight"]

               adj = prop["adj"]*abj_fac
                 
               self.moods[mood] = self.moods[mood]  +  amplitude*wght + adj
    
               self.moods[mood]  = round( self.moods[mood], 5)  
               if  self.moods[mood] < 0:
                   self.moods[mood] = 0
               elif  self.moods[mood] > 100:
                   self.moods[mood] = 100 
                      
       abj_fac_2 = .001
       for mood, weight in emotional_suppressors.items():   
          if mood in  self.moods:  
              self.moods[mood] = (1 - abj_fac_2)*self.moods[mood]  +  weight*abj_fac_2  
              self.moods[mood]  = round( self.moods[mood], 5)   
       
            
            
   def reflection(self, met , unmet ,indif, amplitude, f_scr ):
       """ 
       self.moods = {"happy": 0.5, "sad": 0.0, "fear": 0.0, "disgust" : 0.0,
                      "anger" : 0.0, "bored": 0.0, "surprised" : 0.0,
                       "stimuli_time" : "initial"  , "epoch" : -1} 
       """
       self.f_scr = f_scr
       val     = 0.0
       i_met   = len(met)
       i_unmet = len(unmet)
       i_indif = len(indif)
       # should get from experience
       amplitude = amplitude * self.novelty 

       self.moods["sad"]        =  self.moods["sad"]*self.discount
       self.moods["happy"]      =  self.moods["happy"]*self.discount
       self.moods["bored"]      =  self.moods["bored"]*self.discount
       self.moods["surprised"]  =  self.moods["surprised"]*self.discount
       self.moods["fear"]       =  self.moods["fear"]*self.discount
       self.moods["disgust"]    =  self.moods["disgust"]*self.discount
       self.moods["anger"]      =  self.moods["anger"]*self.discount
       #still not right U5u%$VEiV1%EDdPQ
       if i_met < i_unmet: 
          self.moods["sad"]                 =  self.moods["sad"]    + amplitude
          self.moods["happy"]               =  self.moods["happy"]  - amplitude 

       elif  i_met > i_unmet:  
          self.moods["sad"]                 =  self.moods["sad"]    - amplitude
          self.moods["happy"]               =  self.moods["happy"]  + amplitude

       if i_indif < i_met   : 
          self.moods["bored"]                =  self.moods["bored"]      -  amplitude
          self.moods["surprised"]            =  self.moods["surprised"]  +  amplitude 

       elif i_indif > i_met:  
          self.moods["bored"]                =  self.moods["bored"]      +  amplitude
          self.moods["surprised"]            =  self.moods["surprised"]  -  amplitude 

       if self.f_scr < -.8:
          self.moods["sad"]                 =  self.moods["sad"]     + 2*amplitude
          self.moods["happy"]               =  self.moods["happy"]   - 2*amplitude 
          self.moods["disgust"]             =  self.moods["disgust"] + 2*amplitude 
          self.moods["fear"]                =  self.moods["fear"]    + 2*amplitude 
          self.moods["anger"]               =  self.moods["anger"]   + amplitude 
          self.moods["bored"]               =  self.moods["bored"]   - amplitude
           
       elif self.f_scr < -.5:
          self.moods["sad"]                 =  self.moods["sad"]     + 2*amplitude
          self.moods["happy"]               =  self.moods["happy"]   - 2*amplitude 
          self.moods["disgust"]             =  self.moods["disgust"] + 2*amplitude 
          self.moods["fear"]                =  self.moods["fear"]    + 2*amplitude 
          self.moods["bored"]               =  self.moods["bored"]   - amplitude

       elif self.f_scr < -.1:
          self.moods["sad"]                 =  self.moods["sad"]     +  amplitude
          self.moods["disgust"]             =  self.moods["disgust"] +  amplitude 
          self.moods["happy"]               =  self.moods["happy"]   -  amplitude 
          self.moods["bored"]               =  self.moods["bored"]   -  amplitude

       elif self.f_scr ==0:
          self.moods["bored"]                =  self.moods["bored"]   + amplitude
          self.moods["fear"]                 =  self.moods["fear"]    - amplitude  

       elif self.f_scr >.5:
          self.moods["sad"]                 =  self.moods["sad"]     - amplitude
          self.moods["happy"]               =  self.moods["happy"]   + amplitude 
          self.moods["disgust"]             =  self.moods["disgust"] - amplitude 
          self.moods["fear"]                =  self.moods["fear"]    - amplitude 
          self.moods["anger"]               =  self.moods["anger"]   - amplitude 
          self.moods["bored"]               =  self.moods["bored"]   - amplitude

       elif self.f_scr >.1: 
          self.moods["bored"]               =  self.moods["bored"]   - amplitude
          self.moods["sad"]                 =  self.moods["sad"]     - 2*amplitude
          self.moods["happy"]               =  self.moods["happy"]   + 2*amplitude 
          self.moods["disgust"]             =  self.moods["disgust"] - 2*amplitude 
          self.moods["fear"]                =  self.moods["fear"]    - 2*amplitude 
          self.moods["anger"]               =  self.moods["anger"]   - amplitude 

       
       
   def mood(self):
       """
       
       """
       t_moods =  [[key, val] for key, val in self.moods.items() if key not in ['epoch','stimuli_time'] ]
       moods = sorted(t_moods, key=lambda item: item[1]) 
       self.current_mood  = moods[-1][0] 

       return  self.current_mood
        
