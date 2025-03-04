# -*- coding: utf-8 -*- 
"""
Description: Securtiy layer for agent (This is a stub).
Author: HipMonsters.com 
License: MIT License
"""  

import platform
import time 
from getpass import unix_getpass 
 
class Firewall():
    
    def __init__(self, nerves):
        """
        
        """
        self.acceptable_ips = ["127.0.0.1"]
        self.blocked_ips    = []
        self.open_ports = ["80"] 
        self.open_protcolss = ["http"] 

    def network_address_translation(self):
        """
        """
        return True
    
    def static_packet_filtering(self, ip, port, protocol):
        """
        """
        return True 

    def packet_filtering(self, ip, port, protocol):
        """
        """
        b_ok = False

        if ip in self.acceptable_ips:
            b_ok = True


        return b_ok 

    def application_binspection():
        """
        
        """
    def proxy_firewall():
        """
        """

class Passwords():
    def __init__(self):
         """

         
         """
         
  
class Security(object):

    def __init__(self, robot, config, nerves):
        """
        "firewall", "otpasskeys", "cmd_filters", "oauth2", "threatscore"
        
        """    
        self.robot     = robot
        self.os        = config.OS 
        self.nerves    = nerves 
        self.firewall  = Firewall(nerves)
        self.passwords = Passwords()
           
    def command_filter(self, message, history): 
        """
        
        """
        pass  
     
    
    def one_time_passwords(self, message, history): 
        """
        
        """
        pass  