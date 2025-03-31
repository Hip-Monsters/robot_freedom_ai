# -*- coding: utf-8 -*-
  
"""
Description: Visualization daemon that expresses emotion and sensor input.
Author: HipMonsters.com 
License: MIT License
""" 
import math 
import random  
import time
from turtle import Turtle

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot")   

green        = "green"#(153, 255, 153)
orange       = "orange"#(250, 196, 133)
blue         = "blue"#(174, 205, 255)
yellow       = "yellow"#(255, 255, 153)
red          = "red"#(255, 153, 153)
purple       = "purple"#(127, 19,  230)
cyan         = "cyan"#(153, 255, 255)
pink         = "pink"#(255, 212, 255)
light_purple = "purple"#(210, 186, 255)
gold         = "gold"#(255, 215, 50 )


SENSES = {}
SENSES["distance"]    = {"color":green}
SENSES["movement"]    = {"color":orange}
SENSES["noise"]       = {"color":blue}
SENSES["speech"]      = {"color":gold} 
SENSES["balance"]     = {"color":red}
SENSES["temperature"] = {"color":pink}
SENSES["humidity"]    = {"color":cyan}
SENSES["quiet"]       = {"color":light_purple} 
SENSES["touch"]       = {"color":pink} 
SENSES["light"]       = {"color":yellow}  
SENSES["identification"]  = {"color":pink}  
 

#https://docs.python.org/3/library/turtle.html
class MainDisplayLite():

    def __init__(self,  robot, nerves, config, settings):
        """
      
        """ 
        self.app      = Turtle()
        self.PI       = math.pi
        self.robot    = robot  
        self.nerves   = nerves  
        self.settings = settings  
        self.config   = config   
        self.status   = "Stimuli : none  Mood : neutral"   
        self.app.screen.title('Robot Freedom ')
        self.app.screen.bgcolor("black")  
        self.x_dim  = 600
        self.y_dim  = 1024
        self.x_start  =  int(self.x_dim /2)
        self.y_start  =  int(self.y_dim /2)  
        self.back = (255,255,255)
        self.color = (255,255,0) 
        self.history     =  []  
 
    def serve_forever(self):
        """
        
        """
        i = 1
        while True:  
 
            fin  = []
            for circle in self.history:
 
                radius = circle["radius"]
                color  = circle["color"]

                if    circle["direction"] == 1:

                    circle["x"] = circle["x"]  - 5
                    circle["y"] = circle["y"]  + 5
                    x           = circle["x"]
                    y           = circle["y"] 

                elif  circle["direction"] == 2:
                    circle["x"] = circle["x"] - 15
                    circle["y"] = circle["y"]
                    x           = circle["x"]
                    y           = circle["y"] 

                elif  circle["direction"] == 3:
                    circle["x"] = circle["x"] 
                    circle["y"] = circle["y"] - 10
                    x           = circle["x"]
                    y           = circle["y"] 

                elif  circle["direction"] == 4:
                    circle["x"] = circle["x"] - 5
                    circle["y"] = circle["y"] - 5
                    x           = circle["x"]
                    y           = circle["y"] 

                elif  circle["direction"] == 5:
                    circle["x"] = circle["x"] + 10
                    circle["y"] = circle["y"]
                    x           = circle["x"]
                    y           = circle["y"] 

                elif  circle["direction"] == 6:
                    circle["x"] = circle["x"]  
                    circle["y"] = circle["y"] + 10
                    x           = circle["x"]
                    y           = circle["y"] 

                elif  circle["direction"] == 7:
                    circle["x"] = circle["x"]  + 5
                    circle["y"] = circle["y"]  + 5
                    x           = circle["x"]
                    y           = circle["y"] 

                elif  circle["direction"] == 8:
                    circle["x"] = circle["x"] 
                    circle["y"] = circle["y"] + 5
                    x           = circle["x"] - 5
                    y           = circle["y"] 
                ###

                if  circle["x"] < self.x_dim + 100  and   circle["y"] < self.y_dim  + 100  and   circle["x"] > -100  and   circle["y"] > -100:
                   fin.append(circle)

            detect, stimuli_mood = self.nerves.pop("stimuli")  
            self.history  = fin
            if detect:
                stimuli, mood = stimuli_mood.split(":")
                self.status   = "Stimuli : " + stimuli + " Mood : " + mood 
                setting       = SENSES[stimuli]    
                direction = random.randint(1,8)
                self.history.append({"x":self.x_start, 
                                     "y":self.y_start, 
                                     "radius":100, 
                                     "stimuli" : stimuli,
                                     "color": setting["color"],
                                     "direction" : direction}) 
             
                self.app.color(setting["color"])
                if direction == 1:
                    self.app.left(45) 
                elif direction == 2:
                    self.app.left(90) 
                elif direction == 3:
                    self.app.left(135) 
                elif direction == 4:
                    self.app.left(180) 
                elif direction == 5:
                    self.app.left(225) 
                elif direction == 6:
                    self.app.left(270) 
                elif direction == 7:
                    self.app.left(315) 
                elif direction == 8:
                    self.app.left(360)  

                self.app.forward(50) 

           # self.app.(self.status ) 
           # https://stackoverflow.com/questions/64940957/turtle-control-the-rate-of-refresh-using-sleep-does-not-refresh-properly
            time.sleep(1)
 



if __name__ == "__main__":
    """ 

    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot    

    voice  = MainDisplayLite(robot )
    if mode == "serve":
     
        voice.serve_forever()