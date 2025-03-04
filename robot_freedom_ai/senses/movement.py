# -*- coding: utf-8 -*-
"""
Description: Sensor daemon for movement.
Author: HipMonsters.com 
License: MIT License
"""
import json
from ._sense  import SenseBase

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-a", "--args")     

class  Movement(SenseBase):
    """
    
    """

    def __init__(self,robot, nerves, config, settings, pins ={"pin_1":31}):
        """
        
        """
        super().__init__(robot, 
                         nerves, 
                         config,  
                         settings, "movement")
        self.pins = pins 
        
        if self.os == "LINUX":
               
            import RPi.GPIO as GPIO 
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pins["pin_1"], GPIO.IN) 
            self.GPIO = GPIO 
              
              

if __name__ == "__main__":
    """ 

    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot   
    args    = json.loads(args.args  ) 
 
    movement  = Movement(robot, args )
    if mode == "serve":
        movement.serve_forever()
