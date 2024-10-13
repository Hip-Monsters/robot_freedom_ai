#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Description: AI personality interface.
Author: HipMonsters.com  
License: MIT License  
"""
 
import os

import json
import datetime

class Personality(object):

   def __init__(self, name, config =None):
      """
      
      """
      self.name = name  

      with open("./data/" + self.name + "/personality.json") as f:
           data = ''
           for row in f:
              data += row  
           data = json.loads(data)

      self.traits = data["traits"]

      self.stimuli_factors = {}
      self.stimuli_factors["sense"] = {}
      self.stimuli_factors["sense"]["noise"] = {"emotional_stability": [-1 ,.5], "thoughtfulness": [1, .5] } 
      self.stimuli_factors["sense"]["speech"] = {"emotional_stability": [-1 ,.25], "thoughtfulness": [1, .5] }
      self.stimuli_factors["sense"]["quiet"] = {"emotional_stability": [-1 ,.25], "thoughtfulness": [1, .5] }
      self.stimuli_factors["sense"]["movement"] = {"emotional_stability": [-1 ,.25], "thoughtfulness": [1, .5] }
      self.stimuli_factors["sense"]["distance"] = {"emotional_stability": [-1 ,.25], "thoughtfulness": [1, .5] }
      self.stimuli_factors["sense"]["tempature"] = {"emotional_stability": [-1 ,.25], "thoughtfulness": [1, .5] }
      self.stimuli_factors["sense"]["humidity"] = {"emotional_stability": [-1 ,.25], "thoughtfulness": [1, .5] }     
      self.stimuli_factors["sense"]["balence"] = {"emotional_stability": [-1 ,.25], "thoughtfulness": [1, .5] }
      self.stimuli_factors["sense"]["light"] = {"emotional_stability": [-1 ,.25], "thoughtfulness": [1, .5] }
      self.stimuli_factors["sense"]["touch"] = {"emotional_stability": [-1 ,.25], "thoughtfulness": [1, .5] }
      
   
      
   def event_modifer(self, stimuli, stimuli_class,  magnitude=0):

      """
      """ 
      adjusted     = magnitude
    # print(self.stimuli_factors[stimuli][stimuli_class])
      for trait, factor in self.stimuli_factors[stimuli][stimuli_class].items():
          if factor[0] == 1:
                adjusted += self.traits[trait]*factor[1]
          else:
                adjusted +=  (1 - self.traits[trait])*factor[1] 
 

      return adjusted
   
      
   def modifers(self, stimuli, stimuli_class,  met, unmet): 
      """


      """
      val     = 0.0
      i_met   = len(met)
      i_unmet = len(unmet)

      for trait, factor in self.stimuli_factors[stimuli][stimuli_class]:
          if factor[0] == 1:
                val += self.traits[trait]*factor[1]
          else:
                val +=  (1 - self.traits[trait])*factor[1] 

      if i_met < i_unmet:
         val = val *.5

      neg      = val
      pos      = val
      neutral  = val

      return neg, pos, neutral



