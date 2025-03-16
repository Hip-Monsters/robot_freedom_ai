# -*- coding: utf-8 -*-
"""
Description: This script spawns sensors daemons and monitors the cpu usage.
Author: HipMonsters.com
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024   
pip install pystray
"""    
import os
import json
import subprocess, signal
import os
import psutil, subprocess, sys
import sys 
import time 
import argparse
from subprocess import call 
from subprocess import check_output
#https://stackoverflow.com/questions/6389580/quick-and-easy-trayicon-with-python
 
import subprocess, os
import threading 
import signal
import config

from assets.logo           import logo 
from communication import network 
from communication.updater import Updater 
from communication.nerves import Nerves 
from communication.network import get_local_ip
  

def get_pid(name):
    return check_output(["pidof",name])

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--robot" , type=str,  default='', required=False)  
parser.add_argument("-n", "--networked" , type=int,  default=1, required=False)  
parser.add_argument("-p", "--protocol"  , type=str,  default='monitor', required=False)  
parser.add_argument("-m", "--mode"      , type=str,  default='watch', required=False)  
#image = Image.open("./assets/logo_small.png")  

class Launcher(object):
    """
    """

    def __init__(self , robot ="" , 
                        protocol ="monitor" , 
                        networked=True):
        """
        
        """ 
        self.config     =  config   
        self.net_config =  config.NET_CONFIG   
        self.procs      = {}
        self.commands   = {} 
        self.servers    = []
        self.applications = []
        self.daemons    = []
        self.pids       = {}
        self.epoch      = 1
        self.settings   = {}
        self.updater    = None   
        self.protocol   = protocol
        self.networked  = networked
        self.local_ip   = get_local_ip()
        self.wdir = os.path.dirname(os.path.abspath(__file__))   

        self.agent_is_daemon = False
      
        robot = robot.strip()
        if robot != "":
            self.robot = robot 
        else:
            self.robot = self.config.CONFIG["robot"]   

        self.nerves = Nerves(self.robot)
        
        with open(self.config.DATA_PATH + self.robot + "/settings.json") as f:
           data = ''
           for row in f:
              data += row  
           self.settings = json.loads(data) 
          
        self.b_hub   = False
        self.b_admin = False 

        if self.settings["admin"] == 1:
            self.b_admin = True 

        if self.settings["hub"] == 1:
            self.b_hub = True  
            
        self.servers.append("memcached") 

        # TODO determine what to start (Should be defined in Yaml)

        if self.b_hub and self.b_admin:   
            self.applications.append("server") 
            ## do a quick pasue
            self.applications.append("console") 
            #self.applications.append("http_server")  

        elif self.b_hub:     
            self.applications.append("server") 
            #self.applications.append("console")  

        elif  self.b_admin:      
            self.applications.append("console") 

        else: 
            if self.agent_is_daemon == True: 
               self.daemons.append("agent") 
               if self.config.CONFIG["low_memory_mode"] == 1: 
                    self.daemons.append("main_display_lite") 
               else:
                    self.daemons.append("main_display") 
            else: 
               self.applications.append("agent")  
               if self.config.CONFIG["low_memory_mode"] == 1: 
                    self.applications.append("main_display_lite") 
               else:
                    self.applications.append("main_display") 
            
            if self.config.CONFIG["low_memory_mode"] == 1: 
                self.daemons = ["sense.movement", 
                                "sense.distance", 
                                "chirp",
                                "sound"  ]  
            else: 
                self.daemons = ["voice" , 
                                "chat",
                                "sense.speech_sound",
                                "sense.movement",
                                "sense.distance" , 
                                "sense.touch" ]  

        self.set_cmds()

    def config_network(self  ):
        """
        """

        while self.local_ip == "127.0.0.1":
            self.local_ip   = get_local_ip()
            print("Attempting to connect...")
            time.sleep(30)

        while 1:
            status =   self.test_network_config()
            print(status[0])
        
            if status[0]:
                break
            else:
                print("Network not connected...")
                self.map_network()
                time.sleep(10)  

        self.ip_hub       ,  name_hub  = list(self.net_config["hubs"].items())[0]
        self.ip_repository, bname_resp = list(self.net_config["repositories"].items())[0]
         
        self.updater = Updater(self.ip_repository)
        self.set_cmds()
        
   

    def set_cmds(self  ):
        """
        """
        self.commands["memcached"]         = {"cmd" : ["nohup memcached -l localhost  > ../data/logs/memcached.out"], "subp":-1}
        self.commands["server"]            = {"cmd" : ["python3", "ws_server.py"     ], "subp":-1, "delay": 1}
        self.commands["console"]           = {"cmd" : ["python3", "console.py", "-n " + str(self.networked)   ], "subp":-1}
        self.commands["http_server"]       = {"cmd" : ["python3", "http_server.py"], "subp":-1}

        self.commands["agent"]             = {"cmd" : ["python3", "agent.py"   , "-p " + self.protocol, "-r " + self.robot ,"-n " + str(self.networked) ], "subp":-1}
         
        self.commands["chat"]              = {"cmd" : ["python3", "daemon.py", "-m ai.response", "-c Response", "-r " + self.robot], "subp":-1} 
       
        self.commands["voice"]             = {"cmd" : ["python3", "daemon.py", "-m vocalization.voice", "-c Voice" ,"-r " + self.robot ], "subp":-1} 
        self.commands["sound"]             = {"cmd" : ["python3", "daemon.py", "-m vocalization.sound", "-c Sound" ,"-r " + self.robot ], "subp":-1} 
        self.commands["main_display"]      = {"cmd" : ["python3", "daemon.py", "-m visualization.main_display", "-c MainDisplay" ,"-r " + self.robot ], "subp":-1} 
        self.commands["main_display_lite"] = {"cmd" : ["python3", "daemon.py", "-m visualization.main_display_lite", "-c MainDisplayLite","-r " + self.robot ], "subp":-1}  
        self.commands["sense.speech_sound"]      = {"cmd" : ["python3", "daemon.py", "-m senses.speech_sound", "-c SpeechSound","-r " + self.robot ], "subp":-1} 
        self.commands["sense.movement"]          = {"cmd" : ["python3", "daemon.py", "-m senses.movement", "-c Movement","-r " + self.robot ], "subp":-1} 
        self.commands["sense.touch"]             = {"cmd" : ["python3", "daemon.py", "-m senses.touch", "-c Touch","-r " + self.robot ], "subp":-1}  
        self.commands["sense.distance"]          = {"cmd" : ["python3", "daemon.py", "-m senses.distance", "-c Distance","-r " + self.robot ], "subp":-1}  
        self.commands["sense.sound"]             = {"cmd" : ["python3", "daemon.py", "-m senses.sound", "-c Sound","-r " + self.robot ], "subp":-1} 
        self.commands["sense.speech"]            = {"cmd" : ["python3", "daemon.py", "-m senses.speech", "-c Speech","-r " + self.robot ], "subp":-1} 
        self.commands["sense.tempature_humidity"]= {"cmd" : ["python3", "daemon.py", "-m senses.tempature_humidity", "-c TempatureHumidity" ,"-r " + self.robot  ], "subp":-1} 
        self.commands["sense.light"]             = {"cmd" : ["python3", "daemon.py", "-m senses.light","-c Light" ,"-r " + self.robot ], "subp":-1}
        self.my_env = os.environ.copy() 
        self.my_env["PATH"] = f"/usr/sbin:/sbin:{self.my_env['PATH']}:" + self.wdir   
         

    def test_network_config(self, kill_old=True):
        """
        
        """ 
  
        ip_hub       ,  name_hub  = list(self.net_config["hubs"].items())[0]

        ip_repository, bname_resp = list(self.net_config["repositories"].items())[0]

        if self.b_hub:
            hub_ok = True
        else:
            hub_ok  = network.check_ips_role(ip_hub, "hub")
 
        if self.b_admin:
            repository_ok = True
        else:
            repository_ok = network.check_ips_role(ip_repository, "repository")
        

        print("Hub       ", ip_hub,        hub_ok) 
        print("Repository", ip_repository, repository_ok) 

        return [hub_ok, repository_ok]


    def display_network(self,icon, query):
        """
        
        """
        status = network.map_rf_ips()
        print(json.dumps(status, indent=4))

    def map_network(self ):
        """
        
        """
        network_directory = network.map_rf_ips() 
     
        b_updated = False
        if len(network_directory["repositories"]) > 0:
            self.net_config["repositories"] =  network_directory["repositories"]
            b_updated = True

        if len(network_directory["hubs"]) > 0:
            self.net_config["hubs"] =  network_directory["hubs"]
            b_updated = True

        if len(network_directory["robots"]) > 0:
            self.net_config["robots"] =  network_directory["robots"]

        if  b_updated:
            config_file = open(config.CONFIG_PATH + "net_config.json", "w") 
            config_file.write(json.dumps(self.net_config ,indent=4))
    
    def log_pids(self, key, pid, proc_class):
        """
        
        """

        if proc_class == "app":
            f_name = "pids.apps.csv"
        else:
            f_name = "pids.daemons.csv" 

    def kill_all(self, icon, query):
        """
        for icon
        """
        self.kill_procs("daemon")
        self.kill_procs("app")
        fin = self.cleanup() 
        return fin

    def restart(self, protocol = "monitor"):
        """
        for icon
        
        """
        if self.protocol != protocol:
            self.protocol = protocol
            self.set_cmds()

        self.start_applications(protocol)
        self.start_daemons(protocol)


    def cleanup(self):
        """
        """
        procs = []
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate() 
        out = str(out)
        #defaults write com.apple.CrashReporter DialogType none
        #https://stackoverflow.com/questions/20226802/disable-the-last-time-you-opened-it-unexpectedly-quit-while-reopening-window
        for line in out.split("\\n"): 

          for cmd in ["agent.py", "daemon.py"]: 
             if line.find(cmd) > -1:
                 row = line.split(' ') 
                 try:
                    pid = int(str(row[0]))
                 except:
                     print(row)
                     pid =-1
                 if pid != -1:
                     proc = psutil.Process(pid) 
                     proc.kill() 
                     procs.append("killed " + cmd) 
                     continue

        return procs 
    
    def kill_procs(self, proc_class):
        """
        
        """

        f_name = "pids." + proc_class + ".csv" 
        if os.path.isfile(config.LOGS_PATH + f_name) is False:
           return True
        
        with open(config.LOGS_PATH + f_name) as f:
            for line in f: 
                row = line.strip().split(',')  
                try:  
                   os.kill(int(row[1]), signal.SIGTERM)
                   print("killed " + str(row[0]))
                except:
                    print("No longer exists.")
        return True


    def start_daemons(self, kill_old=True):
        """
        
        """
        proc_class = "daemon"

        if kill_old:
            self.kill_procs(proc_class)  

        out = open(config.LOGS_PATH + "pids." +  proc_class  + ".csv", "w")  
        
        for key in self.daemons:
                cmds =  self.commands[key]
                print("Starting " + key, end="")  
                outfile = open(config.LOGS_PATH + key + ".daemon.log" , "w")  
                subp = subprocess.Popen(" ".join(["cd",self.wdir ,";"]+ cmds["cmd"]), 
                                        stdout=outfile ,
                                        cwd= self.wdir  ,
                                        shell=True,
                                        env=self.my_env)
                
                out.write(key + "," + str(subp.pid) + "\n")
                cmds["subp"]  =  subp
                print("\r" +  "Started " + key)
                
        
        out.close()

    def start_applications(self, 
                           protocol="monitor",  
                           kill_old=True):
        """
        
        """    
        proc_class = "app"

        if kill_old:
            self.kill_procs(proc_class)  
            
        out = open(config.LOGS_PATH + "pids." +  proc_class  + ".csv", "w")  
         
        for key in self.applications:
            cmds = self.commands[key]
            print("Starting " + key, end="") 
            cmd = ' '.join(["cd", self.wdir +";"]+ cmds["cmd"] + [""]) 

            if config.OS == 'OSX': 
                cmd = "source ~/venv_rf/bin/activate; " + cmd
                scmd = 'tell app "Terminal" to do script "%s;"' % cmd 
                call( ["osascript" , "-e", scmd], 
                     env=self.my_env )   

            elif config.OS == 'LINUX':
                scmd = '"%s;"' % cmd 
               # call( ["lxterminal" , "-e", scmd] )  
                os.system("lxterminal -e " + scmd)  

            else:
                scmd = '"%s;"' % cmd
                subp = subprocess.Popen(["command" , "-e", scmd])
                cmds["subp"]  =  subp

           # out.write(key + "," + str(subp.pid) + "\n")  
            out.write(key + "," + "" + "\n")  
            print("\r" +  "Started " + key)  

    def display_status(self,icon, query):
        """
        
        """
        status = self.get_status() 
        print("\n".join(status))
 

    def get_all_procs(self):
        """
        """

        procs = []
        for pro in psutil.process_iter(): 
          if pro.name().find('python') > -1:
           proc = psutil.Process(pro.pid)
           cmds = proc.cmdline()
           if len(cmds) > 1:
               cpu_prec = proc.cpu_percent() 
               procs.append(cmds[1] + " cpu " +  str(cpu_prec) ) 
        return procs 

    def get_status(self ):
        """
        
        """

        log = []
        ## should move to csv so can restart
        for procs in [self.applications, self.daemons]:
            for key  in self.daemons:
             
              cmds = self.commands[key]
              try:
                subp = cmds["subp"]
                if subp == -1:
                    continue 
                proc = psutil.Process(subp.pid)
                mem      = proc.memory_info() 
                cpu_prec = proc.cpu_percent()  
                try:
                    mem_prec = mem.rss / mem.vms
                except:
                    mem_prec = 0.0
                    
                log.append(str(key) + "  " + str(round(mem_prec,4) ) + "  |  "  )
        
              except:
                log.append(str(key) + " Error " + str(round(0.0,4)) + "  |  " )
     
        return log
          
    def server_forever(self ):
        """
        
        """

        print(logo())  
        print("Robot's IP Address  :"    + self.local_ip) 
        print("Sensors             :"    +  " ".join(["voice","noise", "movement","distance","balence"]) ) 
        print("Components          :"    +  " ".join(["speech","device_contol","communication","mic", "camera"])  ) 
        print("AI Modules          :"    +  " ".join(["chat", "cognitive_control", "emotions", "motivations", "personality", "dream_inducer", "strategies" ])  ) 
        print("AI Learner          :"    +  " ".join(["gradient_descent", "BERT", "cosine_similarity","ANN" ]) ) 
        print("Security Modules    :"    +  " ".join(["firewall", "security", "cmd_filters", "threat_scores"]) ) 
        print("AI Ethics Modules   :"    +  " ".join(["asimovs_3_laws", "strategy_inhibitor", "stimuli_mitigation"]) )
        print("Welcome " + self.robot   )

        from communication.http_server import HTTPServer

        try:
              IPAddr = get_local_ip()
              print(IPAddr)
              srv = HTTPServer(self, self.networked)
              srv.server_forever()
          
        except KeyboardInterrupt:
              print("Users killed launcher. Cleaning up...")
              for key , cmds in self.daemons.items():
                  subp = cmds["subp"] 
                  if subp == -1:
                      continue  
                  proc = psutil.Process(subp.pid) 
                  proc.kill()
              sys.exit() 

    def tray_exit(self,icon, query):
        """
        """
        self.icon.stop()

    def set_up_icon(self):
        """
        
        """ 
        self.icon = pystray.Icon("RobotFreedom", image, "RobotFreedom", 
                                 menu=pystray.Menu(
                    pystray.MenuItem("Status"  , self.display_status),
                    pystray.MenuItem("Network" , self.display_network),
                    pystray.MenuItem("Restart" , self.restart),
                    pystray.MenuItem("Kill All", self.kill_all),
                    pystray.MenuItem("Exit"    , self.tray_exit)))

if __name__ == "__main__":

    """
    python3 launcher.py  -monitor
  
    """
    args      = parser.parse_args()  
    robot     = args.robot 
    networked = args.networked 
    mode      = args.mode 
    protocol  = args.protocol 

    launcher = Launcher(robot=robot, 
                        protocol = protocol,
                        networked=networked)
    if networked == 1 :
        launcher.config_network()
    launcher.cleanup()
    launcher.start_applications()
    launcher.start_daemons() 
    #launcher.set_up_icon()
   # threading.Thread(target=launcher.icon, )
    #launcher.icon.run_detached()
    launcher.server_forever() 