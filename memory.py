# -*- coding: utf-8 -*-
  
"""
STUB
Description: Interface for Memory (memcache) to connect componetns to agent(s).
Author: HipMonsters.com 
License: MIT License 
sudo apt install memcached libmemcached-tools -y
else OSS 
brew install memcached.

sudo systemctl status memcached

sudo systemctl start memcached.service
sudo systemctl enable memcached.service
pip install pymemcache/usr/local/opt/memcached/bin/memcached -l localhost

/usr/opt/memchaed/
client.set('key', 'value')
sudo apt install memcached libmemcached-tools -y
memcached -l localhost
which memchased 
"""
 
import sys  
from os import system    
from pymemcache.client import base

class Memory(object):

    
    def __init__(self,  name  , ip=None):
        """
        
        
        """
        
        self.header_length = 10
        
        if ip is None:    
           self.ip =   "127.0.0.1"
        else:
           self.ip =  ip
        
        self.port = 11211
        self.client = base.Client((self.ip, self.port))
 
    def set(self, key, value ): 
        """
        """
        self.client.set( key, value )
    
    def get(self, key ): 
        """
        """
        return self.client.get( key )
 
    def pop(self, key ): 
        """
        """
        val = self.client.get( key )
        if val is not None:
              if val is not False:
                  self.client.set( key, False )
                  return True, val
                  
        return False, {}
 
    def clear(self, key ): 
        """
        """ 
        self.client.set( key, False ) 

 
if __name__ == "__main__":
    """
    """ 
