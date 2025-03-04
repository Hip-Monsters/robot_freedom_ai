"""

"""
import os  
import json
  
#https://medium.com/@vasanthsai/exploratory-data-analysis-of-big-five-personality-test-c7b3e0d7d102
traits_lookup =   {"AGR": "kindness",
                   "EST": "emotional_stability",
                   "OPN": "openness",
                   "EXT": "socialability",
                   "CSN": "thoughtfulness" 
             }

def gen_interactions(sname, outfolder):
     """
     
     """
     with open( "./templates/interactions.json" ) as f:
         s_json = ""
         for row in f:
             s_json += row
         template = json.loads(s_json)

     final = template
     final["name"] = sname

     for question in final["vocalization"].keys(): 
           print("Provide 2-5 sentences for the following prompt separated by ';' :"  + question) 
           val = input() 
           final["vocalization"][question] =  val.split(";")

     #from emotions
     emotion_factors = {}
     emotion_factors["sense"] = {}
     emotion_factors["sense"]["noise"]     = {"sad":    0, "surprised":   1 , "bored":  -.1   , "fear":  .5 ,   "happy":   0  , "disgust":  0     } 
     emotion_factors["sense"]["speech"]    = {"sad":  -.5, "surprised":   0 , "bored":  -.1  , "fear": -.05 , "happy":    .1  , "disgust":  -.05   }
     emotion_factors["sense"]["quiet"]     = {"sad":   .5, "surprised":  -1 , "bored":    1   , "fear":   0 ,  "happy":  -.1  , "disgust":   .05   }
     emotion_factors["sense"]["movement"]  = {"sad":    0, "surprised":  .5 , "bored":  -.1  , "fear":  .05 , "happy":    0   , "disgust":  -.05   }
     emotion_factors["sense"]["distance"]  = {"sad":   .5, "surprised":  -.5, "bored":  -.1  , "fear": -.05 , "happy":   .1   , "disgust":  -.05   }
     emotion_factors["sense"]["tempature"] = {"sad":  -.5, "bored":      .5 }
     emotion_factors["sense"]["humidity"]  = {"sad":  -.5, "bored":      .5 }
     emotion_factors["sense"]["touch"]     = {"sad":  -.5, "bored":      .5 }
     emotion_factors["sense"]["balence"]   = {"sad":  -.5, "surprised":  .5 , "bored":  .05 }
     emotion_factors["sense"]["light"]     = {"sad":  -.5, "bored":      .5 }

      
     print("have a tool to do global adjument of emotion_factors")
     for question in ["sad", "surprised", "bored", "happy", "fear", "disgust"]: 
           print("Does the robot quickly feel "  + question + " (yes, no, average) or (y,n,a) ?") 

           while True:
               
               val = input().lower() 

               if val.startswith("y"): 
                   factor2 = .25
               elif val.startswith("n"): 
                   factor2 = -.25
               elif val.startswith("a"): 
                   factor2 = 0
               else:
                   factor2 = -1
                   print("Not a valid input") 

               if factor2 != -1:
                   break 
               
           for sense in emotion_factors["sense"].items():
               if question in sense:
                   vals = emotion_factors["sense"][question][sense] 
                   vals = [vals[0]     , val[1] + factor2]
                   emotion_factors["sense"][question][sense]  = vals
     

     final["emotions"] = {}
     final["emotions"]["emotion_factors"] = emotion_factors 
     #from experience
     objective_2_strategy  =  { "enguagement" :   {"tones" : ['Absurd', 'Witty', 'Amused'] }, 
                           "defuse" :   {"tones" : ['Appreciative', 'Admiring']}, 
                           "inspire":   {"tones" : ['Inspirational', 'Informative', 'Thoughtful'] }, 
                           "disenguagement": {"tones" : ['Diplomatic']},
                           "relax"  :   {"tones" : ['Altruistic', 'Benevolent']},
                          } 
    
     final["experience"] = {}
     final["experience"]["goal"] = objective_2_strategy 
     #from motivations
    # should be pulled from kwoledge base
     objectives = {"enguagement":     {"mood": ["happy", "sad"]    , "met" :["creating", "processing"], "unmet":["acquisition"]  }, 
                          "disenguagement":  {"mood": ["disgust"]    , "met" :["acquisition"], "unmet":["creating", "processing"]  }, 
                          "defuse":     {"mood": ["fear","anger"], "met" :["enguagement"], "unmet":["angry"]  }, 
                          "relax":      {"mood": ["surprise"]    , "met" :["enguagement"], "unmet":["angry"]  }, 
                          "inspire":    {"mood": ["bored"]    , "met" :["enguagement"], "unmet":["novelity"]  }, 
                          } 
     
 
     final["motivations"] = {}
     final["motivations"]["objectives"] = objectives 

     with open(outfolder + "interactions.json", "w") as f:
         f.write(json.dumps(final, indent=4))

     print("Generated file:" + outfolder + "interactions.json")

def gen_settings(sname, outfolder):
     """
     
     """
     with open( "./templates/settings.json" ) as f:
         s_json = ""
         for row in f:
             s_json += row
         template = json.loads(s_json)

     final = template
     final["full_name"]  = sname
     final["name"]  = sname
     final["admin"] = 0
     final["hub"]   = 0
 
     print("Robots full name e.gNumber Three?") 
     val = input()   
     final["full_name"] = val


     print("Robot color identity (#b0c4de)?") 
     val = input()   
     final["identification_color"] = val

     print("Robot form?") 
     val = input() 
     final["robot_form"] = val

     print("Robot voice? (e.g. en_US-norman-medium)") 
     val = input() 
     if val =="":
         val = "en_US-norman-medium"
     final["voice"]["LINUX"]["voice"] = val


     print("Prompt to LLM (e.g. You are a confused grandmother who responds with few words.)") 
     val = input() 
     if val =="":
         val = "You are a confused grandmother who responds with few words."
     final["chat"]["ai_description"] = val
     

     with open(outfolder + "settings.json", "w") as f:
         f.write(json.dumps(final, indent=4))

     print("Generated file:" + outfolder + "settings.json")

def gen_priorities(sname, outfolder):
     """
     
     """
     final = { "name": sname, 
              "priorities" : {"enguagement": 1,
              "novelity": 0.5,
              "acquisition": 0.5,
              "creating": 0.5,
              "processing" : 0.5
              }  
             }
     
     for question in final["priorities"].keys(): 
           print("From a scale of 1 to 10 rank:"  + question) 

           while True:
               val = input()  
               try:
                   val = float(val)/10.0
               except:
                   val == -1

               if val == -1:
                  print("Not a valid input")

               elif val < 0 or val > 10:
                  print("Please respond between 1 and 10") 
               else:
                   break 
               
           final["priorities"][question] = float(val)
     
     with open(outfolder + "priorities.json", "w") as f:
         f.write(json.dumps(final, indent=4))

     print("Generated file:" + outfolder + "priorities.json")

def generate_personality(sname, outfolder):
   """
   
   """
   results = {}
   for line in open('personality_questions.tbl'): 
       if line.strip() == '':
          continue
       
       aline = line.strip().split('\t')
       text = aline[1]
       cat = aline[0]
   

       print( text + " ") 
       #print("How much does your character agree?")
       print("Not at all , Not Much  , Neutral , Slightly  ,Very " )
       print("   1       ,    2      ,   3        , 4      ,5 " )
       

       while True:
           val = input()  
           try:
               val = int(val)
           except:
               val = -1

           if val == -1:
              print("Not a valid input")

           elif val < 1 or val > 5:
              print("Please respond between 1 and 5") 
           else:
               break
       if cat not in results:
          results[cat] = 0

       results[cat] =  results[cat] + int(val)

   print(results)
   final = {}
   final["name"] = sname
   final["traits"] = {}
   for cat , val in results.items():
      f_cat = cat[:3]
      f_cat = traits_lookup[f_cat]
      itype = 1
      if int(cat[3:]) % 2 == 0:
         itype = -1
      if f_cat not in final["traits"] :
         final["traits"] [f_cat] = 0.0

      final["traits"][f_cat] = final["traits"] [f_cat] + val*itype 

   for cat, val in traits_lookup.items():
       final["traits"][val] =  final["traits"][val] / 10.0

   final["discount"]       = 0.5  
   final["forgetfullness"] = 0.1 

   for trait in ["discount", "forgetfullness"]:
       print("What is the robot's " + trait + " level (1 to 10)?")
       while True:
           val = input()  
           try:
               val = int(val)
           except:
               val = -1

           if val == -1:
              print("Not a valid input")

           elif val < 1 or val > 10:
              print("Please respond between 1 and 10") 
           else:
               break
       final[trait] = val /10.0
           

   final["defaults"] = {"mood":"happy", 
                "objective":"enguagement", 
                "strategy":"Thoughtful"  
               }
       
   print(final)
   with open(outfolder + "personality.json", "w") as f:
      f.write(json.dumps(final, indent=4))
 

if __name__ == "__main__":
    """
    
    """
    print("Welcome the to RobotFreedom.com character generator.")

    while 1:
        
        print("What is the characters name?")
        sname = input()
 
        outfolder = "./settings/"+ sname + "/"
        try:
             os.makedirs(outfolder)
        except FileExistsError: 
             pass 
  

        if os.path.isfile(outfolder + "personality.json") is False:
            generate_personality(sname, outfolder)
        else:
             print("personality.json already exists.")

        if os.path.isfile(outfolder + "priorities.json") is False:
              gen_priorities(sname, outfolder)
        else:
             print("priorities.json already exists.")

        if os.path.isfile(outfolder + "interactions.json")  is False:
             gen_interactions(sname, outfolder)
        else:
             print("interactions.json already exists.")


        if os.path.isfile(outfolder + "settings.json") is False:
             gen_settings(sname, outfolder)
        else:
             print("settings.json already exists.")

        print("Do you want to create a new character? Yes/No")
        sname = input()
        if sname.lower().startswith("n"):
            print("Bye!")
            break