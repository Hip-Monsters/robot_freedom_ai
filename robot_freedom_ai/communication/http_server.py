#!/usr/bin/python
# -*- coding: utf-8 -*-  
"""
Description: Implements a simple HTTP/1.0 Server  
Author: HipMonsters.com 
License: MIT License
"""  
import time
import datetime 
import shutil
import socket
from urllib.parse import unquote
from html.parser  import HTMLParser
from .client        import Client
from .base_cmds     import BaseCmds
from .nerves        import Nerves 
from .network       import get_local_ip
import json 
import config 

class HTMLFilter(HTMLParser):
    """
    
    """
    text = ""
    def handle_data(self, data):
        """
        
        """
        self.text += data

class HTTPServer(object):

    def __init__(self,parent,  networked=True ):
        """
        
        """

        CONFIG = config.CONFIG  
        self.networked     = networked
        self.launcher      = parent
        self.robot         = self.launcher.robot

        t_ip = list(config.NET_CONFIG["hubs"].keys())[0] 

        if  t_ip != "":
            self.client  = Client(self.robot, t_ip) 
        else:
            self.client  = Client(self.robot, '127.0.0.1') 

        self.responses = ["Hello from  " + self.robot]  
        self.server_host = '0.0.0.0'
        self.server_port = 8000   
        self.color = self.launcher.settings["color"] 
        self.nerves = self.launcher.nerves 

        self.base_cmds  = BaseCmds(self.robot, 
                             config, 
                             self.client, 
                             self.nerves,
                             self.networked  ) 

    def get_processes(self):
       """
       
       """
       return self.launcher.get_status()
    
    
    def kill_processes(self):
       """ 
    
       """
       procs = []
       procs = self.launcher.kill_all(None, None) 
       return procs 

    def start_processes(self, protocol):
       """ 
       """  
       self.launcher.restart(protocol)
       procs = ["started processes"] 
       return procs 


     # http://192.168.1.4:8000/
    def server_forever(self ):
       """
       
       """   

       if self.networked:
           print("Connecting to HUB..."   ) 
           connected = self.client.connect()
           if connected:
               self.client.send("WORLD", "HTTP SERVER ACTIVE")   
      
       print("Listening... on ", 
             self.launcher.local_ip ,
               self.server_port   )    
       while True:     
         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         server_socket.bind((self.server_host, self.server_port))
         
         server_socket.listen(1) 
         hostname = socket.gethostname()   
         client_connection, client_address = server_socket.accept()
      
         request = client_connection.recv(1024).decode() 
      
         arequest = request.split('\n')    
         render = True
         print(arequest, arequest[0])
         try:
             if "POST" in  arequest[0]: 
                 print("arequest", arequest[0]) 
                 aparams = arequest[-1].split("=")   
                 
                 if len(aparams) > 1:
                     aparams = unquote(aparams[1])    
                     
                 if aparams.find('+') > -1:
                     cmd, params = aparams.split('+', 1) 
                 else:
                     cmd, params = aparams, "none"
      
                 cmd = cmd.lower().strip() 
                 resp = ""
                 if cmd == "nerves": 
                    cmds =cmd 
                    for topic, details in json.loads(self.nerves.client.get('log')).items():
                        resp += topic  + " " + str(details[0]  ) + "  " +  str(details[1]) + "\n" 
      
                 elif cmd == "update_settings": 
                     self.launcher.updater.update("settings") 
                     resp +=  "Updating Settings\n" 
      
                 elif cmd == "update_code": 
                     self.launcher.updater.update("code") 
                     resp +=  "Updating Code\n" 
      
                 elif cmd == "status":   
                     cmds = cmd 
                     for log in self.get_processes():
                        resp += log + "\n" 
      
                 elif cmd == "clear-logs":   
      
                    filename = config.LOGS_PATH +  "chat_ollama.log" 
                    now = datetime.datetime.now() 
                    timestamp = str(now.strftime("%Y_%m_%d_%H_%M_%S"))
 
                    dest = filename +timestamp
                    shutil.copy(filename, dest)
                    log =  open(filename, 'w')  
                    log.close()
      
                 elif cmd == "logs":   
                     cmds = cmd  
                     
                     filename =  config.LOGS_PATH +  "chat_ollama.log" 
                     client_connection.send('HTTP/1.1 200 OK\r\n'.encode())
                     client_connection.send("Content-Type: file\r\n".encode())
                     client_connection.send("Accept-Ranges: bytes\r\n\r\n".encode()) 
                     with open(filename, 'rb') as f:
                         # Send the file self.robot
                        # client_connection.send(fileself.robot.encode())
      
                         # Send the file data
                         while True:
                             data = f.read(1024)
                             if not data:
                                 break
                             client_connection.send(data)
                 
                 elif cmd == "start":  
                      cmds =cmd 
                      for log in self.start_processes("default"):
                        resp += log + "\n" 
      
                 elif cmd == "start-listen":  
                      cmds =cmd 
                      for log in self.start_processes("listen"):
                        resp += log + "\n" 
      
                 elif cmd == "start-mouse":  
                      cmds =cmd 
                      for log in self.start_processes("mouse"):
                        resp += log + "\n" 
                 
                 elif cmd == "kill-all": 
                     cmds =cmd  
                     for log in self.kill_processes():
                        resp += log + "\n" 
                 
                 else:
      
                     params = params.replace("+", " ")
                     cmds = cmd + " " + params  
                     for i in range(2):
                         connected = self.client.connect() 
                         if connected:
                             resp = getattr(self.base_cmds, "do_%s" % cmd.lower().strip())(params) 
                             break
                         else: 
                            connected = self.client.connect() 
                            resp ="Network Hub is down."
                            time.sleep(10)
      
      
                 self.responses.insert(0, ">" + cmds)
                 if resp is None:
                     self.responses.insert(0,"Sent")
                 elif resp != "": 
                     self.responses.insert(0,resp) 
      
                 b_new, message = self.client.check_messages()
                 if b_new:
                     self.responses.insert(0,message)
      
             ##http://128.0.0.1:8000/update_data/
             elif "updates" in  arequest[0]: 
                
                 if 'admin' in config.CONFIG:
                     if config.CONFIG['admin'] == 1: 
      
                         file = open(config.UPDATES_PATH + "most_recent.zip", 'rb') 
                         if "settings" in  arequest[0]:  
                             file = open(config.UPDATES_PATH + "most_recent.settings.zip", 'rb')  
                             
                         client_connection.send('HTTP/1.1 200 OK\r\n'.encode())
                         client_connection.send("Content-Type: achive/zip\r\n".encode())
                         client_connection.send("Accept-Ranges: bytes\r\n\r\n".encode()) 
                         client_connection.send(file.read()) 
                         client_connection.close() 
                 
                 render = False
      
             elif "whois" in  arequest[0]: 
                 role = "robot"  
                 if 'admin' in self.launcher.settings:
                     if self.launcher.settings['admin'] == 1: 
                        role = "repository"
      
                 if 'hub' in self.launcher.settings:
                     if self.launcher.settings['hub'] == 1: 
                        role = "hub"  
                        
                 render = False 
                 srobot =  role + ":" + self.launcher.settings['name'] 
                 client_connection.send('HTTP/1.1 200 OK\r\n'.encode()) 
                # client_connection.send("Content-Type: application/x-www-form-urlencoded\r\n".encode())
                 client_connection.send("Accept-Ranges: bytes\r\n\r\n".encode())
                 client_connection.send(srobot.encode())  
                 client_connection.close() 
                 
      
             elif "assets" in  arequest[0]: 
                 file = open("./assets/logo_small.png", 'rb') 
                 client_connection.send('HTTP/1.1 200 OK\r\n'.encode())
                 client_connection.send("Content-Type: image/png\r\n".encode())
                 client_connection.send("Accept-Ranges: bytes\r\n\r\n".encode()) 
                 client_connection.send(file.read()) 
                 client_connection.close() 
                 render = False
         
         except Exception as e:
              print(request) 
              print(e) 
              xv
              self.responses.insert(0,str(e))
      
       #  https://stackoverflow.self.client/questions/49084143/opencv-live-stream-video-over-socket-in-python-3
            
         if render:
             res = ""
             for mess in   self.responses:
                 res += mess + "\n"
             LEADER_FOLLOWER = "Local" 
             # Send HTTP response  
             # Send HTTP response 
             response = """HTTP/1.0 200 OK\n\n
                   <html>  
                   <header>
  
                   <meta content='width=device-width, initial-scale=1' name='viewport'/> 
                   <style> 
                     body      {  font: normal 14px Verdana, Arial, sans-serif; background-color: %s }
                     button    {  font-size: 14px; font-family:  Verdana;  } 
                     .form-response  {  font-size: 14px; font-family:  Verdana; width: 300px;   height: 150px; textAlignLast = "left"; }
                     .form-control   {  font-size: 14px; font-family:  Verdana; width: 300px;   height: 50px; }
                     .panel {  padding: 2 2px; font-size: 10px;  background-color: white;  max-height: 0; width: 300px;  overflow: hidden;  transition: max-height 0.2s ease-out; }
                     p { margin:0 }
                     i { margin:0 }
                   </style>

                   </header>
                   <body> 
                    <div style ="float:left" >
                       <a href = "https://robotfreedom.com" >
                          <img src="/assets/logo_small.1.png" alt="RobotFreedom.com" width="50" height="50"> 
                       </a>
                    </div>  
                    <b>&nbsp;&nbsp;%s</b> <br/>
                    <b>&nbsp;&nbsp;%s Command Console</b>  
                    <br/>
                    <br/>
                    <br/>
                    <div id="chatbox">
                     <textarea class="form-response" id="chatarea" readonly  name="message"  style="overflow:scroll;">%s</textarea>
                    </div>
                    <br/>
                    <form action="" method="post"> 
                         <textarea class="form-control" id="message" placeholder="Message"  name="message" ></textarea>
                    <br/> 
                    <br/> 
                           <button type="submit" class="btn btn-default" id="sendmsg" >Send</button> 
                   </form>

                   <button class="accordion">Help</button>  
                   <div class="panel"   > 
                      <h3>Commands:</h3>
                      <b>speak</b>
                      <p>&nbsp;&nbsp;speak "hello"@robot_1</p>
                      <p>&nbsp;&nbsp;speak "Time for making!"@all</p> 
                      <b>dinner</b>
                      <p>&nbsp;&nbsp;Has every robot annouce dinner</p>  
                      <b>move</b>
                      <p>&nbsp;&nbsp;move raise,left,arm @number_3</p>
                      <b>roll</b>
                      <p>&nbsp;&nbsp;roll 6d</p> 
                      <p>&nbsp;&nbsp;roll flip</p> 
                      <b>bye</b>
                      <p>&nbsp;&nbsp;bye</p> 
                      <b>kill-all</b>
                      <p>&nbsp;&nbsp;Stops all robotic programs.</p>
                      <b>start</b>
                      <p>&nbsp;&nbsp;Starts robots in monitor mode.</p>
                      <b>start-listen</b>
                      <p>&nbsp;&nbsp;Starts robots in listen mode.</p>
                      <b>status</b>
                      <p>&nbsp;&nbsp;Returns all Python programms running locally.</p>
                      <b>nerves</b>
                      <p>&nbsp;&nbsp;Returns Key/Values in local nerves.</p>

                    </div>
                    <script>
                     var acc = document.getElementsByClassName("accordion");
                     var i;
                     
                     for (i = 0; i < acc.length; i++) {
                       acc[i].addEventListener("click", function() {
                         this.classList.toggle("active");
                         var panel = this.nextElementSibling;
                         if (panel.style.maxHeight) {
                           panel.style.maxHeight = null;
                         } else {
                           panel.style.maxHeight = panel.scrollHeight + "px";
                         } 
                       });
                     }
                   </script>
                   </body>
                   </html>""" %   (self.color, self.robot, LEADER_FOLLOWER,  res)
              
             client_connection.sendall(response.encode())
             client_connection.close()
      
         # Close socket
         server_socket.close() 

if __name__ == "__main__":
   """
   
   """
   i_attempts = 0
   while 1:
       
       IPAddr = get_local_ip()
       i_attempts += 1

       if IPAddr != "127.0.0.1" or i_attempts > 1 :
          srv = HTTPServer(False) 

          try:
              srv.server_forever()
          except Exception as e:
              print(e)

       time.sleep(10)
       print("waiting to connect...")