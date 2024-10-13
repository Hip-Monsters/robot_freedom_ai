# -*- coding: utf-8 -*-
  
"""
Description: Interface for Nerves (memcache) to connect components to agent(s).
Author: HipMonsters.com 
License: MIT License
""" 

import sys  
from os import system   
from pymemcache.client import base

class Nerves(object):

    
    def __init__(self,  name  , ip=None):
        
        self.header_length = 10
        
        if ip is None:    
           self.ip =   "127.0.0.1"
        else:
           self.ip =  ip
        
        self.port = 11211
        self.client = base.Client((self.ip, self.port))
 
    def set(self, key, value ): 
        """
        """
        value = value.encode('utf-8').strip() 
        self.client.set( key, value )
    
    def get(self, key ): 
        """
        """
        return self.client.get( key )
    
    def all_signals(self ): 
        """
        """
        res = {}
        for key, val in self.client.stats("items").items():
             res[key] = val 

        return res
 
    def pop(self, key ): 
        """
        """
        val = self.client.get( key )
        if val is None:
           val = ""
        else:
            val = val.decode().strip()   

        if val is not None:
            if val != "":  
               if val != "False":  
                  self.client.set( key,"" ) 
                  return [True, val]
                  
        return [False, ""]
    
    def stopped(self, key ): 
        """
        """
        val = self.client.get( key )
        if val is None:
           val = ""
        else:
            val = val.decode().strip()   
        if val is not None:
            if val != "":  
               if val != "False":   
                  return [False, val]
                  
        return [True, ""]
 
    def clear(self, key ): 
        """
        """ 
        self.client.set( key, False ) 

 
if __name__ == "__main__":
    """
    """ 