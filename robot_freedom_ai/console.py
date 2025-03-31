# -*- coding: utf-8 -*-
#!/usr/bin/env python
  
"""
Description: Console for monitoring daemons and agents.
Author: HipMonsters.com 
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024
Version: .7
Platform: RaspberryPi
License: MIT License  
"""

import sys  
import time
import cmd 
import config  
from communication.base_cmds      import BaseCmds

OS =  config.OS
 
import argparse
from communication.nerves         import Nerves 
from communication.client         import Client

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--robot" , type=str,  default='', required=False)  
parser.add_argument("-n", "--networked" , type=int,  default=1, required=False)  
parser.add_argument("-m", "--mode"   , type=str,  default='monitor', required=False)  
  
from errors import handle_exceptions

# password = unix_getpass('Password: ')
class Shell(cmd.Cmd):

    intro  = 'Welcome to the Robot Freedom terminal. Type help or ? to list commands.\n'
    prompt = '(robot) '
    file   = None

    def __init__(self, robot, networked="remote"):
        """
        
        """
        cmd.Cmd.__init__(self) 

        global config
        self.config = config 
        self.networked = networked

        if robot == "":
            self.robot = self.config.CONFIG["robot"]  
        else:
            self.robot = robot
            
        self.nerves = Nerves(self.robot)
 
        if self.networked == 1: 
            t_ip =   list(config.NET_CONFIG["hubs"].keys())[0]  
            self.communication = Client(self.robot,t_ip)  
            self.communication.connect()
            self.communication.send("WORLD", "AWAKE")
        else:
            self.communication = {}
             
        self.base_cmds  = BaseCmds(self.robot, 
                                   self.config,
                                   self.communication,
                                   self.nerves,
                                   self.networked)  
        print("Communication Channel Established."    )

    @handle_exceptions 
    def do_docs(self, arg):
        'all signals :  signals 1' 
        docs = self.base_cmds.do_docs(arg)
        for line in docs:
            print(line)  

    @handle_exceptions 
    def do_set_robot(self, arg): 
        'set_robot squirrel'
        self.robot = arg 

    @handle_exceptions 
    def do_forward(self, arg):
        'forward 1 ' 
        self.base_cmds.do_forward(arg)

    @handle_exceptions 
    def do_right(self, arg):
        'right 1 '
        self.base_cmds.do_right(arg)

    @handle_exceptions 
    def do_left(self, arg):
        'left 1 ' 
        self.base_cmds.do_left(arg)

    @handle_exceptions 
    def do_mood(self, arg):
        'all signals : mood' 
        self.base_cmds.do_left(arg)
    
    @handle_exceptions 
    def do_monitor(self, arg):
        'all monitor : monitor 1' 
        if self.nerves is None:
             self.nerves = Nerves('User')
        done = set([])
        while 1:
            for topic in ["chat", "chat_responses", "speech", "sound"]  :
              found, mess = self.nerves.new(topic)
              if found and mess not in done:
                  print(topic , mess)
                  done.add(mess)
              time.sleep(.1)

    @handle_exceptions 
    def do_direct_chat(self, arg):
        'all signals : direct_chat "how are you' 
        val = self.base_cmds.do_direct_chat(arg)
        print(val)

    @handle_exceptions 
    def do_chat(self, arg):
        'all signals : chat "how are you doing?"' 
        val = self.base_cmds.do_chat(arg)
        print(val)

    @handle_exceptions 
    def do_dinner(self, arg):
        'dinner'
        val = self.base_cmds.do_dinner(arg)
        print(val)
    
    @handle_exceptions 
    def do_signals(self, arg):
        'all signals :  signals 1' 
        sigs =  self.nerves.all_signals( ) 
        print(sigs)  

    @handle_exceptions 
    def do_roll(self, arg):
        'all signals :  roll 6d'  
        val = self.base_cmds.do_roll(arg)
        print(val)

    @handle_exceptions 
    def do_move(self, arg):
        'all signals :  move raise,left,arm @squirrel'  
        val = self.base_cmds.do_move(arg)
        print(val)

    @handle_exceptions 
    def do_run(self, arg):
        'all signals :  run ../../data/scripts/__remote_test.csv'    
        val = self.base_cmds.do_run(arg)
        print(val)

    @handle_exceptions 
    def do_replay(self, arg):
        'all signals :  run ../../data/scripts/__remote_test.csv'    
        val = self.base_cmds.do_replay(arg)
        print(val)

    @handle_exceptions 
    def do_say(self, arg):
        'say "hello"'  
  
        val = self.base_cmds.do_speak(arg)
        print(val)

    @handle_exceptions 
    def do_speak(self, arg):
        'speak "hello"'  
  
        val = self.base_cmds.do_speak(arg)
        print(val)

    @handle_exceptions 
    def do_snapshot(self, arg):
        'snapshot 1' 
        val = self.base_cmds.do_snapshot(arg)
        print(val)
    
    @handle_exceptions 
    def do_shutdown(self, arg):
        'Stop   and exit:  shutdown'
        val = self.base_cmds.do_shutdown(arg)
        print(val)
         
    @handle_exceptions 
    def do_bye(self, arg):
        'Stop   and exit:  bye'
        val = self.base_cmds.do_bye(arg)
        print(val)
   

if __name__ == '__main__':
    """
    
    """ 

    args     = parser.parse_args()  
    robot    = args.robot 
    networked = args.networked 
    mode      = args.mode 
  
    try:
        Shell(robot, networked).cmdloop() 
    except KeyboardInterrupt:
        print ('Killed by user')
        sys.exit(0)


    