# -*- coding: utf-8 -*-
  
"""
Description: Controller for Arduino 
Author: HipMonsters.com 
License: MIT License
""" 

from os import system   
import time    
import serial 
import serial.tools.list_ports 
 
   
class Controller(object):

    def __init__(self, robot, strict=True):
        """
        
        """
        self.strict  = strict
        self.devices = {}
        self.robot   = robot

    
    def connect_to_robots(self,  robots):
       """

       """ 
       print("Connecting to Devices...                                  ", end ="")
       for key, vals in robots.items():
           
           val, snd = vals 
          # try:
           if 1 == 1:
               arduino = serial.Serial(port=val) 
               self.devices[key] =  arduino 
               print("\r Resetting device " + val +   "                  " , end="")   
               self.write("z\n", key)   
               time.sleep(.1) 
         #  except:
          #     print("Warning, Robot did not connect!")
           #    self.devices[key] =  lambda x: print(x) 
              
    
       print("\rCompleted connecting devices.                                  ", end="") 
       return  self.devices


    def write(self, cmd, robot = None): 
       """

       """ 
       if robot is None:
          robot =  self.robot 
       arduino = self.devices[robot] 
       try:
          arduino.write(str.encode(cmd))   
          arduino.flush() 
          time.sleep(.1) 
       except serial.SerialException:
          print("/r Error connection to devices!!", end="")
 
 
if __name__ == "__main__":
    """
    """ 

