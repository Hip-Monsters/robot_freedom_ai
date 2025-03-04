# -*- coding: utf-8 -*-
  
"""
Description: The age 
Notes: Set up two motors:
       pins: 17 & 22 Right motors
       pins: 24 & 23 Left motors
"""
import datetime
import time
import random

try:
   import RPi.GPIO as gpio 
except:
   gpio = None

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot")  
parser.add_argument("-f", "--file"         , default="NA")  
parser.add_argument("-c", "--command_style", default="sequence")  
parser.add_argument("-v", "--verbose"      , default=False)  
 

# List of valid movements for the robot
## not for makerfaire MOVEMENT_DIRECTIONS = ["f", "s", "r", "l","b"]
MOVEMENT_DIRECTIONS = ["f",  "r", "l", "b"]

# Define minium length of time to robot should go in any one direction
MOVE_LENGTH_MIN = 2
 

class MOBILITY_GPIO(object):
    """
    
    """
    
    def __init__(self, nerves): 
        """
        Tells the RaspberryPi the ports are for outputing commands
        """  

        self.nerves     = nerves
  
        gpio.setmode(gpio.BCM)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)
        gpio.setup(25, gpio.OUT)
        gpio.setup(16, gpio.OUT) 
 
        "Initiate robot as stopped"
        self.current_direction = "s"
        self.b_forward_ok      = True 

        # Set last time movement changed to now
        self.last_move_time = datetime.datetime.now()
 
    def move(self, direction, wait_len):
        """
        Sends commands to the robot using gpio 
        
        """ 
        self.current_direction = direction
        
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
            self.nerves.set("stimuli", "move_forward" + ":" +  "focused" ) 
    
        elif direction == "b":
            gpio.output(27, True)
            gpio.output(22, False)
            gpio.output(23, False)
            gpio.output(24, True)
            print("\r Reverse" , end ="")
            self.nerves.set("stimuli", "move_backward" + ":" +  "focused" ) 
    
        elif direction == "l": 
            gpio.output(27, True)
            gpio.output(22, False)
            gpio.output(23, True)
            gpio.output(24, False)
            print("\r Left", end ="")
            self.nerves.set("stimuli", "move_left" + ":" +  "focused" ) 
    
        elif direction == "r": 
            gpio.output(27, False)
            gpio.output(22, True)
            gpio.output(23, False)
            gpio.output(24, True)
            print("\r Right" , end ="")
            self.nerves.set("stimuli", "move_right" + ":" +  "focused" ) 
         
        elif direction == "s": 
            gpio.output(27, False)
            gpio.output(22, False)
            gpio.output(23, False)
            gpio.output(24, False)
            print("\r Right" , end ="")
            self.nerves.set("stimuli", "move_halted" + ":" +  "alert" ) 
         
        # sleep before finishing up commands
        
        time.sleep(.1)
        # Release control
        gpio.cleanup()  

    def random_move(self):
        """
        #if time_since_last_change  > MOVE_LENGTH_MIN: 
        """ 
        # Filter out current move from valid moves
        valid_moves = [v for v in MOVEMENT_DIRECTIONS if v != self.current_direction]
            
        # Pick a movement randomly
        self.current_direction = random.choice(valid_moves)
          
        rnd_pause = random.randint(0, 2)
                
        #Change direction
        self.move(self.current_direction,rnd_pause )
            
        # Set last movment time
        self.last_move_time = datetime.datetime.now()

    def detected_wall(self, time_since_last_change):
        """
        """
        global MOVE_LENGTH_MIN
        global MOVEMENT_DIRECTIONS
       
        self.current_direction = 'r' 
        self.move("s", 0 )
        self.nerves.set("stimuli", "move_halted" + ":" +  "alert" )  
        time.sleep(.1)  
               
        self.b_forward_ok = False  
        #Back up
        for pause in [.1, .15, .2]:
            self.move('s', 1 ) 
            time.sleep(pause)  
 
        self.current_direction  = "f"
        self.random_move(self.current_direction )

        #Change direction
        #detect, amplitude = self.nerves.pop("distance") 
        #if detect is False:  
        self.b_forward_ok = True

        time.sleep(1)
        self.current_direction  = "f"  
        self.move(self.current_direction , 1 )
           
if __name__ == "__main__":
    """
   
     """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot   
  
    mouse = MOBILITY_GPIO(robot)
    mouse.monitor()
