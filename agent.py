# -*- coding: utf-8 -*-
  
"""
Description: The agent daemon that allows the Artifical Intelligence to process sensors signals and control the robot.
Author: HipMonsters.com  
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024
Version: 4.0
Plaftorm: RaspberryPi
License: MIT License 
"""

import sys 
import platform
import csv
import datetime  
import threading 
import time 

####    Libraries   ################
from memory         import Memory
from nerves         import Nerves 
from client         import Communication
from controller     import Controller 
from camera         import Camera
from sound          import Sound 
from sequences      import sequences  
from security       import Security
from logo           import logo
 
from ai.behavior             import Behavior
from ai.basic_interactions   import Interactions
from ai.basic_knowledge      import Knowledge
from ai.ethics               import Ethics

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot")  
parser.add_argument("-f", "--file"         , default="NA")  
parser.add_argument("-c", "--command_style", default="sequence")  
parser.add_argument("-v", "--verbose"      , default=False)  
 
 
stop_threads = False 


def poll_trigger(obj, kargs  ):   
    """
    
    """
 
    print("\rThread obj " + str(obj) + " polling...                      "  , end=""  )   
    if  v:
        return True
    else:    
        return False
     
        
def wait_for_event(fnct , event, obj, history , kargs):
    """
    """
    global   stop_threads  
    i = 0
    while True:
        print("\rThread " + str(fnct) + " running..." + str(i) + "         " , end="" )
        i += 1
        time.sleep(1)
        kargs["polls"] = i
        if stop_threads is True or  fnct(obj, kargs):
             print("\rEvent occured for " + str(fnct)  + "                ", end=""  )  
             stop_threads  = True 
             event.set()
             return  True
 
    
class AIAgent(object):
    
    def __init__(self, name, mode , verbose = True, sequence_format =True ):
        """ 

        """

        self.os  = "LINUX"
        if platform.system() == 'Windows':
           self.os = "WIN"
        elif platform.system() == 'Darwin': 
           self.os = "OSX"


         
        self._space  = " ".join(['' for v in range(40)])

        print("Waking up HipMonsters Robot" + self._space, end=""  )

        
        ## Connect to the Ardinuo 
        if self.os == "OSX": 
            self.robot_ports = ('/dev/cu.usbmodem14201',"113") 
        else:
            self.robot_ports = ("/dev/ttyACM0", "1")
        self.robots = None
          

        print("\Initalializing up basic settings...."  + self._space , end="" )
        self.verbose          = verbose 
        self.mode             = mode 
        self.name             = name 
        self.polling_rate     = .5 
        self.sequence_format  = sequence_format 

        self.security         = Security(self.name)

        print("\Initalializing internal clocks...."  + self._space , end="" )
        self.epoch            = 0
        self.last_stimui      = datetime.datetime.now()
        self.current_cycle    = datetime.datetime.now() 
        self.last_update      = datetime.datetime.now() 
        self.last_response    = datetime.datetime.now() 


        print("\rInstallizing components...."  + self._space , end="" )

        print("\r Communication ..."  + self._space , end="")
        self.communication = Communication(name)
        self.communication.connect()
        self.communication.send("WORLD", "AWAKE")
        print("\r Communication  Complete."  + self._space , end=""  )

        print("\r Connecting with Memory ..."  + self._space , end="")
        self.memory     = Memory(self.name)
        self.nerves     = Nerves(self.name)
    
        print("\r Initializing Controler ...."  + self._space , end="")
        self.controller     =  Controller(name)   
  
 
        print("\r Initializing Camera..  "  + self._space , end="" ) 
        self.camera         =  Camera(name)
        self.sound          =  Sound(name)

        print("\r Spawning Vocalization...."  + self._space , end="")
       # status = os.system('systemctl is-active --quiet voice')
       # print(status)
 

        self.nerves.set("speak" ,"")
        # self.voice          =  Voice(name, ROBOTS)  

        if  self.mode in ('interact', "monitor"):

            print("\r Spawning sensors...."  + self._space , end="" )
            time.sleep(.1)
            print("\r        voice..."  + self._space , end="" ) 
            time.sleep(.1)  
            print("\r        sound..."  + self._space, end=""  )  
            time.sleep(.1) 
            print("\r        distance..."  + self._space , end="" )  
            time.sleep(.1) 
            print("\r        tempature..."  + self._space , end="" )   
            time.sleep(.1)
            print("\r        touch..."  + self._space , end="" )   
            time.sleep(.1)
            print("\r        humidity..."  + self._space , end="" )   
            time.sleep(.1)
            print("\r        motion..."   + self._space , end="" )   
            time.sleep(.1)
            print("\r        balence..."  + self._space , end="" )  
            time.sleep(.1)
        

        self.device_connections = {}  
   
        print("\rConnecting devices.  " + self._space, end="")
        self.connect_devices()
        

        print("\rLoading AI Knowledge               " + self._space, end="")
        self.knowledge                = Knowledge(self.name)
        self.short_term_history       = {} 


        print("\rLoading AI Behavior                " + self._space, end="")
        self.behavior    = Behavior(self.name  , 
                                    self.short_term_history  , 
                                    self.knowledge  ) 
 
        #self.behavior.reflection()


        print("\rLoading AI Interactions          " + self._space, end="")
        self.interactions             = Interactions(self.name, self.knowledge)

        self.ethics                   = Ethics(self.name)

        print("\rRobot and AI setup is complete." + self._space + self._space, end="")  
        print(logo())
        print("Communicating IP    :"    + self.communication.ip  +  self._space )  
        print("Sensors             :"    +  " ".join(["voice","noise", "movement","distance","balence"])+  self._space ) 
        print("Components          :"    +  " ".join(["speech","device_contol","communication","mic", "camera"]) +  self._space) 
        print("AI Modules          :"    +  " ".join(["chat", "knowledge", "emotions", "motivations", "personality", "dream_inducer", "strategies" ]) +  self._space) 
        print("AI Learner          :"    +  " ".join(["gradient_descent", "BERT", "cosine_similarity","ANN" ]) +  self._space) 
        print("Security Modules    :"    +  " ".join(["firewall", "security", "cmd_filters", "threat_scores"]) +  self._space) 
        print("AI Ethics Modules   :"    +  " ".join(["asimovs_3_laws", "strategy_inhibitor", "stimuli_mitigation"])  + self._space)
        print("Welcome " + name  + self._space   )

    def connect_devices(self):
        """
        
        """ 
        if self.robots is None:
             self.device_connections = {}
             self.device_connections[self.name] =  self.robot_ports
        else:
             self.device_connections = self.robots 

        self.controller.connect_to_robots(self.device_connections)   


    def send_command(self, cmd, robot): 
       """
      
       """ 
        
       if self.sequence_format:
          
          if type(cmd) == str:
              a_cmd = cmd.split(' ')
          else:
              a_cmd = cmd
          dcmd = {"part": a_cmd[0], "action": a_cmd[1], "side": a_cmd[2]}
          
          cmds = sequences(dcmd)   
          for cmd in  cmds:
              if cmd.startswith('p'): 
                 i_len = int(cmd.replace('p',''))
                 time.sleep(i_len)  
              else:
                 self.controller.write(cmd, robot)
       else: 
           self.controller.write(cmd, robot)   

    def get_chat_response(self, prompt):

        self.nerves.set("chat" ,"respond>" + prompt)
 
        i_cnt = 0
        while True:
            detect, val = self.nerves.pop("chat_responses")  
            i_cnt +=1
            if detect or i_cnt > 10:
                return val
            time.sleep(self.polling_rate)


    def speak(self,message):
        """
        
        """
        self.nerves.set("speak" ,";".join(["speak", "wait", message]))

    def speak_and_wait(self,message):
        """
        
        """
        self.speak(message) 
        time.sleep(4)
        i_cnt = 0
        while True:
            detect, val = self.nerves.stopped("speak")  
            i_cnt +=1
            if detect or i_cnt > 10:
                break
            time.sleep(self.polling_rate)

    def remember(self, event,  value):
        """
        """ 
        if  event not in  self.short_term_history :
            self.short_term_history[event]  = []

        self.short_term_history[event] = [datetime.datetime.now(),  value]

    def wait_fo_signal(self, signal):

       while True:
           val =  self.nerves[signal]
           if val is not False:
                   break

    def run_script(self, script, b_multi_actors = False):
        """ 
    
        """

        with open(script, 'r') as DictReader:

            in_data = csv.DictReader(DictReader, delimiter=',', quotechar='"')
            p_actor = ""
            for row in in_data:

                if self.verbose:
                     print(row)

                if self.name == row["actor"] and b_multi_actors is False:
                          

                  if row["command"] == "speak": 
                      
                      if b_multi_actors:
                          if row["actor"] != p_actor: 
                             self.nerves.put["speak"] = ";".join( ["switch_voice", "wait_for" , row["actor"]])
                          
                      self.speak(row["value"])
                     
                  elif row["command"] == "sleep":
                      time.sleep(float(row["value"]))

                  elif row["command"] == "move": 
                      self.send_command(row["value"] ,row["actor"])  
                      
                  elif row["command"] == "communicate": 
                       self.communication.send(row["value"]  ,row["param1"] )

                  elif row["command"] == "wait_for_signal":   
                       signal_val =  self.wait_fo_signal[row["value"]] 
                       self.remember(row["value"], signal_val)

                  elif row["command"] == "wait_for_event":
                       
                       while True:
                          detect, val = self.nerves.pop(row["value"]) 
                          if detect:
                              break
                          time.sleep(self.polling_rate)


                  elif row["command"] == "wait_for_a_message": 
                    
                      recipient      = "WORLD" 
                      expected_reply = "DONE"
                      sent_from      = row["value"]
                     
                      while True:
                          detect, val = self.communication.wait_for_a_message(recipient,  expected_reply , sent_from) 
                          if detect:
                              break
                          time.sleep(self.polling_rate)

                  elif row["command"] == "wait_for_event_thread": 
                      ## just testing
                      event = threading.Event()
                      params = {"recipient":"WORLD" , "expected_reply":"DONE", "from":"number_3"}
                      t4 = threading.Thread(target = self.communication.wait_for_a_message, args =( poll_trigger, event , params))
                      t4.start() 
                      event.wait()

    def  run_remote_cmd(self, input):
        """
        
        """
        self.speak_and_wait("Recieved a command....")
     
        print("\r" + input , end="")
         
        commands = {}
        #try: 
        if 1 ==1:
            a_input = input.split(":")
            if len(a_input) == 1:
               self.speak_and_wait("Improper command " + input)
               return False
             
            commands["cmd"]  = a_input[1]
            if len(a_input) > 2:
               commands["params"] = a_input[2]
      
            if commands["cmd"] == "speak":
                self.speak_and_wait(commands["params"])

            elif commands["cmd"] == "chat":  
                self.behavior.stimui_time = datetime.datetime.now()
                response  = self.interactions.responses("sense",
                                                        "voice", 
                                                        commands["params"], 
                                                        self.behavior,
                                                        True, 
                                                        self.get_chat_response) 
                self.speak_and_wait(response["speach"][0])
    
            elif commands["cmd"] == "shutdown":
                self.speak_and_wait("Gobing to sleep.")
                sys.exit()
    
            elif commands["cmd"] == "bye":
                self.speak_and_wait("bye bye!")
      
            elif commands["cmd"] == "inspire":
                self.speak_and_wait("You are great!")
    
            elif commands["cmd"].startswith("roll"): 
                response = self.interactions.command_responses("roll " + commands["params"])
                self.speak_and_wait( response["speach"][0]) 

            else :
               self.speak_and_wait("Unknown command " + input)
               return False
            
     #   except:
      #      self.speak_and_wait("I did not understand what you meant by " + input)
        return True 
    
    def monitor(self):
        """ 

        """ 

        i_quiet = 0
        while True:  
            # sleep to set cycle 
            time.sleep(.25)

            ### Update clocks
            self.epoch          += 1
            self.current_cycle  =  datetime.datetime.now()

            have_message, message = self.communication.check_messages()
            print("\r" + "messages".ljust(25, ' ') + " " + str(have_message) + self._space , end=""  )   
        
            if have_message: 
                if message.find("remote_cmd") > -1: 
                    commands = message 
                    self.run_remote_cmd(commands)
                else: 
                    self.speak("I have mail!") 
                    self.speak(message)  

            detect, commands = self.nerves.pop("remote_cmd") 
            if detect:
                self.run_remote_cmd(commands) 
                
            for sense in self.behavior.emotions.emotion_factors["sense"].keys():
                
                if sense == "quiet": 
                    detect, amplitude = False, "nothing"
                    dur = self.current_cycle - self.last_stimui
                    if dur.total_seconds() > 60:
                        detect,  amplitude = True, .10* dur.total_seconds() 
                        i_quiet += 1
                    else:
                        i_quiet = 0
                else:
                    detect, amplitude = self.nerves.pop(sense)  

                ## delay to make sure
                dur = self.last_response - self.last_stimui
                if dur.total_seconds() < 1:
                     time.sleep(.5)
 
                print("\r" + sense.ljust(25, ' ') + " " + str(detect) + "  " +  str(amplitude)  + self._space , end="")
                
                if detect:  
                 
                    if amplitude == "timeout":
                         continue
                    
                    interval = (self.current_cycle - self.last_stimui).total_seconds()  
                    self.last_stimui  =  self.current_cycle
                    
                    if sense != "cmd": 

                        if i_quiet >= 3: 
                            print("\r" + "Initating Sleep Cycle..."  +     self._space , end=""  ) 
                            print("\r" + "Dreaming....            "  +     self._space , end=""  )  
                            self.behavior.reflection()
                            print("\r" + "Starting Wakeup Sequence..."  +     self._space , end=""  )  

                        self.behavior.stimuli("sense", sense, 1, self.epoch, 
                                              self.last_stimui, interval) 

                        self.nerves.set("stimuli", sense + ":" + self.behavior.emotions.mood() )  

                        chat = False
                        if sense == "speach":
                            chat = True

                        responses = self.interactions.responses("sense", 
                                                                 sense, 
                                                                 amplitude,  
                                                                 self.behavior ,
                                                                 chat,
                                                                 self.get_chat_response) 
                        for response in responses["speach"]: 
                            self.speak_and_wait(response)  

                        for response in responses["movement"]: 
                            self.send_command(response, self.name )
                     
                        self.last_stimui  =  datetime.datetime.now()
                        self.nerves.set(sense, "")  
                        if sense == "speach": 
                            self.nerves.set("noise", "")   
                    else:
                        print("reflex- like balence sensor on arms")
           
            time.sleep(self.polling_rate) 

if __name__ == "__main__":
    """
    python3 agent.py -m monitor -r example_robot 
  
    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot    

    verbose = True
    if args.verbose is not None:
        if args.verbose == "True":
             verbose = True
        else:
             verbose = False 

    sfile = ""
    if args.file is not None:
        sfile = args.file 

    command_style_sequence = True
    if args.command_style is not None:
        if args.command_style == "device" :
          command_style_sequence =  False 

    agent = AIAgent(robot, 
                  mode,
                  verbose,
                  command_style_sequence) 

    if mode == "monitor":
        agent.monitor()
    else:
        agent.run_script(sfile)
