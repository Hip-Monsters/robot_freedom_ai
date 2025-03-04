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

import random  
import time 
import csv  
  
 
 
class BaseCmds(object):
 
    def __init__(self, user, config, com, nerves, networked=1):
        """
        
        """ 
        self.user= user
        self.networked = networked 

        self.config  = config 
        self.robot = self.config.CONFIG["robot"]
        self.user= self.robot 

        self.nerves = nerves 
        if self.networked == 0:
            self.nerves = nerves
        else:
            self.communication = com 
 

    def __send_cmd(self, key ,  param ):
        """
        
        """
        print( self.networked, key, param)

        if self.networked == 0: 
             self.nerves.set(key, param)
        else: 
            if param.find("@") > 1:
                param , robot  = param.split('@', 1)
            else:
                robot = self.robot 
            self.communication.send(robot,  key + ":" +  param ) 

    def __get_messages(self, message, i_timeout = 10000):
        """
        
        """
        i_tot = 0 
        while True:
              b_message, s_message   = self.communication.check_messages( ) 
              if b_message: 
                 return  b_message, s_message
              
              if i_tot >=  i_timeout :
                  return False, ""
              i_tot += 1
            
              time.sleep(.1)

    def __wait_for(self, message, i_timeout = 10000):
        """
        
        """
        i_tot = 0 
        while True:
              b_message, s_message   = self.communication.check_messages_for(message ) 
              if b_message: 
                 return  b_message, s_message
              
              if i_tot >=  i_timeout :
                  return False, ""
              i_tot += 1
            
              time.sleep(.1) 
 
    def do_set_robot(self, arg):
        """
        
        """
        self.robot = arg  
    
    
    def do_mood(self, arg):
        'all signals : Mood' 
        self.__send_cmd("remote_cmd",  "return:mood")   
        return ""
    
    def do_chat(self, arg):
        'all chat : "Hi!"' 
        self.__send_cmd("remote_cmd",  "chat:" + arg)  
        return "" 
    
    def do_monitor(self, arg):
        'all monitor : Mood' 
        if self.nerves is None:
             self.nerves = Nerves('User')
        done = set([])
        while 1:
            for topic in ["chat", "chat_responses", "speech", "sound"]  :
              found, mess = self.nerves.new(topic)
              if found and mess not in done:
                  yield(topic , mess)
                  done.add(mess)
              time.sleep(.1)

    def do_direct_chat(self, arg):
        'chat' 
        if self.nerves is None:
             self.nerves = Nerves('User')
        self.nerves.set("chat","respond>"+ arg) 

        i   = 0
        val = "error"

        while True:
            done, val  = self.nerves.pop("chat_responses") 
            if i == 1000 or done:
                break
            time.sleep(.2)
            i += 1
        return val  
    
    def do_signals(self, arg):
        'all signals :  SIGNALS'
        print('')
        sigs =  self.nerves.all_signals( ) 
        return sigs

    def do_roll(self, prompt):
        'all signals :  ROW 6d'  
        response = "Command not found."
        if  prompt.startswith('20d'):
            response  = str(random.randint(1, 20)) 
        elif  prompt.startswith('12d'):
            response  = str(random.randint(1, 12)) 
        elif  prompt.startswith('6d'):
            response  = str(random.randint(1, 6)) 
        elif  prompt.startswith('10d'):
            response  = str(random.randint(1, 10)) 
        elif  prompt.startswith('4d'):
            response  = str(random.randint(1, 4)) 
        elif  prompt.startswith('100d'):
            response  = str(random.randint(1, 100)) 
        elif  prompt.startswith('flip'):
            response  = str(random.randint(1, 2)) 
        elif  prompt.startswith('8d'):
            response  = str(random.randint(1, 8))   
        return response 

    def do_sim_sense(self, arg):
        'all signals :  sim_sense light,1'  
        self.__send_cmd("direct_cmd",   "sim_sense:" + arg)  
        return "" 
    
    
    
    def do_video(self, arg):
        'Video' 
       # self.__send_cmd("remote_cmd", json.dumps(cmd))    
        if arg.strip() == "":
            arg = " NA "
        self.__send_cmd("remote_cmd",  "video:" + arg) 
        return "" 
    
    def do_snapshot(self, arg):
        'Snapshot' 
       # self.__send_cmd("remote_cmd", json.dumps(cmd))    
        if arg.strip() == "":
            arg = " NA "
        self.__send_cmd("remote_cmd",  "snapshot:" + arg) 
        return "" 
    
    def do_sleep(self, arg):
        'all signals :  sleep 30'  
        self.__send_cmd("direct_cmd",   "sleep:" + arg)  
        return "" 
    
    def do_move(self, arg):
        'all signals :  move raise,left,arm @squirrel' 
        #   dcmd = {"part": a_cmd[0], "action": a_cmd[1], "side": a_cmd[2]}
        self.__send_cmd("remote_cmd",   "move:" + arg)  
        return "" 

    def do_run(self, arg):
        'all signals :  run ./scripts/__remote_test.csv'   
        print("Checking status...")

        #detect, val = self.nerves.pop("spoke") 
        self.__wait_for("spoke", 10)
        b_random_movements = False
        with open(arg, 'r') as DictReader: 
            
            in_data = csv.DictReader(DictReader, 
                                     delimiter=',', 
                                     quotechar =  '"',
                                     skipinitialspace=True,
                                     quoting=csv.QUOTE_ALL,
                                     doublequote = True)
          
            p_actor = ""
           
            for row in in_data:
                print(row) #
                actor = row["actor"]  
                row["command"] = row["command"].strip()
                if row["command"] == "set": 
                     
                    if  row["value"]  == "rnd_movements":
                        b_random_movements  = True 
                    elif  row["value"]  == "videos":
                       self.__send_cmd("remote_cmd" , "video_mode" + "@" + "ANYONE" )   

                elif row["command"] == "speak": 
               
                    if b_random_movements:
                       self.__send_cmd("remote_cmd" , "move:random" + "@" + actor )   

                    self.__send_cmd("remote_cmd" , "speak:" + row["value"] + "@" + actor)  
                          
                    self.__wait_for("spoke")

                elif row["command"] == "speak-no-wait": 
                     self.__send_cmd("remote_cmd" , "speak:" + row["value"] + "@" + actor)   
                     
                elif row["command"] == "sleep":  
                      time.sleep(float(row["value"])) 

                elif row["command"] == "move":  
                      self.__send_cmd("remote_cmd" , "move:" + row["value"] + "@" + actor )   
        return "" 
                      

    def do_say(self, arg):
        'Say: say "hi"@squirrel' 
        return self.do_speak(arg)
    
    def do_speak(self, arg):
        'Speak: speak "hi"@squirrel' 
        cmd = {"cmd":"speak:" , "text" :arg.lower() }   
        if arg.find("@") == -1:
            arg += "@all"
        self.__send_cmd("remote_cmd",  "speak:" + arg)   
        print("remote_cmd",  "speak:" + arg)
        return "Sent" 
    
    def do_dinner(self, arg):
        'Speak: speak "hi"@squirrel'  
        arg = "Dinner!"
        if arg.find("@") == -1:
            arg += "@all"
        self.__send_cmd("remote_cmd",  "speak:" + arg)   
        time.sleep(1)
        self.__send_cmd("remote_cmd",  "speak:" + arg)   
        time.sleep(1)
        self.__send_cmd("remote_cmd",  "speak:" + arg)   
        time.sleep(1)
        self.__send_cmd("remote_cmd",  "speak:" + arg)   
        time.sleep(1)
        self.__send_cmd("remote_cmd",  "speak:" + arg)   
        time.sleep(1)
        return "Sent" 
    
    def do_shutdown(self, arg):
        'Stop   and exit:  BYE'
        print('')
        self.__send_cmd("remote_cmd", "action:" +  "shutdown")  
        return "Bye"
    
    def do_bye(self, arg):
        'Stop   and exit:  BYE'
        print('')
        self.__send_cmd("remote_cmd", "action:" +  "bye") 
       # self.close() 
        return "Bye" 
  

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__': 
     """
     
     """
     cmds = RobotFreedomCmds("user", "remote") 


    