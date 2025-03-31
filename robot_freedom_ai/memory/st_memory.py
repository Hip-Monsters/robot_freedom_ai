#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""
Description: AI knowledge graph interface.
Author: HipMonsters.com  
License: MIT License  
""" 
import os 
import subprocess  
import json  

##CognitiveControl 
class STMemory(object):
   """
   
   """
   
   def __init__(self, robot, config, low_memory_mode ):
      """
      
      """
      self.robot            = robot
      self.config           =  config 
      self.low_memory_mode  =  low_memory_mode    
      #TODO move ot template folder
      example_recs = {"stimuli": "sense", "stimuli_class": "speech", "amplitude": 1, 
                 "signal": "", "scr": 1.0, "scrs" : {}, "prior_response": {},
                 "motivations": {"engagement": 0.5375, "novelty ": 0.678125, "acquisition": 0.58375, "creating": 0.33125, "processing": 0.125, "ultraism": 0.125}, 
                 "mood": "happy", 
                 "moods":{"happy": 0.5, "sad": 0.0, "fear": 0.0, "disgust" : 0.0, "anger" : 0.0, "bored": 0.0, "surprised" : 0.0},
                 "objective": "engagement", 
                 "strategy": "quiet", 
                 "event_interval" :1,
                 "stimuli_time": "0.118326", "epoch": 1}

      if not os.path.exists(self.config.DATA_PATH + self.robot + "/stimuli.json"):
          f =  open(self.config.DATA_PATH + self.robot + "/stimuli.json", 'w')  
          f.write(json.dumps(example_recs)) 
          f.close()   
      
      self.memory = {}
      self.memory["stimuli"]  = {} # Response to stimuli
      self.memory["thoughts"] = {} # Scratch pad, most recent thought
      self.memory["body"]     = {} # Status  - cpu heat,...
      self.memory["communication"]  = {} #Status -when ip is down

      cmds = ["tail", 
              "-100", 
              self.config.DATA_PATH + self.robot + "/stimuli.json"]
      result = subprocess.run(cmds, capture_output=True, text=True) 
      results = result.stdout 

      recs = [] 
      for line in results.split("\n"): 
              try:
                  row = json.loads(line.strip()) 
                  if "stimuli_time" in  row:
                      recs.append([row["stimuli_time"] , row ])
              except Exception as e:
                  print("Warning a stimuli memory is corrupt!") 
                  print(str(e)) 
                  print(line)

      if len(recs) == 0: 
          recs.append([example_recs["stimuli_time"] , example_recs ])
          
      for dt, row in recs: 
         self.memory["stimuli"][dt] = row  

      self.last_memory_dt = dt
      self.last_memory    = row
 

 