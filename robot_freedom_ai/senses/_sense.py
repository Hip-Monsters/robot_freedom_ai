# -*- coding: utf-8 -*-
  
"""
Description: Sensor daemon base class
Author: HipMonsters.com 
License: MIT License
"""
 
import time    

class  SenseBase(object):
    """
    
    """

    def __init__(self, robot,   nerves, config,  settings, sense, args={}):
        """
        
        """ 
        self.os           = config.OS 
        self.config       = config
        self.settings     = settings
        self.sense        = sense 
        self.robot        = robot  
        self.quietcount   = 0
        self.errorcount   = 0 
        self.args         = args
        self.polling_rate = .75
        self.nerves       = nerves
        self.counter      = 0
        self.log          = False
 
            
    def poll(self):
        """
        """ 
           
        if self.os == "LINUX":
            
            signal = self.GPIO.input(self.pins["pin_1"]) 
            if signal == 1:                
               return [True , "signal" ]
            
        elif self.os == "OSX": 
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

        
           self.counter = self.counter + 1
           time.sleep(self.polling_rate)
 