#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: HipMonsters.com  
License: MIT License  
"""  
from . handler import Handler, handle_exceptions 
import datetime 

class MemoryHandler(Handler): 
    """
    
    """

    @handle_exceptions   
    def remember(self, event,  value):
        """
        
        """ 
        if  event not in  self.agent.st_memory.memory :
            self.agent.st_memory.memory[event]  = []

        self.agent.st_memory.memory[event] = [datetime.datetime.now(),  value]
