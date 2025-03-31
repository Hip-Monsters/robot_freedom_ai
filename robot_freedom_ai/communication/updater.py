#!/usr/bin/python
# -*- coding: utf-8 -*- 

"""
Description:  
Author: HipMonsters.com 
License: MIT License
""" 

import os  


def Updater(object):
     
     def __init__(self,ipaddr ):
          """
          
          """
          self.ipaddr = ipaddr
 

     def update(self, stype ):
          """
          """
          if stype == "code":
              cmds = """ 
curl %s/updates/code/ --output updates.zip

unzip -o updates.zip

rm updates.zip
""" % self.ipaddr  
 
          elif stype == "settings":
              cmds = """ 
cd ../settings

curl %s/updates/data/ --output settings.zip
  
unzip -o settings.zip

rm settings.zip
""" % self.ipaddr  

          os.system(cmds)

if __name__ == "__main__":

     ip = "" #need to import net_config
     updater = Updater(ip)
     updater.update("code")