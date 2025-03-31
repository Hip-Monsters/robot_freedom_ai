# -*- coding: utf-8 -*-
  
"""
Description: this dictionary defines sequence of movements for a robot for a provided term.
Author: HipMonsters.com 
License: MIT License
""" 
import random  


MAPS = {} 
""" 
  if (msg == "q")   Serial.print("Lift Left Arm");  
  else if (msg == "a")   Serial.print("Lower Left Arm"); 
  else if (msg == "w")  Serial.print("Flex Left Biceps"); 
  else if (msg == "s")  Serial.print("Relax Left Biceps"); 
  else if (msg == "e")   Serial.print("Open Left Hand"); 
  else if (msg == "d")   Serial.print("Close Left Hand"); 
  else if (msg == "t")   Serial.print("Lift Right Arm"); 
  else if (msg == "g")   Serial.print("Lower Right Arm"); 
  else if (msg == "y")   Serial.print("Flex Right Biceps"); 
  else if (msg == "h")   Serial.print("Relax Right Biceps"); 
  else if (msg == "u")   Serial.print("Open Right Hand"); 
  else if (msg == "j")   Serial.print("Close Right Hand"); 
  else if (msg == "i")   Serial.print("Open Right Hand"); 
  else if (msg == "k")   Serial.print("Close Right Hand"); 
  else if (msg == "o")   Serial.print("Move head left"); 
  else if (msg == "l")   Serial.print("Move Head Right");  
  else if (msg == "c")   Serial.print("Forward"); 
  else if (msg == "v")   Serial.print("Reverse"); 
  else if (msg == "b")   Serial.print("Left"); 
   (msg == "n") {        Serial.print("Right");  
   if state 'x' shut everything down  
    if( msg == "0")  { currentPalette = RainbowColors_p;         currentBlending = LINEARBLEND; }
    if( msg == "1")  { currentPalette = RainbowStripeColors_p;   currentBlending = NOBLEND;  }
    if( msg == "2")  { currentPalette = RainbowStripeColors_p;   currentBlending = LINEARBLEND; }
    if( msg == "3")  { SetupPurpleAndGreenPalette();             currentBlending = LINEARBLEND; }
    if( msg == "4")  { SetupTotallyRandomPalette();              currentBlending = LINEARBLEND; }
    if( msg == "5")  { SetupBlackAndWhiteStripedPalette();       currentBlending = NOBLEND; }
    if( msg == "6")  { currentPalette = CloudColors_p;           currentBlending = LINEARBLEND; }
    if( msg == "7")  { currentPalette = PartyColors_p;           currentBlending = LINEARBLEND; }
    if( msg == "8")  { currentPalette = myRedWhiteBluePalette_p; currentBlending = NOBLEND;  } 
    if( msg == "9")  { currentPalette = myRedWhiteBluePalette_p; currentBlending = LINEARBLEND; }
"""
 
SEQ = {}
#SEQ["body"] 
SEQ["head"] = {}
SEQ["head"]["turn"] = {} 
SEQ["head"]["turn"]["left"]  =  ['o'] 
SEQ["head"]["turn"]["right"] =  ['l']
#SEQ["head"]["turn"]["shake"] =  ['l', 'p2', 'o']

SEQ["hand"] = {} 
SEQ["hand"]["open"] = {} 
SEQ["hand"]["open"]["left"]  =  ['e'] 
SEQ["hand"]["open"]["right"] =  ['u']
SEQ["hand"]["open"]["both"]  =  ['u', 'e']
 
SEQ["hand"]["open"] = {}  
SEQ["hand"]["open"]["left"]   = ['d']  
SEQ["hand"]["open"]["right"]  = ['j'] 
SEQ["hand"]["open"]["both"]   = ['j','d'] 
                
"""
SEQ["hand"]["open_close"] = {}  
SEQ["hand"]["open_close"]["left"]   = ['e', 'p4', 'd']  
SEQ["hand"]["open_close"]["right"]  = ['i', 'p4', 'k'] 
SEQ["hand"]["open_close"]["both"]   = ['i', 'e', 'p4','d', 'k'] 
"""

SEQ["arm"]  = {}
SEQ["arm"]["raise"] = {}  
SEQ["arm"]["raise"]["left"]   = ['q', 'w']  
SEQ["arm"]["raise"]["right"]  = ['t', 'y'] 
SEQ["arm"]["raise"]["both"]   = ['q','t','w','y'] 
     
SEQ["arm"]["lower"] = {}  
SEQ["arm"]["lower"]["left"]   = ['a', 's']  
SEQ["arm"]["lower"]["right"]  = ['g', 'h'] 
SEQ["arm"]["lower"]["both"]   = ['a','f','g','h']  

SEQ["arm"]["bend"] = {}  
SEQ["arm"]["bend"]["left"]   = ['w']  
SEQ["arm"]["bend"]["right"]  = ['y'] 
SEQ["arm"]["bend"]["both"]   = ['w','y'] 
     
SEQ["arm"]["straighten"] = {}  
SEQ["arm"]["straighten"]["left"]    = ['s']  
SEQ["arm"]["straighten"]["right"]   = ['h'] 
SEQ["arm"]["straighten"]["both"]    = ['s', 'h']  


SEQ["arm"]["up"] = {}  
SEQ["arm"]["up"]["left"]   = ['q']  
SEQ["arm"]["up"]["right"]  = ['t'] 
SEQ["arm"]["up"]["both"]   = ['q','t' ] 
     
SEQ["arm"]["down"] = {}  
SEQ["arm"]["down"]["left"]   = ['a']  
SEQ["arm"]["down"]["right"]  = ['g'] 
SEQ["arm"]["down"]["both"]   = ['a','g']
""" 
SEQ["arm"]["flex"] = {}  
SEQ["arm"]["flex"]["left"]   = ['w', 'p1', 's']  
SEQ["arm"]["flex"]["right"]  = ['r', 'p1' 'f'] 
SEQ["arm"]["flex"]["both"]   = ['w', 'r', 'p1', 'f', 's']  

SEQ["arm"]["wave"] = {}  
SEQ["arm"]["wave"]["left"]   = ['a', 's' , 'p1', 'q', 'w']  
SEQ["arm"]["wave"]["right"]  = ['g', 'h', 'p1' , 't', 'y'] 
SEQ["arm"]["wave"]["both"]   = ['a', 's', 'g', 'h', 'p1', 't', 'y', 'q', 'w']  
"""
RESETS = ["q", "w","e", "r", "t", "y", "u", "i", "o"]

FLIPS = {}
FLIPS['q'] = 'a'
FLIPS['w'] = 's'
FLIPS['e'] = 'd'
FLIPS['r'] = 'f'
FLIPS['t'] = 'g'
FLIPS['y'] = 'h'
FLIPS['u'] = 'j'
FLIPS['i'] = 'k'
FLIPS['o'] = 'l'
FLIPS['a'] = 'q'
FLIPS['s'] = 'w'
FLIPS['d'] = 'e'
FLIPS['f'] = 'r'
FLIPS['g'] = 't'
FLIPS['h'] = 'y'
FLIPS['j'] = 'u'
FLIPS['k'] = 'i'
FLIPS['l'] = 'o'

CMDS       = {} 
CMDS['q']  = {"side": "left" , "part" : "shoulder"}
CMDS['a']  = {"side": "left" , "part" : "shoulder"}
CMDS['w']  = {"side": "left" , "part" : "Biceps"}
CMDS['s']  = {"side": "left" , "part" : "Biceps"}
CMDS['e']  = {"side": "left" , "part" : "hand"}
CMDS['d']  = {"side": "left" , "part" : "hand"}
#CMDS['r']  = {"side": "left" , "part" : ""}
#CMDS['f']  = {"side": "left" , "part" : " "}
CMDS['t']  = {"side": "right" , "part" : "shoulder"}
CMDS['g']  = {"side": "right" , "part" : "shoulder"}
CMDS['y']  = {"side": "right" , "part" : "Biceps"}
CMDS['h']  = {"side": "right" , "part" : "Biceps"}
CMDS['u']  = {"side": "right" , "part" : "hand"}
CMDS['j']  = {"side": "right" , "part" : "hand"}
#CMDS['i']  = {"side": "right" , "part" : " "}
#CMDS['k']  = {"side": "right" , "part" : " "}
"""
CMDS['o']  = {"side": "right" , "part" : "head"}
CMDS['l']  = {"side": "left" , "part"  : "head"}
"""
"""
CMDS['z']  = {"side": "all" , "part" : "all"}
CMDS['x']  = {"side": "all" , "part" : "all"}
CMDS['c']  = {"side": "all" , "part" : "wheels"}
CMDS['v']  = {"side": "all" , "part" : "wheels"}
CMDS['b']  = {"side": "all" , "part" : "wheels"}
CMDS['n']  = {"side": "all" , "part" : "wheels"}
""" 

def rand_cmds(current_cmds=""):
   """
   
   """
   actions = []
   potential = [k for k in CMDS.keys() if k  in current_cmds]
   i_len = len(potential) - 1
   for i in range(0, random.randint(2, 6)):
       i_a = random.randint(0, i_len)
       a = potential[i_a]
       actions.append(a)
       actions.append("p.1")

   return actions

def rand_sequence(current_states={}):
   """
   
   """ 
   parts = [k for k in SEQ.keys() if k not in "head"] 
   i_len = len(parts) - 1
   cmds = []

   for key,  val in current_states.items():
       if val:
           i_moveit = random.randint(0, 10)
           if i_moveit > 4:
               cmds.append(FLIPS[key]) 
           
   return cmds 


def rand_sequence_old(current_states={}):
   """
   
   """ 
   parts = [k for k in SEQ.keys() if k not in "head"]

   i_len = len(parts) - 1
   i_loops = 0
   i_found = 0
   cmds = []
   for side in ['left', 'right']:
     i_loops = 0
     while i_loops < 6:
       i_loops += 1 
       ipart = random.randint(0, i_len)
       part = parts[ipart]

       actions = [k for k in SEQ[part].keys()] 
       i_len_actions = len(actions) - 1 
       i_action =  random.randint(0, i_len_actions)
       action   =  actions[i_action]
       #sides = [k for k in SEQ[part][action].keys()]  
       #i_len_side = len(sides) - 1 
       #i_side =  random.randint(0, i_len_side) 
       #side =  sides[i_side] 
       tcmds = SEQ[part][action][side] 
       b_new = True 
       for cmd in tcmds:
           if cmd in current_states:
               if current_states[cmd]:
                   b_new = False
                   break
       if b_new: 
           cmds.extend(tcmds)
           break 
       
   if 'o' in current_states:
       if  current_states['o']:
           cmds.append('l')
       else:
           cmds.append('o')
           
   elif 'l' in current_states:
       if  current_states['l']:
           cmds.append('o')
       else:
           cmds.append('l')
   else:
        cmds.append('o')
           
           
   """      
   print("")
   print("Current_states", current_states)
   print("part", part)
   print("action", action)
   print("side", side)
   print(" " )
   """  
   return cmds

def flip_sequence(base="a"):
   """
   
   """
   actions = []
   potential = list(CMDS.keys())
   i_len = len(potential) - 1
   for i in range(0, random.randint(2, 6)):
       i_a = random.randint(0, i_len)
       a = potential[i_a]
       actions.append(a)
       actions.append("p.1")

   return actions

def sequences(sequence, current_states):
     """
     
     
     """
     if sequence['part'] == "random":
         
         cmds = rand_sequence(current_states )   
         return  cmds, current_states
     
     elif sequence['part'] == "light":
        if sequence['action'] == "color":
            if sequence['side'] == "red":
                 return ['l1'] , {}
            elif sequence['side'] == "green":
                 return ['l2'] , {}
            elif sequence['side'] == "blue":
                 return ['l3']  , {}
            elif sequence['side'] == "yellow":
                 return ['l4'] , {}
             
     #TODO system command like rest
     else:
         try:
             cmds = SEQ[sequence['part']][sequence['action'] ][sequence['side']]  

         except:
             print('Sequence missing', sequences) 
             t = open( './seq.error.log', 'a')
             t.write(str(sequence) + "\n")
             cmds  = rand_sequence(current_states)    
         
         return  cmds, current_states
     
     return [],  current_states