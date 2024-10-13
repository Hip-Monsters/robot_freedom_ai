# -*- coding: utf-8 -*-
  
"""
Description: Sensor daemon for movement.
Author: HipMonsters.com 
License: MIT License
"""
import json
from sense_base import SenseBase

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-a", "--args")     

class  SenseMovement(SenseBase):
    """
    
    """

    def __init__(self, name, args , pins ={"pin_1":31}):
        """
        
        """
        super().__init__(name, args, "movement")
        self.pins = pins 
        
        if self.os == "LINUX":
               
            import RPi.GPIO as GPIO 
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pins["pin_1"], GPIO.IN) 
            self.GPIO = GPIO 
              
              

if __name__ == "__main__":
    """
    python3 sense_movement.py -m serve -r number_3  -a '{"max":70}'
    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot   
    args    = json.loads(args.args  ) 

    print(  "\r" + mode , end ="")
    movement  = SenseMovement(robot, args )
    if mode == "serve":
        movement.serve_forever()
