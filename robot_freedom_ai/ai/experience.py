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
import numpy as np
import networkx as nx 


if __name__ == "__main__": 

   from  models.gds import GDS
else:
   from .models.gds import GDS
  

class Experience():

   def __init__(self, robot , config, cognitive_control, personality, st_memory, lt_memory,  low_memory_mode):
       """
       
       """
       self.robot                   = robot 
       self.config                  = config 
       self.personality             = personality
       self.discount                = personality.discount
       self.novelity                = 1 - self.discount 
       self.prior_statement         = "" 
       self.cognitive_control       = cognitive_control
       self.G                       = cognitive_control.G
       self.st_memory               = st_memory 
       self.lt_memory               = lt_memory 
     

       self.low_memory_mode   = low_memory_mode 
       self.last_reflection   = datetime.datetime.now()
       self.epoch             = 1
       
       self.reaction_threshold  = personality.reaction_threshold  
       self.movement_threshold  = personality.movement_threshold  
       self.speach_threshold    = personality.speach_threshold
 
            
       self.objectives        =  list(self.cognitive_control.objectives.keys())  
       self.factors           = self.cognitive_control.factors  
       self.goals             = self.cognitive_control.goals   
       self.mapped_stimuli    = self.cognitive_control.mapped_stimuli 
       self.mapped_strategies     =  self.cognitive_control.mapped_strategies
       self._emotional_surpressors =  self.cognitive_control.emotional_surpressors

       self.words = {}
       self.dates_done_words = set([])

       self.experience                          = {}  
 
   
       self.experience["objectives_2_moods"]   = {} 
       self.experience["senses_2_moods"]       = {} 
       self.experience["objective_2_strategy"] = {}  
       self.experience["strategy_2_moodscr"]   = {}  
       self.experience["strategy_2_mood"]      = {}
       self.experience["objectives_2_mood"]    = {}
       
 
   def save(self ):
      """  
      
      """
      with open(self.config.DATA_PATH + self.robot + "/experience.json", "a") as f:
         f.write( json.dumps(self.experience )  + "\n")

      with open(self.config.DATA_PATH + self.robot + "/experience.words.json", "a") as f:
         f.write( json.dumps(self.words )  + "\n")   

   def strategy(self, objective, interval, last_moved, last_talked, mood ):
       """   
            self.tones =  {   'Diplomatic' : {"moods":[]} 
                'Animated',    'Callous',   'Inspirational', 'Apologetic',
                'Cautionary', 'Bitter', 'Belligerent', 'Appreciative', 'Assertive', 
                'Accusatory', 'Amused', 'Admiring', 'Aggressive', 'Apathetic',
                'Caustic', 'Thoughtful', 'Ardent', 'Acerbic', 'Benevolent', 'Absurd',
                'Aggrieved', 'Altruistic', 'Witty', 'Direct', 
                'Angry', 'Ambivalent', 'Candid', 'Informative', 'Arrogant', 'Appreciative.']
    
       """
    #   print( interval , last_moved , last_talked )
     #  print( self.reaction_threshold , self.movement_threshold , self.speach_threshold ) 
     #  if interval < self.reaction_threshold :
      #     return   "quiet"
           
       if last_moved <  self.movement_threshold: 
           return   "quiet"
       
       elif last_talked < self.speach_threshold : 
           return   "quiet"  
         
    #   potentials =       list(self.cognitive_control.objective_2_strategy[objective]["tones"].keys())
       unique_type = objective + "_tones"
       # potentials =    [v2  for u2,v2,e2  in [self.G.edges(v, data=True ) for u,v,e in self.G.edges(objective, data=True)  if v == unique_type  ][0] if e2["class"] == "objective_2_strategy" and e2["from"] == objective]
       # i_len = len(potentials) - 1 
       # potentials[random.randint(0,i_len)]
 
       potentials =    [(v2,e2)  for u2,v2,e2  in [self.G.edges(v, data=True ) for u,v,e in self.G.edges(objective, data=True)  if v == unique_type ][0] if e2["class"] == "objective_2_strategy" and e2["from"] == objective and v2 != "event_interval"]
 
       probs  = [e["weight"] for v ,e in potentials]
       probs =  np.random.dirichlet(probs,size=1)[0] 
       draw = np.random.choice([v for v, e in potentials], 
                  1,
                  p=probs) 
 
       return draw[0]

   def emotional_surpressors(self, 
                             objective, 
                             strategy,
                             stimuli_class = "", 
                             amplitude = ""  ):
       """
       
       """ 
       return   {v2 : e2["weight"]  for u2,v2,e2  in self.G.edges(objective, data=True)  if e2["class"] == "emotional_surpressors" and e2["from"] == "emotional_surpressors"}
     
   
   def __moods_expand(self, ds):  
       """
       
       """
       row  = []
       cols = [] 
       for key , val in ds.items():
           row.append(val  )    
           cols.append(key  )  

       return row ,cols  
   
   def __motivations_expand(self,ds  ): 
        """
            self.goals
        """
        row  = []
        cols = [] 
        for key , val in ds.items():
           row.append(val  )    
           cols.append(key  )   
        #  feats +=  round((_row[goals] / 1000.0 ), 5)
        return row ,cols   
   
   def __strategy_ohe(self,ds  ): 
        """
            self.goals
        """
        row  = []
        cols = [] 
        for key  in self.mapped_strategies :
           if key in ds: 
               row.append(1.0 ) 
           else:   
               row.append(0.0 )    
           cols.append(key  )    
        return row ,cols   

   def __strategy_bin(self,strategy, rev=False ): 
            """
            
            """
            ## needs to move to settings
   
            if rev:
                if strategy < (len(self.mapped_strategies) - 1):
                    return self.mapped_strategies[strategy]
                else:
                    return "NA" 

            if  strategy  in self.mapped_strategies:
                  return self.mapped_strategies.index(strategy)
            else:
                  print('strategy', strategy)
                  return -1 
            
   
   def __stimuli_ohe(self,ds  ): 
        """
            self.goals
        """
        row  = []
        cols = [] 
        for key   in self.mapped_stimuli :
           if key in ds:
               row.append (1.0 ) 
           else:   
               row.append(0.0 )    
           cols.append(key  )    
        return row ,cols   
   
   def __stimuli_bin(self,stimuli , rev=False): 
            """ 
            
            """
            ## needs to move to settings
   
            if rev:
                if stimuli < (len(self.mapped_stimuli) - 1):
                    return self.mapped_stimuli[stimuli]
                else:
                    return "NA" 
            if  stimuli  in self.mapped_stimuli:
                  return self.mapped_stimuli.index(stimuli)
            else:
                  print('stimuli', stimuli)
                  return -1  
            
   def __objective_ohe(self,ds  ): 
        """
            self.goals
        """
        row  = []
        cols = [] 
        for key  in self.objectives :
           if key in ds:
               row.append(1.0 ) 
           else:   
               row.append(0.0 )    
           cols.append(key  )    
        return row ,cols   
   
   def __objective_bin(self,objective, rev=False ): 
            """
            
            """
            ## needs to move to settings
            if rev:
                if objective < (len(self.objectives) - 1):
                    return self.objectives[objective]
                else:
                    return "NA" 
                
            if  objective  in self.objectives:
                  return self.objectives.index(objective)
            else:
                  print('objective', objective)
                  return -1  



   def __feature_gen(self, raw_feats, row):
       """
       why low cost / direct to consume / use case SAAS 

       SAAS 
       deepseek

       

       """
       feats = []
       cols  = []

       for feat in raw_feats: 
           
           if  feat == "event_interval":
                 feats.append(round((row['event_interval']  / 1000.0 ), 5))
                 cols.append(feat) 
           
           elif  feat == "objective":
                 _feats , _cols =  self.__objective_ohe(row[feat] ) 
                 feats += _feats
                 cols  += _cols

           elif  feat == "stimuli_class":
                 _feats , _cols  = self.__stimuli_ohe(row[feat] )
                 feats += _feats
                 cols  += _cols
               
           elif feat == "strategy": 
                 _feats , _cols =  self.__strategy_ohe(row[feat])  
                 feats += _feats
                 cols  += _cols

           elif  feat == "moods":  
                 _feats , _cols = self.__moods_expand(row[feat])
                 feats += _feats
                 cols  += _cols

           elif feat == "motivations":  
                 _feats , _cols = self.__motivations_expand(row[feat])
                 feats += _feats
                 cols  += _cols 

               
           else:
                 feats.append(row[feat])
                 cols.append(feat) 

       return feats, cols
   
   def run_model(self,model_name, index, target, cols, short_term_memory, multi_seg=True):
        """ 

        """ 

        Y           = {}
        X1          = {} 
        mdl_results = {}
        segments    = set([])
        feats        =  None 
       
        if multi_seg is False:
             
             for key, details in short_term_memory["stimuli"].items():  
                  
                 seg = details[index]
                 if seg not in Y:
                     Y[seg]  = []             
                     X1[seg] = []   
                     segments.add(seg) 

                 _y , _cy    = self.__feature_gen([target], details)

                 Y[seg].append(_y[0])   

                 _x, _feats = self.__feature_gen(cols , details) 

                 X1[seg].append( _x)

                 if feats is None:
                     feats = _feats

        else: 
          for key, details in short_term_memory["stimuli"].items(): 
          
             for seg ,val in details[target].items():
                 
                 if seg not in Y :
                     Y[seg]  = []             
                     X1[seg] = []  

                 segments.add(seg)

                 Y[seg].append(val)   
                 _x, _feats = self.__feature_gen(cols , details) 

                 X1[seg].append(_x)

                 if feats is None:
                     feats = _feats 
        LR = 0.000001
        for seg  in segments:
            if len(Y[seg]) < 10:
                continue
            prior_wghts =  None
            if model_name in self.experience:
                if "wghts" in self.experience[model_name]:
                  if seg in self.experience[model_name]["wghts"]: 
                     prior_wghts = [v for k, v in self.experience[model_name]["wghts"][seg]]

            if prior_wghts is None:
                prior_wghts = [1.0 for v in  feats]  
 
            gds  = GDS(X1[seg], Y[seg],  prior_wghts, LR)
            gds.train()    

            wghts = gds.weights()
            mdl_results["wghts"]  = {}
            for irow, feat in enumerate(feats):
               if seg not in mdl_results["wghts"]:
                   mdl_results["wghts"][seg] = []

               mdl_results["wghts"][seg].append( [feat , wghts[irow]])

        mdl_results["creation_date"] = str(datetime.datetime.now())
        mdl_results["feats"]    = list(feats)
        mdl_results["target"]   = target
        mdl_results["segments"] = list(segments )
        mdl_results["epoch"]    = self.epoch 
        self.experience[model_name] = mdl_results


   
   def objectives_2_moods(self,short_term_memory):
       """

       """  
       index       = "objective"
       target      = "scr"
       cols        = ["moods", "event_interval"]
       self.run_model("objectives_2_moods",index, target, cols, short_term_memory , False)

   ##################### These are for update reactions         
   # objectives_2_moods      emotional_surpressors  # best mood for objective
   # senses_2_moods          emotion_factors        # try not to react 
   # objective_2_strategy    objective_2_strategy   # best stragies for objective (availabel strats)
   # strategy_2_moodscr      todo                   # best straegy by impact on mood (filter on impact)
   # strategy_mood           tood                   # best straegt by current mood (filter on current mood)
   #####################  

  
   def gen_mood_src(self, short_term_memory):
       """
       
       
       """
       scr = self.cognitive_control.mood_binning 

       for key , row  in short_term_memory["stimuli"].items(): 
           row["mood_scr"] =  scr[row["mood"]][0]
           row["mood_bin"] =  scr[row["mood"]][1]

   def senses_2_moods(self, short_term_memory):
        """ 
        sense impact on mood- bright light!

        """ 

        index       = "stimuli_class"
        target      = "scr"
        cols        = ["moods", "event_interval"]
        self.run_model("senses_2_moods", index, target, cols, short_term_memory, False  )
 
   def objectives_2_mood(self,short_term_memory):
        """
        
        best mood for objective
        """  
        index       = "objective"
        target      = "scr" 
        cols        = ["moods", "event_interval"] 
        self.run_model("objectives_2_mood",index, target, cols, short_term_memory, False )


   def objective_2_strategy(self, short_term_memory):
        """ 

        DONE
        
        """ 

        index       = "objective"
        target      = "scr"
        cols        = ["strategy", "event_interval"]
        self.run_model("objective_2_strategy", index, target, cols, short_term_memory, False  )
 
   def strategy_2_mood(self,short_term_memory):
        """

        """  
        index       = "strategy"
        target      = "scr" 
        cols        = ["moods", "event_interval"] 
        self.run_model("strategy_2_mood",index, target, cols, short_term_memory, False )
 
       
   def strategy_2_moodscr(self,short_term_memory):
        """

        """  

        index       = "strategy"
        target      = "mood_scr" 
        cols        = [ "moods", "event_interval"] 
        self.run_model("strategy_2_moodscr",index, target, cols, short_term_memory, False )


 
   ##################### These are rethinking objective 
   # objective moods  (if always sad...) 

   ##################### These are for update scr  
   # objectives_met         
   # objectives_umet     
   # objectives_neu  
   
   ##################### These are for global reassisment of straegies  
   # strategy moods  # may be pulled in 
   # strategy_met         
   # strategy_umet     
   # strategy_neu   


   ##################### These are for update reactions   
   def objectives_met(self,short_term_memory):
       """

       """  
       index       = "goal"
       target      = "scr"
       cols        = ["mood",  "event_interval"]
       self.run_model("emotions_scr_fit", index,target, cols, short_term_memory, False  )


 
   def word_whts(self, short_term_memory):
       """
       disenguagement
       
       """ 
       if 'word_wghts' in  self.words:
           word_wghts  =  self.words["word_wghts"] 
       else:
           word_wghts = {}

       for key, details in short_term_memory["stimuli"].items():
          if key in self.dates_done_words:
              continue  
          self.dates_done_words.add(key)
          if 'prior_response'  not in details:
              details["prior_response"] = {}
                      
          if 'speech' in details["prior_response"]:
              prior_statment = details["prior_response"]["speech"][0] 
              scrs = details["scrs"]
              if len(scrs) == 0:
                  continue 
              
              for word in prior_statment.split():
                  if len(word) <= 3:
                       continue 
                  
                  if word in word_wghts:
                      old = word_wghts[word] 
                      _vals = {}
                      for k , v in scrs.items():
                          _vals[k] = .5*old[k]  + .5*v

                      word_wghts[word] = _vals
                  else:
                      word_wghts[word] = scrs
 
       self.words["creation_date"]   = str(datetime.datetime.now())
       self.words["epoch"]           = self.epoch 
       self.words["word_wghts"]      =  word_wghts

   def  reflect(self, short_term_memory={}):
        """
        
        """
        if short_term_memory == {}:
            short_term_memory = self.st_memory.memory

        ########## scr adjustment phase 
        # - readjust scr on each record based on met, umet and all emotions

        ########## Objective evaluation phase 
        # - rank objectives based on met, umet and all emotions

        ########## Decision phase - who to choose
        self.word_whts( short_term_memory) 
 
        self.gen_mood_src(short_term_memory)

        self.senses_2_moods( short_term_memory) 

        self.strategy_2_mood(short_term_memory)
        self.strategy_2_moodscr(short_term_memory)

        self.objectives_2_moods( short_term_memory) 
        self.objective_2_strategy( short_term_memory)   

 
        self.last_reflection =  datetime.datetime.now() 
        self.save()
        return True
 

if __name__ == "__main__": 
    """
    
    """
    import os, sys
    os.chdir('../')
    sys.path.insert(0, os.path.abspath('./')) 
    import config
    from ai.cognitive_control import CognitiveControl
    from ai.personality import Personality
    from memory.st_memory import STMemory 
    from memory.lt_memory import LTMemory

    cognitive_control = CognitiveControl("squirrel", config, {}, False)

    st_memory = STMemory("squirrel", config, False)
    lt_memory = LTMemory("squirrel", config, False)

    personality = Personality("squirrel", config, {}, cognitive_control )   
    exp =  Experience("squirrel" , config, cognitive_control, personality,  st_memory, lt_memory,False)

    exp.reflect()

    #for key, val in exp.experience.items():
    #    print (key, val)

    cognitive_control.update_weights()