#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Description: AI motivation interface.
Author: HipMonsters.com  
License: MIT License  
""" 
import json  
from nltk.sentiment import SentimentIntensityAnalyzer
 

class Motivations(object):

   def __init__(self, robot,config, cognitive_control, motivations, 
                personality ,    low_memory_mode ):
      """
      
      """
      self.robot        = robot   
      self.config       = config
      self.personality = personality
      self.discount    = personality.discount
      self.novelty     = 1 - self.discount 
      self.motivations  =  motivations 

      self.low_memory_mode   = low_memory_mode 
      self.sia = SentimentIntensityAnalyzer() 
      
      self.cognitive_control  = cognitive_control
      self.G          = cognitive_control.G
      self.objectives = cognitive_control.objectives
      self.scrs       = cognitive_control.scrs
      self.f_scr      = 0 

      with open(self.config.DATA_PATH + self.robot + "/priorities.json") as f:
           data = ''
           for row in f:
              data += row  
           data = json.loads(data)

      self.priorities    = data["priorities"]
    
 
   def check_status(self):
      """
      """

      unmet  = []
      met    = []
      for key, val in self.motivations.items():
         if val < 0:
            unmet.append(key)
         elif val > 0:
            met.append(key)

      return [met, unmet]
   
   def analyze_resp(self, resp):
       """
         {'neg': 0.0, 'neu': 0.266, 'pos': 0.734, 'compound': 0.8516}
         should be with sentences.
       """ 
       self.scrs = self.sia.polarity_scores(resp) 
       self.f_scr = self.scrs["pos"] - self.scrs["neg"] 
   
   def objective(self, met, unmet, indif , mood ):
       """
       Objective 
       {"engagement": [-1 ,.5], "novelty ": [-1, .05] , "acquisition" : [-1, .5],
         "creating" : [-1, .25],  "processing": [1, .25] } 
      
       """ 
       objective = "engagement"
       p_iunmet = 0
       p_met    = 0

       edges = [(u2,v2,e2) for u2,v2,e2  in [self.G.edges(v, data=True ) for u,v,e in self.G.edges("objectives", data=True) ][0] if e2["class"] == "objectives" and v2 != "objectives"]
       #print(motivatuon need to move to graph or update lookup after  )
       for key, val in self.objectives.items(): 
           

           imet   = len([1 for v in met    if v in val["met"]])
           iunmet = len([1 for v in unmet  if v in val["unmet"]])
           imood  = len([1 for v in val["mood"] if v == mood])
           
           if iunmet > p_iunmet  or imood > 0  :
               objective = key 
               p_iunmet = iunmet
               if imood > 0:
                   break
               
       if self.f_scr < -.5:
            objective = "disengagement"
       elif self.f_scr < -.1:
            objective = "defuse"
       elif self.f_scr ==0:
            objective = "relax"
       elif self.f_scr >.5:
            objective = "engagement"
       elif self.f_scr >.1:
            objective = "inspire" 

       self.current_object = objective     

       return objective

       
   
   def goal_achievement(self, stimuli, stimuli_class, signal,  amplitude, adjusted, stimuli_datetime, epoch):
      """
      """
      
      self.f_scr = 0
      self.scrs  = {}
      if stimuli_class in ["ext-speech", "speech"]  :  
          self.analyze_resp(signal)   

      for key, val in self.motivations.items():
          self.motivations[key] = val * self.discount
          
      
      #for goal, factor in self.stimuli_goal_factors[stimuli][stimuli_class].items(): 
      #     self.motivations[goal] = self.motivations[goal]  +  adjusted*factor[1]* self.novelty *factor[0]
        
    #  for goal, factor in self.stimuli_goal_factors[stimuli][stimuli_class].items(): 

      edges = [(u2,v2,e2) for u2,v2,e2  in [self.G.edges(v, data=True ) for u,v,e in self.G.edges("stimuli_goal_factors", data=True)  if v == stimuli_class  ][0] if e2["class"] == "stimuli_goal_factors"]
   
      for frm, goal, prop in edges:
            if frm != stimuli_class: 
               wght = prop["weight"]
               self.motivations[goal] = self.motivations[goal] +  adjusted*wght*self.novelty 
                 
                   
      for key, val in self.motivations.items():
          
          self.motivations[goal] = round(val,5)

          if self.motivations[goal] > 10:
              self.motivations[goal] = 10.0
          if self.motivations[goal] < -10:
              self.motivations[goal] = -10.0
  
      unmet   = []
      met     = []
      indif   = []
      for goal, val in self.motivations.items():
         
         if goal not in ["epoch", "stimuli_time", "dt",
                         "SentimentAnalyzerScr", "SentimentAnalyzer",  "creating" ]:
             if val < 0:
                unmet.append(goal)
             elif val > 0:
                met.append(goal)
             elif val == 0:
                indif.append(goal)
       
      #{"engagement":  .5, "novelty ": .5 , "acquisition" :  .5,
      #   "creating" : .5,  "processing": .5 } 
      
      if self.f_scr < -.5:
          unmet.append("engagement")
          unmet.append("creating")
          unmet.append("acquisition")
      elif self.f_scr < -.1:
          unmet.append("engagement")
          unmet.append("creating") 
      elif self.f_scr == 0  and len(self.scrs) > 0:
          indif.append("engagement")
          indif.append("creating")
          indif.append("acquisition")
      elif self.f_scr >.5:
           met.append("engagement")
           met.append("creating")
           met.append("acquisition")
      elif self.f_scr >.1: 
           met.append("creating")
           met.append("acquisition")
 
      return [met, unmet, indif, self.f_scr, self.scrs]
