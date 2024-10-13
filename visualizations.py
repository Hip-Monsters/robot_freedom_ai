# -*- coding: utf-8 -*-
  
"""
Description: Viualization daemon that expresses emotion and sensor input.
Author: HipMonsters.com 
License: MIT License
"""

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame,math

#import pyttsx
from pygame import gfxdraw
import random

from pygame.locals import *
from nerves         import Nerves
 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot")   

green        = (153, 255, 153)
orange       = (250, 196, 133)
blue         = (174, 205, 255)
yellow       = (255, 255, 153)
red          = (255, 153, 153)
purple       = (127, 19,  230)
cyan         = (153, 255, 255)
pink         = (255, 212, 255)
light_purple = (210, 186, 255)
gold         = (255, 215, 50 )


SENSES = {}
SENSES["distance"]    = {"color":green}
SENSES["movement"]    = {"color":orange}
SENSES["noise"]       = {"color":blue}
SENSES["speech"]      = {"color":gold} 
SENSES["balence"]     = {"color":red}
SENSES["temperature"] = {"color":pink}
SENSES["humidity"]    = {"color":cyan}
SENSES["quiet"]       = {"color":light_purple} 
SENSES["touch"]       = {"color":pink} 
SENSES["light"]       = {"color":yellow}  
SENSES["identification"]  = {"color":pink}  
 


class Visualizations():

    def __init__(self, robot):
        """
      
        """ 
        pygame.init()
        self.PI       = math.pi
        self.nerves   =  Nerves(robot)  
        self.status   = "Stimuli : none  Mood : neutral"  
        self.clock    = pygame.time.Clock()

        pygame.display.set_caption('Robot Freedom ' + robot)
     #   pygame.display.set_icon(pygame.image.load('./favicon.ico'))
       #1024x600 
      #  self.screen = pygame.display.set_mode((640, 480))
        self.x_dim  = 600
        self.y_dim  = 1024
        self.x_start  =  int(self.x_dim /2)
        self.y_start  =  int(self.y_dim /2)
        self.screen = pygame.display.set_mode((self.x_dim, self.y_dim))
       # self.screen = pygame.display.set_mode((300, 512))
        self.info   = pygame.font.SysFont('Comic Sans MS', 20)


        pygame.mouse.set_cursor(*pygame.cursors.arrow) 
        self.back = (255,255,255)
        self.color = (255,255,0) 
        self.history     =  []


 
    def serve_forever(self):
        """
        
        """
        i = 1
        while True: 
            self.screen.fill(self.back) 
 
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
 
                pygame.gfxdraw.filled_circle(self.screen, x  ,y,radius, color)

                if  circle["x"] < self.x_dim + 100  and   circle["y"] < self.y_dim  + 100  and   circle["x"] > -100  and   circle["y"] > -100:
                   fin.append(circle)

            detect, stimuli_mood = self.nerves.pop("stimuli")  
            self.history  = fin
            if detect:
                stimuli, mood = stimuli_mood.split(":")
                self.status   = "Stimuli : " + stimuli + " Mood : " + mood
 
                setting       = SENSES[stimuli]  
                pygame.gfxdraw.filled_circle(self.screen,
                                             self.x_start,
                                             self.y_start,
                                             100,
                                             setting["color"])
                 
                self.history.append({"x":self.x_start, 
                                     "y":self.y_start, 
                                     "radius":100, 
                                     "stimuli" : stimuli,
                                     "color":setting["color"],
                                     "direction" : random.randint(1,8)}) 
            else: 
               pass
                

            text_surface = self.info.render(self.status, False, blue)
            self.screen.blit(text_surface, (11,11))
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60000) 
            pygame.time.wait(1000)
 



if __name__ == "__main__":
    """
    python3 Visualizations.py -m serve -r number_3 
    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot    

    voice  = Visualizations(robot )
    if mode == "serve":
     
        voice.serve_forever()