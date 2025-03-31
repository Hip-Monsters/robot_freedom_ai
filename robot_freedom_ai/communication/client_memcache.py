#!/usr/bin/python
# -*- coding: utf-8 -*- 

"""
Description: Interface for Communication (memcache) to connect components to agent(s).
Author: HipMonsters.com 
License: MIT License
"""  
from os import system   
import time
from pymemcache.client import base
import json

class Client(object):

    
    def __init__(self,  robot  , ip=None):
        
        self.header_length = 10
        
        if ip is None:    
           self.ip =   "127.0.0.1"
        else:
           self.ip =  ip
        
        self.port = 11211
        self.client = base.Client((self.ip, self.port))
        self.client.set('log', json.dumps({}) ) 
        self.robot = robot 
        self.empty = json.dumps([])

    def __permission(self):
        """
        
        """
        
        while 1:
             message = self.client.get( self.robot + "_locked" )
             if message ==0:
                 return True
             time.sleep(.1)

        return False

    def connect(self):
        """
        
        """ 
        self.semd( self.robot )
        return True
    
    '''  
    def check_for_a_message(self, recipient,  expected_reply , sent_from):
        """ 
        check_for_a_message("number2", "step 1 done?", "yes")

        """
        messages = self.client.get( self.robot )

        self.client.set( self.robot , [])
    ''' 

    def check_messages_for(self, mess):
        """ 

        """  
        b_found = False
        messages = [""]

        self.set(self.robot + "_locked", 1) 
        messages = self.client.get( "notification" )
        
        if messages is not None:
            for mess in messages:
                if  mess["message"].lower() == mess.lower():
                    self.client.set( "notification", self.empty )
                    self.set(self.robot + "_locked", 0)
                    return True , messages[0]
                 
        return b_found ,  messages[0]  
   
        
    def check_messages(self):
        """ 

        """  
        b_found = False
        messages = [""]

        self.set(self.robot + "_locked", 1) 
        messages = self.client.get( self.robot )

        if messages is not None: 
            self.client.set( self.robot , self.empty)
            self.set(self.robot + "_locked", 0)
            return True , messages[0]["message"]
        
        self.set(self.robot + "_locked", 0)

        return b_found, messages[0]


    def wait_for_a_message(self, recipient,  expected_reply , sent_from):
        """
        
        """
        detect = False
        val    = "" 

        b_found = False
        messages = []

        self.set(self.robot + "_locked", 1) 
        messages = self.client.get( self.robot )
        
        if messages is not None:
            for mess in messages:
                if  mess["from"] == sent_from and  mess["message"] == expected_reply:
                    self.set(self.robot + "_locked", 0)
                    return True , messages[0]
         
        self.set(self.robot + "_locked", 0)
        return  detect, val   
                        

    def send(self,  recipient,  message ): 
        """
        """

        payload = {"recipient":recipient, 
                   "from":  self.robot  , 
                   "message" : message }
        
        self.set(recipient, json.dumps(payload))
 

    def set(self, key, value ): 
        """
        """ 

        value = json.dumps(value)
        value = value.encode('utf-8').strip() 
        key = key.encode('utf-8').strip() 

        self.client.set( key, value ) 
    
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
                  self.client.set( key, [] ) 
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