#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""
Description: AI experience interface.
Author: HipMonsters.com  
License: MIT License  
"""

import os
import datetime 
import json
import random 
from ai.learners.Gradient_Descent_Solver import Gradient_Descent_Solver  
 

class Experience():

   def __init__(self, name , short_term_memory):
       """
       
       """
       self.name              = name
       self.short_term_memory = short_term_memory  
       self.last_reflection   =  datetime.datetime.now()
       self.epoch            = 1
       

       if not os.path.exists("./data/" + self.name + "/experience.json"):
          f =  open("./data/" + self.name + "/experience.json", 'w')   
          f.close()

       data = []
       with open("./data/" + self.name + "/experience.json") as f:
          
           for line in f: 
              row = json.loads(line)
              data.append(row)

       self.short_term_memory["experience"]  = data 
       if len(data) == 0:
          self.experience = {"enguagement": {"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,"novelity":{"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,"acquisition":{"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,"creating": {"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,"processing":{"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0}}
       else:
          self.experience = data[-1] 
       
       self.factors = ["happy" , "sad" , "fear" , "disgust", "anger" ,  "bored" , "surprise" , "event_interval" , "stimuli_class", "amplitude"]
       self.goals  =  ["enguagement", "novelity" , "acquisition" , "creating" , "processing" ]
           

   def save(self ):
      """
      
      """
      self.experience["epoch"] = self.epoch 
      self.experience["reflection_time"] = str( self.last_reflection ) 
      self.short_term_memory["experience"].append(self.experience)


      with open("./data/" + self.name + "/experience.json", "a") as f:
          f.write(json.dumps(self.experience) + "\n")
       

   def emotional_surpressors(self, stimuli , stimuli_class, amplitude   ):
       """
       
       """
       # self.experience
       return self.experience 

   
   def strategy(self, objective, interval, mood ):
       """   
            self.tones =  {   'Diplomatic' : {"moods":[]} 
                'Animated', 
                'Callous',
                 'Inspirational', 'Apologetic',
                'Cautionary', 'Bitter', 'Belligerent', 'Appreciative', 'Assertive', 
                'Accusatory', 'Amused', 'Admiring', 'Aggressive', 'Apathetic',
                'Caustic', 'Thoughtful', 'Ardent', 'Acerbic', 'Benevolent', 'Absurd',
                'Aggrieved', 'Altruistic', 'Witty', 'Direct', 
                'Angry', 'Ambivalent', 'Candid', 'Informative', 'Arrogant', 'Appreciative.']
    
       """

       self.goal_2_strategy  =  { "engage" : {  "tones" : ['Diplomatic', 'Benevolent', 'Witty', 'Thoughtful'] }, 
                                  "defuse" : {   "tones" : ['Appreciative',  'Thoughtful']}, 
                                  "inspire": {   "tones" : ['Inspirational', 'Informative'] }, 
                                  "relax" : {   "tones" :  ['Ambivalent', 'Absurd']},
                                 } 
        
       potentials =        self.goal_2_strategy[objective]["tones"]
       i_len = len(potentials) - 1

       ##fitst based on mood
       ##for strat in potentials:
       ##
       ### then filter on experinece

       ##for strat in potentials:
       ### if did not work dont do
 
       if interval < 1: 
           return   "quiet"
       else:
           return    potentials[random.randint(0,i_len)]
            
   def reflection(self, data, vargs ={}  ):
        """
       
        """
        print("\rSelf-Reflection - initiating"   + self._space , end="" )  

        Y =  {} 
        for goal in self.goals:
            Y[goal] = []
        X1 = []
        Z  = []
        ## Builds imhibitors
        for row in data:

            for goal in self.goals: 
                Y[goal].append( round((row[goal] / 1000.0 ), 5)) 

            arow = []
            arow.append(round((row['happy']    / 100.0 ), 5))   
            arow.append(round((row['sad']      / 100.0 ), 5))
            arow.append(round((row['fear']     / 100.0 ), 5))
            arow.append(round((row['disgust']  / 100.0 ), 5))
            arow.append(round((row['anger']    / 100.0 ), 5))
            arow.append(round((row['bored']    / 100.0 ), 5))
            arow.append(round((row['surprised']/ 100.0 ), 5))
            arow.append(round((row['event_interval']  / 1000.0 ), 5))

            ## could split X's instead
            if (row['stimuli_class'] ==  'noise'):   
                 arow.append( 1 )  
            elif (row['stimuli_class'] ==  'speech'):   
                 arow.append( 2)
            elif (row['stimuli_class'] ==  'movement'):   
                 arow.append( 4)
            elif (row['stimuli_class'] ==  'distance'):   
                 arow.append( 5)
            else:
                 arow.append( 3)

            print("\rSelf-Reflection"  + self._space , end="" )   
            arow.append(row['amplitude'])
            X1.append(arow)
  
        print("\rSelf-Reflection  Training..."   + self._space , end="" )  
        LR = 0.000001
        for goal  in self.goals:

            prior_wghts = [v for v in  self.experience[goal].values()]
          #  imx =  len(X1[0])  
          #  prior_wghts = prior_wghts[0:imx] 
            
            print("\rSelf-Reflection Solving for " + goal   + self._space , end="" )  
            gds  = Gradient_Descent_Solver(X1, Y[goal], LR, weights = prior_wghts)
            gds.train()
            print("\rSelf-Reflection Solved for " + goal   + self._space , end="" )   

            #  gds.report_results()
            # gds.plot_solution_convergence()
            wghts = gds.weights()
            for irow, factor in enumerate(self.factors):
               self.experience[goal][factor] = wghts[irow]

        print("\rSelf-Reflection Complete   " + goal   + self._space , end="" )   
        self.last_reflection =  datetime.datetime.now()
        self.epoch  = self.epoch  +1
        self.save()

""" 
{
"enguagement": {"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,
"novelity":{"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,
"acquisition":{"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,
"creating": {"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,
"processing":{"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0}
}

{"enguagement": {"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,"novelity":{"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,"acquisition":{"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,"creating": {"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0} ,"processing":{"happy":0.0, "sad":0.0, "fear":0.0, "disgust":0.0, "anger":0.0, "bored":0.0, "surprise":0.0, "time_delta":0.0, "stimuli_class":0.0}}

"""
