#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: HipMonsters.com  
License: MIT License  
""" 

from . handler import Handler, handle_exceptions


class NervesHandler(Handler): 
    """
    
    """

    @handle_exceptions 
    def wait_for_signal(self, signal):
       """
       
       """ 
       while True:
           val =  self.agent.nerves[signal]
           if val is not False:
                break
           
    @handle_exceptions 
    def wait_fo_messagel(self, signal):
       """
       
       """ 
       while True:
           val =  self.agent.nerves[signal]
           if val is not False:
                   break
            