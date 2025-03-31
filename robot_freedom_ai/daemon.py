# -*- coding: utf-8 -*-
"""
Description: Generic Daemon.
Author: HipMonsters.com 
Date Created: Jan 1, 2021
Date Modified: Oct 10, 2024
Version: 8.0
Platform: RaspberryPi
License: MIT License  
"""
  
import time 
import json  

import config
from communication.nerves         import Nerves   
from memory.lt_memory import   LemNormalize 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--module")  
parser.add_argument("-c", "--class_name")  
parser.add_argument("-r", "--robot")  
  

class Daemon(object):

    def __init__(self, module , classname, robot ):
        """
        
        """  
        robot         = robot.strip()
        nerves        = Nerves(robot)  
        module_name   = module.split(".")[-1]

        with open(config.DATA_PATH +  robot + "/settings.json") as f:
           data = ''
           for row in f:
              data += row  
           settings = json.loads(data)
 
        _mod          = __import__(module , fromlist=[None] ) 
        self.module   = getattr(_mod, classname )(robot,   nerves, config,  settings ) 
     
 
        return None     
         
                
           
if __name__ == "__main__":
    """  

    
    """
    args       = parser.parse_args()  
    module     = args.module    
    class_name = args.class_name    
    robot      = args.robot    
    daemon     = Daemon(module, class_name, robot)
    daemon.module.serve_forever()

 