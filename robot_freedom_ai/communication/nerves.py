#!/usr/bin/python
# -*- coding: utf-8 -*- 

"""
Description: Interface for Nerves (memcache) to connect components to agent(s).
Author: HipMonsters.com 
License: MIT License
""" 
 
from os import system   
from pymemcache.client import base
import json

class Nerves(object):

    
    def __init__(self,  name  , ip=None):
        
        self.header_length = 10
        
        if ip is None:    
           self.ip =   "127.0.0.1"
        else:
           self.ip =  ip
        
        self.port = 11211
        print((self.ip, self.port))
        self.client = base.Client((self.ip, self.port))
        self.client.set('log', json.dumps({}) ) 
 
    def set(self, key, value ): 
        """
        """
        tval = value 
        value = value.encode('utf-8').strip() 
        self.client.set( key, value )

        log = json.loads(self.client.get('log'))
        if key not in  log:
              log[key] = [0,""]

        icnt , pmess =   log[key]

        if pmess == "": 
            pmess = tval 

        if tval!= "": 
            icnt = icnt + 1

        log[key] = [icnt   , pmess]
        
        self.client.set('log', json.dumps(log) ) 
    
    def get(self, key ): 
        """
        """
        return self.client.get( key )
    
    def new(self, key ): 
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
                  return [True, val]

        return False , "" 
    
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