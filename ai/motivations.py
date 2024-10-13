#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Description: AI motivation interface.
Author: HipMonsters.com  
License: MIT License  
"""
import os
import json
import datetime 

class Motivations(object):

   def __init__(self, name, short_term_memory , config =None):
      """
      
      """
      self.name = name   
      self.short_term_memory = short_term_memory

      with open("./data/" + self.name + "/priorities.json") as f:
           data = ''
           for row in f:
              data += row  
           data = json.loads(data)
      self.priorities    = data["priorities"]

      if "motiviations" not in self.short_term_memory: 
           self.short_term_memory["motiviations"] = {}

      if not os.path.exists("./data/" + self.name + "/motiviations.json"):
          f =  open("./data/" + self.name + "/motiviations.json", 'w')   
          f.close()

      data = []
      with open("./data/" + self.name + "/motiviations.json") as f:
          
           for line in f: 
              try:
                  row = json.loads(line)
                  data.append(row)
                  if "stimui_time" in row:
                      self.short_term_memory["motiviations"][row["stimui_time"]]  =  row 
              except:
                  print("Warning a memory of motives is corrupt!")

      if len(data) == 0:
         self.motiviations    =  {"enguagement":  .5, "novelity": .5 , "acquisition" :  .5,
         "creating" : .5,  "processing": .5 } 
      else:
         self.motiviations    = data[-1]

      self.current_object = ""

   def save(self, epoch  , stimui_time):
      """
      
      """
      str_stimui_time = str(stimui_time)
      self.motiviations["stimui_time"] = str_stimui_time
      self.motiviations["epoch"]       = epoch
 
      if "motiviations" not in self.short_term_memory:
          self.short_term_memory["motiviations" ] = {}

      self.short_term_memory["motiviations"][str_stimui_time] =  self.motiviations

      with open("./data/" + self.name + "/motiviations.json", "a") as f:
          f.write(json.dumps(self.motiviations)  + "\n")
 
   def check_status(self):
      """
      """

      unmet  = []
      met = []
      for key, val in self.motiviations.items():
         if val < 0:
            unmet.append(key)
         elif val > 0:
            met.append(key)

      return [met, unmet]
   
   def objective(self, met, unmet, indif , mood ):
       """
       Objective 
       {"enguagement": [-1 ,.5], "novelity": [-1, .05] , "acquisition" : [-1, .5],
         "creating" : [-1, .25],  "processing": [1, .25] } 
      
       """
       self.objectives = {"engage":     {"mood": ""    , "met" :["creating", "processing"], "unmet":["acquisition"]  }, 
                          "disengage":  {"mood": ""    , "met" :["acquisition"], "unmet":["creating", "processing"]  }, 
                          "defuse":     {"mood": "fear", "met" :["engage"], "unmet":["angry"]  }, 
                          "relax":      {"mood": ""    , "met" :["engage"], "unmet":["angry"]  }, 
                          "inspire":    {"mood": ""    , "met" :["engage"], "unmet":["novelity"]  }, 
                       
                        } 
       objective = "engage"
       p_iunmet = 0
       p_met    = 0
       for key, val in self.objectives.items(): 
           imet   = len([1 for v in met    if v in val["met"]])
           iunmet = len([1 for v in unmet  if v in val["unmet"]])
           imood  = len([1 for v in val["mood"] if v == mood])
           
           if iunmet > p_iunmet or imood > 0  :
               objective = key 
               p_iunmet = iunmet
               if imood > 0:
                   break
       self.current_object = objective       
       return objective

       
   
   def goal_achievement(self, stimuli, stimuli_class, adjusted, stimuli_datetime, epoch):
      """
      """

      self.stimuli_goal_factors = {}
      self.stimuli_goal_factors["sense"] = {}
      self.stimuli_goal_factors["sense"]["noise"]  = {"enguagement": [1 ,0]  , "novelity": [1, .75]  , "acquisition" : [1, .1],  "creating" : [1, 0],    "processing": [1, 0] } 
      self.stimuli_goal_factors["sense"]["speech"] = {"enguagement": [1 ,.5] , "novelity": [1, .25]  , "acquisition" : [1, .5],  "creating" : [1, .25],  "processing": [1, 0] } 
      self.stimuli_goal_factors["sense"]["quiet"]  = {"enguagement": [-1 ,.5], "novelity": [-1, .05] , "acquisition" : [-1, .5], "creating" : [-1, .25],  "processing": [1, .25] } 
      self.stimuli_goal_factors["sense"]["movement"]  = {"enguagement": [-1 ,.5], "novelity": [-1, .05] , "acquisition" : [-1, .5], "creating" : [-1, .25],  "processing": [1, .25] } 
      self.stimuli_goal_factors["sense"]["distance"]  = {"enguagement": [-1 ,.5], "novelity": [-1, .05] , "acquisition" : [-1, .5], "creating" : [-1, .25],  "processing": [1, .25] } 
      self.stimuli_goal_factors["sense"]["tempature"] = {"enguagement": [-1 ,.5], "novelity": [-1, .05] , "acquisition" : [-1, .5], "creating" : [-1, .25],  "processing": [1, .25] } 
      self.stimuli_goal_factors["sense"]["humidity"]  = {"enguagement": [-1 ,.5], "novelity": [-1, .05] , "acquisition" : [-1, .5], "creating" : [-1, .25],  "processing": [1, .25] } 
      self.stimuli_goal_factors["sense"]["touch"]     = {"enguagement": [-1 ,.5], "novelity": [-1, .05] , "acquisition" : [-1, .5], "creating" : [-1, .25],  "processing": [1, .25] } 
      self.stimuli_goal_factors["sense"]["balence"]   = {"enguagement": [-1 ,.5], "novelity": [-1, .05] , "acquisition" : [-1, .5], "creating" : [-1, .25],  "processing": [1, .25] } 
      self.stimuli_goal_factors["sense"]["light"]   = {"enguagement": [-1 ,.5], "novelity": [-1, .05] , "acquisition" : [-1, .5], "creating" : [-1, .25],  "processing": [1, .25] } 
     
      
      for goal, factor in self.stimuli_goal_factors[stimuli][stimuli_class].items():
          if factor[0] == 1:
                self.motiviations[goal] = self.motiviations[goal] +  adjusted*factor[1]
          else:
                self.motiviations[goal] = self.motiviations[goal] + adjusted*factor[1] 

          self.motiviations[goal] = round(self.motiviations[goal], 2)

          if  self.motiviations[goal] < -1000:
             self.motiviations[goal] = -1000
          if  self.motiviations[goal] > 1000:
             self.motiviations[goal] = 1000




      unmet   = []
      met     = []
      indif   = []
      for goal, val in self.motiviations.items():
         
         if goal not in ["epoch", "stimui_time", "dt"]:
             if val < 0:
                unmet.append(goal)
             elif val > 0:
                met.append(goal)
             elif val == 0:
                indif.append(goal)

      self.save(epoch , stimuli_datetime)

      return [met, unmet, indif]
