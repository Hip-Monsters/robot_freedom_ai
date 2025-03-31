#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: HipMonsters.com  
License: MIT License  
""" 
import time
from . handler import Handler, handle_exceptions


class MobilityHandler(Handler): 
    """
    
    """

    @handle_exceptions 
    def send_command(self, cmd, robot): 
       """
      
       """ 
        
       if self.sequence_format:
          dcmd  = ""
          _cmds = "" 
          if cmd  == "random":  
              _cmds,   current_states = self.agent.sequences({'part':"random"}, 
                                                            self.agent.current_states) 
              cmds = _cmds[:2]

          elif type(cmd ) == list:
              _cmds,   current_states = self.agent.sequences({'part':"random"},
                                                             self.agent.current_states) 
              cmds = _cmds[:2]

          else:
              cmds = ""

              if type(cmd) == str:
                  cmds = cmd.split(',')
              else:
                  cmds = cmd

              if len(cmds) == 1:
                 cmds = [cmd] 

              elif len(cmds) != 3:
                 cmds = [cmds[0]]  
              else: 
                 dcmd = {"action": cmds[0].strip(),
                         "side":   cmds[1].strip(),
                         "part":   cmds[2].strip()} 
                 
                 cmds,  current_states = self.agent.sequences(dcmd, 
                                                              self.agent.current_states)  

          if len(cmds) == 0:
              print("Improper device command:" + str(cmd), _cmds, dcmd)   

          else:
              """  
              self.nerves.set("movement" , json.dumps(cmds) )
              """
              #print("send_command", cmds)
              for cmd in  cmds:
                  cmd = cmd.strip()
                  if cmd.startswith('p'): 
                     try:
                         i_len = float(cmd.replace('p','')) 
                     except:
                         i_len = .1
                   #  time.sleep(i_len)
                  else:
                     answer = self.agent.mobility.write(cmd, robot)
                     self.agent.current_states[cmd]        = True
                     self.agent.current_states[self.agent.FLIPS[cmd]] = False
                     time.sleep(.01)
              
       else: 
           answer = self.mobility.write(cmd, robot)  