# -*- coding: utf-8 -*-
  
"""
Description: this dictionary defines sequence of movements for a robot for a provided term.
Author: HipMonsters.com 
License: MIT License
"""


import random 
CMDS  = {}
 
CMDS['q']  = {"side": "left" , "part" : "shoulder"}
CMDS['a']  = {"side": "left" , "part" : "shoulder"}
CMDS['w']  = {"side": "left" , "part" : "bicept"}
CMDS['s']  = {"side": "left" , "part" : "bicept"}
CMDS['e']  = {"side": "left" , "part" : "nad"}
CMDS['d']  = {"side": "left" , "part" : "hand"}
#CMDS['r']  = {"side": "left" , "part" : ""}
#CMDS['f']  = {"side": "left" , "part" : " "}
CMDS['t']  = {"side": "right" , "part" : "shoulder"}
CMDS['g']  = {"side": "right" , "part" : "shoulder"}
CMDS['y']  = {"side": "right" , "part" : "bicept"}
CMDS['h']  = {"side": "right" , "part" : "bicept"}
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

def rand_sequence():
   actions = []
   potential = list(CMDS.keys())
   i_len = len(potential) - 1
   for i in range(0, random.randint(2, 6)):
       i_a = random.randint(0, i_len)
       a = potential[i_a]
       actions.append(a)
       actions.append("p1")

   return actions

def sequences(sequence):
     """
     
     
     """
     if sequence['part'] == "random":
         return rand_sequence()
     
     elif sequence['part'] == "head":
        if sequence['action'] == "turn":
            if sequence['side'] == "left":
                 return ['o'] 
            elif sequence['side'] == "left":
                 return ['l'] 
     
     elif sequence['part'] == "hand":
        if sequence['action'] == "open":
            if sequence['side'] == "left":
                return ['e']
            elif sequence['side'] == "right":
                return ['i']
            elif sequence['side'] == "both":
                 return ['e','i']
            
        elif sequence['action'] == "close":
            if sequence['side'] == "left":
                return ['d']
            elif sequence['side'] == "right":
                return ['k']
            elif sequence['side'] == "both":
                return ['d','k']
            
        elif sequence['action'] == "open_close":
            if sequence['side'] == "left":
                return ['e', 'p4', 'd']
            elif sequence['side'] == "right":
                return ['i', 'p4', 'k']
            elif sequence['side'] == "both":
                return ['e','i','p4', 'd', 'k']
 
     elif sequence['part'] == "arm":
        if sequence['action'] == "raise":
            if sequence['side'] == "left":
                return  ['q','w']
            elif sequence['side'] == "right":
                return ['r','t']
            elif sequence['side'] == "both":
                return ['q','r','w','t']
        elif sequence['action'] == "lower":
            if sequence['side'] == "left":
               return ['a','s']
            elif sequence['side'] == "right":
                return ['f','g']
            elif sequence['side'] == "both":
                return ['a','f','s','g'] 

        elif sequence['action'] == "flex":
            if sequence['side'] == "left":
               return  ['w','p3', 's']
            elif sequence['side'] == "right":
               return  ['r','p3', 'f']
            elif sequence['side'] == "both":
               return  ['w','r','p','s','f']

        elif sequence['action'] == "wave":
            if sequence['side'] == "left":
               return  ['a','s', 'p2', 'q', 'w']
            elif sequence['side'] == "right":
               return  ['g','h', 'p2','t', 'y']
            elif sequence['side'] == "both":
               return  ['a','g', 's', 'h', 'p2','q', 't', 'w', 'y']
