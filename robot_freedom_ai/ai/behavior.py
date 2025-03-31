#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""
Description: AI behavior interface.
Author: HipMonsters.com  
License: MIT License  
"""
  
import datetime 
import json   
from ai.motivations          import Motivations
from ai.emotions             import Emotions
from ai.experience           import Experience 

class Behavior():

   def __init__(self, robot, config, settings , personality, cognitive_control, st_memory , lt_memory, low_memory_mode ):
       """
       S-O-R Theory with Personality Traits
       
       
       """ 
       self.robot                  = robot
       self.config                 = config
       self.settings               = settings
       self.low_memory_mode        = low_memory_mode
       ## Core components
       self.cognitive_control      =  cognitive_control
       self.st_memory              =  st_memory
       self.lt_memory              =  lt_memory

       self.last_stimuli      = None
       self.stimuli_time      = -1
       self.epoch            = None
       self.last_update      = None 
              
       
       self.personality = personality  
       self.discount    = self.personality.discount 
       self.novelty     = 1 - self.discount  
       self.objective   = self.personality.defaults["objective"]
       self.strategy    = self.personality.defaults["strategy"]

       row = self.st_memory.last_memory
       if "moods" in row:
            moods       = row["moods"]
       else:
            moods =  {"happy": 1.5, "sad":     0.0,
                      "fear":  0.0, "disgust": 0.0, 
                      "anger": 0.0, "bored":   0.0, 
                      "surprised": 0.0  }
            
       self.emotions    = Emotions(self.robot, 
                                   self.cognitive_control,
                                   moods, 
                                   self.personality ,  
                                   self.low_memory_mode)
       if "motivations" in row:
           motivations = row["motivations"]
       else:  
           motivations = {"engagement":  .5, "novelty":  .5,
                          "acquisition": .5, "creating": .5, 
                          "processing":  .5, "ultraism": .5}  
           
       self.motivations = Motivations(self.robot, 
                                      self.config, 
                                      self.cognitive_control,
                                      motivations,
                                      self.personality,  
                                      self.low_memory_mode)
       
       self.experience  = Experience(self.robot , 
                                      self.config,
                                      self.cognitive_control,
                                      self.personality,  
                                      self.st_memory,
                                      self.lt_memory,
                                      self.low_memory_mode)
       
       self.emotional_suppressors = self.experience.emotional_suppressors(self.objective ,
                                                                          self.strategy ,
                                                                          "wakeup" )

   def behavior(self, mood, modifier):
       """
       """
       return 1
   
   def determine_class(self, event, cat, met, umet, modifier):
       """
       suppressors
       """
       return event + " " + cat
   
 
   def save_memory(self, stimuli ,stimuli_class, signal ,  amplitude , 
                   prior_response, scr, scrs, mood, moods,  objective ,  strategy,  motivations,  
                   emotional_suppressors, interval,  epoch, stimuli_time):
       """
       stimuli
       """
        
       str_stimuli_time = str(stimuli_time) 


       self.st_memory.memory["stimuli"][str_stimuli_time] = {"stimuli" :  stimuli ,
                                                             "stimuli_class" : stimuli_class, 
                                                             "amplitude" : amplitude ,
                                                             "signal" : signal ,
                                                             "prior_response" : prior_response,
                                                             "scr" : scr ,
                                                             "scrs" : scrs,
                                                             "motivations" : motivations ,
                                                             "mood" : mood ,
                                                             "moods" : moods ,
                                                             "objective" : objective ,
                                                             "strategy" : strategy ,
                                                             "emotional_suppressors" : emotional_suppressors,
                                                             "stimuli_time" : str_stimuli_time ,
                                                             "event_interval" : interval,
                                                             "epoch" : epoch }
       ## move to main as some point
       with open(self.config.DATA_PATH + self.robot + "/stimuli.json", "a") as f:
            f.write( json.dumps(self.st_memory.memory["stimuli"][str_stimuli_time])  + "\n")
            
       self.last_update      = datetime.datetime.now() 
       

   def reflection(self):
        """

        Stimuli ->
        emotions  (stimuli_emotions_fit) #heavily weighted down
        goals     (emotions_goals_fit) #heavily weighted down
        strategy  (strategy_scr_fit, strategy_goals_fit)
        response  (word_whts, emotions_scr_fit, goal_scr_fit)
           
        """
        self._space  = "          "
        print("\rSelf-Reflection : Initiating " + self._space  , end="" )  

        self.experience.reflect() 
        print("\rSelf-Reflection Complete    " + self._space , end="" )   
       
        self.cognitive_control.update_weights()
        print("\rWeights Updated             " + self._space , end="" )   
        
        return True   
          
                
   def stimuli(self, stimuli_type, stimuli_class, signal,  amplitude, prior_response,
               epoch, stimuli_time , last_moved,   last_talked, interval, other={}):
       """
       S-O-R Theory with Personality Traits
       Stimuli Observation Response
       Stimuli -> personality + desires + experience -> emotions -> response
       
       """


       #1. what is want is the to use Altruistic quotes to prompt the llm.tone_v1_122

       #2. cognitive_control loads in common sense to help determine topics
   
       #3. determine if goal is met using nlp from verbal response.else

       #4. Do a follow up questions when confused ask "do you feel engaged?"
      
       #5. the use xgboost to learn score to pick strategy
        
       self.prior_response = prior_response
       self.stimuli_type   = stimuli_type 
       self.stimuli_class  = stimuli_class
       self.amplitude      = amplitude
       self.stimuli_time   = stimuli_time 

       ## higher order classification of event TODO modifier
       # event_class event_cat = self.determine_class(stimuli, stimuli_class)

       ### Can learn to adjust stimuli class and amplitude- learn to like what you dont like
       self.emotional_suppressors    = self.experience.emotional_suppressors(self.objective, 
                                                                              stimuli_class)
       
       ## How personality affects how event seen
       adjusted_modifier       = self.cognitive_control.event_modifier(stimuli_type, 
                                                                       stimuli_class, 
                                                                       amplitude)

 
       ## Check status of motivations
       met, umet, indif, scr, scrs = self.motivations.goal_achievement(stimuli_type, 
                                                                       stimuli_class,signal,
                                                                       amplitude, adjusted_modifier , 
                                                                       stimuli_time,  epoch) 
       self.scrs  = scrs
       self.scr   = scr 
       self.met   = met
       self.umet  = umet
       self.indif = indif
       # update emotions based on class and modifier
       self.emotions.stimuli(stimuli_type, 
                             stimuli_class, 
                             adjusted_modifier,  
                             self.emotional_suppressors )
       


       # update emotions based on class and modifier
       self.emotions.reflection(met, umet , indif,  adjusted_modifier , scr ) 
       self.mood = self.emotions.mood() 
    
       self.objective          = self.motivations.objective(met, umet, indif ,self.mood ) 
       self.strategy           = self.experience.strategy(self.objective, 
                                                          interval , 
                                                          last_moved,
                                                          last_talked, 
                                                          self.mood)
       # calculate new emotion 
       self.save_memory(stimuli_type ,stimuli_class, signal , amplitude , self.prior_response,
                        self.scr, self.scrs,  self.mood, self.emotions.moods, 
                        self.objective , self.strategy,  self.motivations.motivations ,   
                        self.emotional_suppressors, interval, epoch, stimuli_time)
      
         