# -*- coding: utf-8 -*-
  
"""
Description: This script spawns sensors daemons and monitors the cpu usage.
Author: HipMonsters.com
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024
Version: 1.3
Plaftorm: RaspberryPi
License: MIT License
"""

import psutil, subprocess, sys

import  time 
#from getpass import unix_getpass

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
 
procs      = {}
processes =  {} 
processes["chat"]     = {"cmd" : ["python3", "chat.py"          , "-m serve","-r example_robot"], "subp":-1}
processes["voice"]    = {"cmd" : ["python3", "voice.py"         , "-m serve","-r example_robot"], "subp":-1}
processes["sound"]    = {"cmd" : ["python3", "sense_sound.py"   , "-m serve","-r example_robot","-a '{\"prompts\":[\"hello\"]}'"], "subp":-1}
processes["speech"]   = {"cmd" : ["python3", "sense_speech.py"  , "-m serve","-r example_robot","-a '{\"prompts\":[\"hello\"]}'"], "subp":-1}
processes["movement"] = {"cmd" : ["python3", "sense_movement.py", "-m serve","-r example_robot","-a '{\"max\":70}'"], "subp":-1}
processes["distance"] = {"cmd" : ["python3", "sense_distance.py", "-m serve","-r example_robot","-a '{\"max\":30}'"], "subp":-1}
processes["touch"]    = {"cmd" : ["python3", "sense_touch.py"   , "-m serve","-r example_robot","-a '{\"max\":30}'"], "subp":-1}
processes["visuals"]  = {"cmd" : ["python3", "visualizations.py", "-m serve","-r example_robot"], "subp":-1}
 
pids = {} 

def start_daemons(kill_old=True):

    with open("pids.csv") as f:
        for line in f: 
            row = line.strip().split(',')
            
            try: 
               proc = psutil.Process(int(row[1]))
               proc.kill()
               print("killed " + str(row[0]))
            except:
                print("No longer exists.")
            
    
    out = open('pids.csv', "w")  
    for key , cmds in processes.items():
        print("Starting " + key) 
        cmd = ' '.join(cmds["cmd"])
        subp = subprocess.Popen(cmd ,   
                                shell=True)
        out.write(key + "," + str(subp.pid) + "\n")
        cmds["subp"]  =  subp
        print("Started " + key)
    
    out.close()

def shell():

    try:
       while True:
           print("")
           for key , cmds in processes.items():
               subp = cmds["subp"]
               proc = psutil.Process(subp.pid)
               mem  =  proc.memory_info() 
               cpu_prec = proc.cpu_percent()  
               try:
                   mem_prec = mem.rss / mem.vms
               except:
                   mem_prec = 0.0
                   
               print(str(key) + "  " + str(round(mem_prec,4)))

           time.sleep(10)
       
    except KeyboardInterrupt:
           for key , cmds in processes.items():
               subp = cmds["subp"]
               proc = psutil.Process(subp.pid) 
               proc.kill()
           sys.exit()
    

if __name__ == "__main__":
    """
    python3 daemon_wrangler.py -m monitor  
  
    """
    args =  parser.parse_args()  

    mode    = args.mode 
    start_daemons()

    if mode == "monitor":
        shell()