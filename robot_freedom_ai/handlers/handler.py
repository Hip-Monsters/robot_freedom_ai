#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: HipMonsters.com  
License: MIT License  
"""   
import sys 
sys.path.append("..")
from  errors import  handle_exceptions
 
    
class Handler(object):
    """
    
    """
    
    def __init__(self,   agent ):
        """ 
        'agent', 'config', 'nerves', 'os', 

        """ 
 
        self.agent         = agent  
        self.polling_rate  = agent.polling_rate
        self.robot         = agent.robot
        self.video         = agent.video
        self.settings      = agent.settings
        self.os            = agent.config.OS
        self.config        = agent.config.CONFIG   
        self.verbose       = agent.config.VERBOSE  
        self.sequence_format = agent.sequence_format
        self.nerves        = agent.nerves