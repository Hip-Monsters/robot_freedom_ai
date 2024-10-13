# -*- coding: utf-8 -*-
#!/usr/bin/env python
  
"""
Description: Console for monitoring daemons and agents.
Author: HipMonsters.com 
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024
Version: .7
Plaftorm: RaspberryPi
License: MIT License  
"""


import platform
import time
import cmd
import json
from getpass import unix_getpass

OS = "LINUX"
if platform.system() == 'Windows':
  OS = "WIN"
elif platform.system() == 'Darwin': 
  OS = "OSX"
 
from nerves         import Nerves 
from client         import Communication
  

# password = unix_getpass('Password: ')
class RobotFreedomShell(cmd.Cmd):

    intro  = 'Welcome to the Robot Freedom shell. Type help or ? to list commands.\n'
    prompt = '(robot) '
    file   = None

    def __init__(self, user, com_type="remote"):
        """
        
        """
        cmd.Cmd.__init__(self)
        self.user= user
        self.com_type = com_type 
        self.robot = "number_3"
        if self.com_type == "local":
             self.nerves = Nerves('User')
        else:
            self.communication = Communication(self.user)
            self.communication.connect()
            self.communication.send("WORLD", "AWAKE")
        print("Communication Channel Established."    )

    def __send_cmd(self, key ,  param ):
        """
        
        """
        if self.com_type == "local":
             self.nerves.set(key, param)
        else:
            self.communication.send(self.robot,  key +  ":" +  param ) 

 
    def do_set_robot(self, arg):
        self.robot = arg
 
    def do_forward(self, arg):
        'Move robot forward by the specified distance:  FORWARD 10' 
        self.__send_cmd("remote_cmd", "action:" +  "f")

    def do_right(self, arg):
        'Turn robot right by given number of degrees:  RIGHT 20'
        self.__send_cmd("remote_cmd", "action:" +  "r")  

    def do_left(self, arg):
        'Turn robot left by given number of degrees:  LEFT 90'
        print(arg.lower())
        self.__send_cmd("remote_cmd", "action:" +  "l")  

    
    def do_mood(self, arg):
        'all signals : Mood' 
        self.__send_cmd("remote_cmd",  "roll:" + arg)   
    
    def do_chat(self, arg):
        'all signals : Mood' 
        self.__send_cmd("remote_cmd",  "chat:" + arg)   

    
    def do_signals(self, arg):
        'all signals :  SIGNALS'
        print('')
        sigs =  self.nerves.all_signals( ) 
        print(sigs) 

    def do_roll(self, arg):
        'all signals :  ROW 6d' 
        self.__send_cmd("remote_cmd",   "roll:" + arg)   

    
    def do_speak(self, arg):
        'Speak'
        print('')
        cmd = {"cmd":"speak:" , "text" :arg.lower() }
        self.__send_cmd("remote_cmd", json.dumps(cmd))   
    
    def do_shutdown(self, arg):
        'Stop   and exit:  BYE'
        print('')
        self.__send_cmd("remote_cmd", "action:" +  "shutdown")  
        return True
    
    def do_bye(self, arg):
        'Stop   and exit:  BYE'
        print('')
        self.__send_cmd("remote_cmd", "action:" +  "bye") 
        self.close()
        return True
  

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':
  #  RobotFreedomShell("user", "local").cmdloop()
    RobotFreedomShell("user", "remote").cmdloop()
    