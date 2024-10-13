# -*- coding: utf-8 -*-
  
"""
Description: Sensor daemon for distance.
Author: HipMonsters.com 
License: MIT License
"""

import json
from sense_base import SenseBase 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-a", "--args" )    
 
 
class  SenseDistance(SenseBase):
    """
    
    """

    def __init__(self,name , args, pins ={"pin_trigger":4, "pin_echo":17}):
        """
        
        """  
        super().__init__(name, args, "distance")
        self.pins = pins 
        
        if self.os == "LINUX": 
            from gpiozero import DistanceSensor 
            self.ultrasonic = DistanceSensor(echo=self.pins["pin_trigger"], 
                                             trigger=self.pins["pin_echo"])
             
    def poll(self):
        """
        """ 
           
        if self.os == "LINUX":
            
            if self.ultrasonic.wait_for_in_range():             
               return [True ,"something near"]
               
        elif self.os == "OSX":
            
           if self.counter  >= 12:
               self.counter = 0
               return [True, "tisomething near"]
           
        return [False, "nothing"]
     

if __name__ == "__main__":
    """
    python3 sense_distance.py -m serve -r number_3  -a '{"max":30}'
    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot   
    args    = json.loads(args.args  ) 

    print(  "\r" + mode , end ="")
    distance  = SenseDistance(robot, args )
    if mode == "serve":
        distance.serve_forever()
