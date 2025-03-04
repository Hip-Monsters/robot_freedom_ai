# -*- coding: utf-8 -*-
"""
Description: The agent daemon that allows the Artifical Intelligence to process sensors signals and control the robot.
Author: Mood_Relate.org 
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024
Version: 4.0
Plaftorm: RaspberryPi
License: MIT License 
"""
import json
import sys  
import csv
import datetime  
import time  

####    Libraries   ################
 
 
import argparse

parser = argparse.ArgumentParser() 

sys.path.append("..")
from  errors import  handle_exceptions
 
    
class Responder(object):
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


        self.mobility = self.agent.mobility
