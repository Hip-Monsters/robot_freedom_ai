# -*- coding: utf-8 -*-
  
"""
Description: The agent daemon for the mouse robot that allows the Artifical Intelligence to process sensors signals and control the robot.
Author: HipMonsters.com 
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024
Version: 3.0
Plaftorm: RaspberryPi
License: MIT License 
Notes: Set up two motors:
       pins: 17 & 22 Right motors
       pins: 24 & 23 Left motors
"""
import datetime
import time
import random
import RPi.GPIO as gpio
 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot")  
parser.add_argument("-f", "--file"         , default="NA")  
parser.add_argument("-c", "--command_style", default="sequence")  
parser.add_argument("-v", "--verbose"      , default=False)  
 

# List of valid movements for the robot
## not for makerfaire MOVEMENT_DIRECTIONS = ["f", "s", "r", "l","b"]
MOVEMENT_DIRECTIONS = ["f",  "r", "l"]

# Define minium length of time to robot should go in any one direction
MOVE_LENGTH_MIN = 2

# Intial direction
CURRENT_DIRECTION = "f"

# Set last time movement changed to now
LAST_MOVE_TIME = datetime.datetime.now()

class Movement(object):
    """
    
    """
    
    def __init__(self, robot): 
        """
        Tells the RaspberryPi the ports are for outputing commands
        """  

        self._space  = " ".join(['' for v in range(40)])
        self.robot = robot
        print("\r Connecting with devices ..."  + self._space , end="")
       
        gpio.setmode(gpio.BCM)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)
        gpio.setup(25, gpio.OUT)
        gpio.setup(16, gpio.OUT)
        self.LAST_MOVE_TIME = datetime.datetime.now()
        print("\r Connected with GPIO."  + self._space , end="")   

        print("\rRobot and AI setup is complete." + self._space + self._space, end="")  
        
        
    def move(self, direction, wait_len = .1):
        """
        Sends commands to the robot using gpio 
        """
        
        gpio.cleanup() 
        gpio.setmode(gpio.BCM)
        gpio.setup(27, gpio.OUT)
        gpio.setup(22, gpio.OUT)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)
        #if directions is "f"
        if direction == "f":
            # Send command False (off) to port 17.
            gpio.output(27, False) 
            gpio.output(22, True)
            gpio.output(23, True)
            gpio.output(24, False)
    
            # Print direction to screen for debug
            print("\r Forward", end ="") 
    
        elif direction == "b":
            gpio.output(27, True)
            gpio.output(22, False)
            gpio.output(23, False)
            gpio.output(24, True)
            print("\r Reverse" , end ="") 
    
        elif direction == "l": 
            gpio.output(27, True)
            gpio.output(22, False)
            gpio.output(23, True)
            gpio.output(24, False)
            print("\r Left", end ="") 
    
        elif direction == "r": 
            gpio.output(27, False)
            gpio.output(22, True)
            gpio.output(23, False)
            gpio.output(24, True)
            print("\r Right" , end ="") 
         
        elif direction == "s": 
            gpio.output(27, False)
            gpio.output(22, False)
            gpio.output(23, False)
            gpio.output(24, False)
            print("\r Right" , end ="") 
         
        # sleep before finishing up commands 
        time.sleep(wait_len)

        # Release control
        gpio.cleanup() 

       #  need to implement pulsise wave modulation lke :
       #  https://www.bing.com/search?q=pulse+width+modulation&FORM=AWRE
             
       # remeber direction a pulse (turn on and off)
 
           
if __name__ == "__main__":
    """
   
    """  
  
    move = Movement("test")
    move.move("f", 1)
