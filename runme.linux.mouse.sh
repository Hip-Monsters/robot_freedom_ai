#!/bin/bash
# Description: Starting script for mouse
# Author: HipMonsters.com 
# License: MIT License
# Note: https://raspberrypi.stackexchange.com/questions/61913/how-to-set-the-lxterminal-to-stay-when-running-a-command

lxterminal -e "python3 server.py;bash" 

lxterminal -e "memcached -l localhost ; bash" 

lxterminal -e "python3 daemon_wrangler.py -m monitor ; bash" 

lxterminal -e "python3 mouse.py -m monitor -r mouse ; bash"
 
 
