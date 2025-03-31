#!/usr/bin/python
# -*- coding: utf-8 -*- 

"""
Description:  
Author: HipMonsters.com 
License: MIT License
""" 

import subprocess
import urllib.request
import socket  
import os

def check_ips_role(ip, role):
    """
    
    """

    try:
        contents = urllib.request.urlopen("http://" + ip + ":8000/whois/", timeout=2).read()
        contents = str(contents, 'utf-8')
    except:
        contents = "" 
    print(contents)
    if contents.startswith(role):
        return True
    else:
        return False
    
    

def auto_discovery():
    """
    
    """
    devices = {}
    devices["all"]     = {}
    devices["robots"]  = {}
    devices["hubs"]    = {}
    devices["repositories"] = {} 
    """  
    cmd = subprocess.run(["arp", "-a"], capture_output=True)
    a = str(cmd).split(",")
    b = a[3].replace("stdout=b'", "").replace("\\n", "\n")  
    nets = b.split("on wlan0")[0].split("\n")
     pip package kamene
    """
    nets  = map_network()
    
    for ip in nets: 
        """  
    for net in nets: 
        pattern = r"\((.*?)\)"
        match = re.search(pattern, net)
        print(net)
        if match is not None:
           ip = match.group(1)
        else:
           ip = net 
        """ 
        devices["all"][ip] = "Active"  
        try:
            contents = urllib.request.urlopen("http://" + ip + ":8000/whois/", timeout=1).read()
            contents = str(contents, 'utf-8')
        except:
            contents = "" 

        if contents.startswith("robot:"):
            devices["robots"][ip]  = contents.split(":")[1] 
            
        elif contents.startswith("hub:"):
            devices["hubs"][ip]  = contents.split(":")[1] 

        elif contents.startswith("repository:"):
            devices["repositories"][ip]  = contents.split(":")[1] 


    return devices
 


def ping(ip):
    """
    Do Ping
    :param ip: 
    :return: bool
    """
    t =  os.system("ping " + ip + " -c1 -t 1")
    if t == 0:
        return True
    else:
        return False 
    
def ping_thread(ip):
    DEVNULL = open(os.devnull, 'w')
    while True:  
        try:
            subprocess.check_call(['ping', '-c1', ip],
                                   stdout=DEVNULL)
             
            return True
        except:
            return False

def map_rf_ips(b_stop_on_hub=True):
   
    ip_parts = get_local_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
       
    devices = {}
    devices["all"]     = {}
    devices["robots"]  = {}
    devices["hubs"]    = {}
    devices["repositories"] = {}
    b_repository = False
    b_hub        = False
    for i in range(1, 255):
        ip = base_ip + '{0}'.format(i)
        print(ip)
        try:  
            contents = urllib.request.urlopen("http://" + ip + ":8000/whois/", timeout=1).read()
            contents = str(contents, 'utf-8')  
            print(contents)
        except:
            contents = "" 

        if contents.startswith("robot:"):
            devices["robots"][ip]  = contents.split(":")[1] 
            
        elif contents.startswith("hub:"):
            devices["hubs"][ip]  = contents.split(":")[1] 
            b_hub = True 

        elif contents.startswith("repository:"):
            devices["repositories"][ip]  = contents.split(":")[1] 
            b_repository = True

        if b_stop_on_hub :
            if b_hub:
                break
        else :
            if b_hub and b_repository:
                break


    return devices

def get_local_ip():
    """
    
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def map_network():

    
    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_local_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
      
    # cue hte ping processes
    ips = []
    for i in range(1, 255):
        test = base_ip + '{0}'.format(i)
        valid = ping(test)
        if valid:
            ips.append(test)


if __name__ == "__main__":
     print(auto_discovery())