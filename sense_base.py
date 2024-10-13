# -*- coding: utf-8 -*-
  
"""
Description: Sensor daemon base class
Author: HipMonsters.com 
License: MIT License
"""

import platform
import time 
from nerves         import Nerves
 
 
class  SenseBase(object):
    """
    
    """

    def __init__(self, name , args, sense):
        """
        
        """ 
        self.os  = "LINUX"
        if platform.system() == 'Windows':
             self.os  = "WIN"
        elif platform.system() == 'Darwin': 
             self.os  = "OSX" 
        self.sense        = sense 
        self.name         = name  
        self.quietcount   = 0
        self.errorcount   = 0 
        self.args         = args
        self.polling_rate = 1 
        self.nerves       = Nerves(name) 
        self.counter      = 0
 
            
    def poll(self):
        """
        """ 
           
        if self.os == "LINUX":
            
            signal = self.GPIO.input(self.pins["pin_1"]) 
            if signal == 1:                
               return [True , "signal" ]
            
        elif self.os == "OSX":
           print(self.counter  ,  self.args["max"])
           if self.counter  >= 10 :  
               self.counter = 0
               return [True, "signal"]
  
        
        return [False, "na" ]
    
    def serve_forever(self): 
        """
        
        """

        while True:
           detected, val  = self.poll()
           if detected:
                self.nerves.set(self.sense, val)  

           time.sleep(self.polling_rate)
           self.counter = self.counter + 1
 