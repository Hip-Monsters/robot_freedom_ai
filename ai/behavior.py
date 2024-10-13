#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Description: AI behavior interface.
Author: HipMonsters.com  
License: MIT License  
"""
 
import os
import datetime 
import json 
   
 
from ai.motivations          import Motivations
from ai.personality          import Personality
from ai.emotions             import Emotions
from ai.experience           import Experience
from dateutil import parser

class Behavior():

   def __init__(self, name , short_term_memory , knowledge):
       """
       S-O-R Theory with Personality Traits
       
       
       """
       self.name = name
       ## Core components
       self.knowledge              =  knowledge
       self.short_term_memory      =  short_term_memory

       self.emotions    = Emotions(self.name   , self.short_term_memory )
       self.motivations = Motivations(self.name, self.short_term_memory)
       self.personality = Personality(self.name)
       self.experience  = Experience(self.name, self.short_term_memory)
       ####
       self.last_stimui       = None
       self.stimui_time       = -1
       self.epoch            = None
       self.last_update      = None
       self.objective        = "engage"
       self.strategy         = "Thoughtful"

       if "stimuli" not in self.short_term_memory: 
           self.short_term_memory["stimuli"] = {}
              
       if not os.path.exists("./data/" + self.name + "/stimuli.json"):
          f =  open("./data/" + self.name + "/stimuli.json", 'w')   
          f.close()
 
       data = []
       with open("./data/" + self.name + "/stimuli.json") as f:
          
           for line in f: 
              try:
                  row = json.loads(line)
                  data.append(row) 
                  if "stimui_time" in  row:
                      self.short_term_memory["stimuli"][row["stimui_time"]]  =  row 
              except:
                  print("Warning a stimuli memory is corrupt!")
   def behavior(self, mood, modifier):
       """
       """
       return 1
   
   def determine_class(self, event, cat, met, umet, modifer):
       """
       """
       return event + " " + cat
   
   def save_memory(self,stimuli ,stimuli_class, amplitude, epoch, stimui_time ):
       """
       
       """
        
       str_stimui_time = str(stimui_time) 


       self.short_term_memory["stimuli"][str_stimui_time] = {"stimuli" :  stimuli ,
                                                             "stimuli_class" : stimuli_class, 
                                                             "amplitude" : amplitude ,
                                                              "stimui_time" : str_stimui_time ,
                                                              "epoch" : epoch }
       ## move to main as some point
       with open("./data/" + self.name + "/stimuli.json", "a") as f:
            f.write(json.dumps( {"stimuli" :stimuli ,
                                  "stimuli_class" :stimuli_class, 
                                   "amplitude":amplitude , 
                                   "epoch" : self.epoch,
                                   "stimui_time":  str_stimui_time } ) + "\n")
            
       self.last_update      = datetime.datetime.now() 

   def reflection(self):
        """
       
        """
        #Adjust behavior modifier based on stimuli and emotions
     
        results = []
        for stimuli_date  ,  modivations    in self.short_term_memory["motiviations"].items(): 
            v = {}
            for key,  val  in modivations.items():
                v[key] = val
            dt = parser.parse(stimuli_date)

            v["dt"] = dt       
            results.append(v)
       
        data = []
        i_start = 0
        for stimuli_date  , stimuli in  self.short_term_memory["stimuli"].items():
     
            if stimuli_date not in  self.short_term_memory["emotions"]:
               
                 continue 
            emotions   = self.short_term_memory["emotions"][stimuli_date] 
           # priorities = self.motiviations.priorities 

            dt = parser.parse(stimuli_date) 
            targets = None
            for row in results[i_start:]:
               diff = row['dt'] - dt 
               if diff.total_seconds() > 0:
                   row["event_interval"]  = diff.total_seconds()
                   targets = row
                   break
               i_start += 1
            if targets is None:
                 break
                 
            fin = {}
            for key, val in targets.items():
               fin[key]  = val 

            for key, val in emotions.items():
               fin[key]  = val 

            for key, val in stimuli.items():
               fin[key]  = val 

            data.append(fin)
            action     = "get repsonse" 
             
            ## get priorities 
            ## looks at goals to
        
        self.experience.reflection(data)
          
            
   def stimuli(self, stimuli, stimuli_class, amplitude, epoch, stimui_time , interval, other={}):
       """
       S-O-R Theory with Personality Traits
       Stimuli Observeration Response
       Stimuli -> personality + desires + experience -> emtions -> response
       
       """
       self.stimui_time = stimui_time
       ### Log true  
       self.save_memory(stimuli ,stimuli_class, amplitude ,  epoch, stimui_time)

       ## higher orrder classification of event TODO
      # event_class event_cat = self.determine_class(stimuli, stimuli_class)

       ### Can learn to adjust stimuli class and amplictude- leanr to like what you dont like
       emotional_surpressors    = self.experience.emotional_surpressors(stimuli, stimuli_class, amplitude)

       ## How personality affects how event seen
       adjusted_modifier       = self.personality.event_modifer(stimuli, stimuli_class, amplitude)

 
       ## Check status of motivations
       met, umet, indif   = self.motivations.goal_achievement(stimuli, stimuli_class, adjusted_modifier , 
                                                              stimui_time,  epoch) 
  
       # update emotions based on class and modifier
       self.emotions.stimuli(stimuli, stimuli_class, adjusted_modifier , emotional_surpressors )
       

       # update emotions based on class and modifier
       self.emotions.reflection(met, umet , indif,  adjusted_modifier  )

    
       self.objective          = self.motivations.objective(met, umet, indif , self.emotions.mood() )
   
       self.strategy           = self.experience.strategy(self.objective, interval , self.emotions.mood())
       # calculate new emotion
       self.emotions.save(stimui_time,  epoch)
         