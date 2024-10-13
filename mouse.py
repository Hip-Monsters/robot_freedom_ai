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

from memory         import Memory
from nerves         import Nerves 
from client         import Communication
from controller     import Controller
from voice          import Voice
from sense_sound    import SenseSound
from sense_distance import SenseDistance 
from sense_movement import SenseMovement 
from camera         import Camera
from sound          import Sound
from balence        import Balence
from sequences      import sequences  
from security       import Security
from logo           import logo

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

class Mouse(object):
    """
    
    """
    
    def __init__(self, name): 
        """
        Tells the RaspberryPi the ports are for outputing commands
        """  

        self._space  = " ".join(['' for v in range(40)])
        self.name = name
        print("\r Connecting with devices ..."  + self._space , end="")
       
        gpio.setmode(gpio.BCM)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)
        gpio.setup(25, gpio.OUT)
        gpio.setup(16, gpio.OUT)
        self.LAST_MOVE_TIME = datetime.datetime.now()
        print("\r Connecting with Memory ..."  + self._space , end="")
        self.memory     = Memory(self.name)
        self.nerves     = Nerves(self.name)
        
        self.current_direction = "s"

        print("\rRobot and AI setup is complete." + self._space + self._space, end="")  
        print(logo())
        #print("Communicating IP    :"    + self.communication.ip  +  self._space )  
        print("Sensors             :"    +  " ".join(["voice","noise", "movement","distance","balence"])+  self._space ) 
        print("Components          :"    +  " ".join(["speach","device_contol","communication","mic", "camera"]) +  self._space) 
        print("AI Modules          :"    +  " ".join(["chat", "knowledge", "emotions", "motivations", "personality", "dream_inducer", "strategies" ]) +  self._space) 
        print("AI Learner          :"    +  " ".join(["gradient_descent", "BERT", "cosine_similarity","ANN" ]) +  self._space) 
        print("Security Modules    :"    +  " ".join(["firewall", "security", "cmd_filters", "threat_scores"]) +  self._space) 
        print("AI Ethics Modules   :"    +  " ".join(["asimovs_3_laws", "strategy_inhibitor", "stimuli_mitigation"])  + self._space)
        print("Welcome " + name  + self._space   )
        
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
            self.nerves.set("stimuli", "balence" + ":" +  "happy" ) 
    
        elif direction == "b":
            gpio.output(27, True)
            gpio.output(22, False)
            gpio.output(23, False)
            gpio.output(24, True)
            print("\r Reverse" , end ="")
            self.nerves.set("stimuli", "temperature" + ":" +  "happy" ) 
    
        elif direction == "l": 
            gpio.output(27, True)
            gpio.output(22, False)
            gpio.output(23, True)
            gpio.output(24, False)
            print("\r Left", end ="")
            self.nerves.set("stimuli", "noise" + ":" +  "happy" ) 
    
        elif direction == "r": 
            gpio.output(27, False)
            gpio.output(22, True)
            gpio.output(23, False)
            gpio.output(24, True)
            print("\r Right" , end ="")
            self.nerves.set("stimuli", "speach" + ":" +  "happy" ) 
         
        elif direction == "s": 
            gpio.output(27, False)
            gpio.output(22, False)
            gpio.output(23, False)
            gpio.output(24, False)
            print("\r Right" , end ="")
            self.nerves.set("stimuli", "quiet" + ":" +  "happy" ) 
         
        # sleep before finishing up commands
        time.sleep(.1)
        # Release control
        gpio.cleanup() 
       #  need to implement pulsise wave modulation lke :
       #  https://www.bing.com/search?q=pulse+width+modulation&FORM=AWRE
             
       # remeber direction a pulse (turn on and off)

    def monitor(self):
        """
        """
        global MOVE_LENGTH_MIN
        global MOVEMENT_DIRECTIONS
        # Loop forever
        CURRENT_DIRECTION = 'r'
        while True:
           
           detect, amplitude = self.nerves.pop("distance")  
           # Find the time in seconds since the last movement change
           time_since_last_change = (datetime.datetime.now() - self.LAST_MOVE_TIME).total_seconds()
     
           if detect:
                self.move("s", 0 )
                self.nerves.set("stimuli", "distance" + ":" +  "happy" ) 
                print("Sensed distance")
                time.sleep(.1)
               # self.nerves.set('distance', "")  
               
           b_forward_ok = True
           if detect or  time_since_last_change  > MOVE_LENGTH_MIN: 
               
               # If time since last change exceeds movement length run the code
               if time_since_last_change  > MOVE_LENGTH_MIN: 
                   
                   # Filter out current move from valid moves
                   valid_moves = [v for v in MOVEMENT_DIRECTIONS if v != CURRENT_DIRECTION]
            
                   # Pick a movement randomly
                   CURRENT_DIRECTION = random.choice(valid_moves)
                   if b_forward_ok ==False:
                       if CURRENT_DIRECTION == "f":
                           CURRENT_DIRECTION = "r" 
                       b_forward_ok = True
                   
                   # Random wait time
                   rnd_pause = random.randint(0, 2)
                
                   #Change direction
                   self.move(CURRENT_DIRECTION,rnd_pause )
            
                   # Set last movment time
                   self.LAST_MOVE_TIME = datetime.datetime.now()
               if detect: 
                  
                   #Change direction
                   self.move('s', 1 ) 
                   time.sleep(.25) 

                   self.move('b', 1 )  
                   time.sleep(.1) 
                   self.move('b', 1 ) 
                   time.sleep(.1)  
                   self.move('b', 1 ) 
                   time.sleep(.1)  

                   detect, amplitude = self.nerves.pop("distance")  
                   b_forward_ok = False
           else:
                   self.move(self.current_direction , 1 )
                                   
           time.sleep(.05)
           
if __name__ == "__main__":
    """
    python3 mouse.py -m monitor -r mouse 
 
    python3 mouse.py -m script -r number_3  -f ./scripts/script_1.csv  -c device -v True 
    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot   
  
    mouse = Mouse(robot)
    mouse.monitor()
