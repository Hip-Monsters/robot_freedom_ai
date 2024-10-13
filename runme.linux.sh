#!/bin/bash
# Description: Starting script for AI Agent and sensor daemons on a RaspberryPi.
# Author: HipMonsters.com 
# License: MIT License
# Note: https://raspberrypi.stackexchange.com/questions/61913/how-to-set-the-lxterminal-to-stay-when-running-a-command

lxterminal -e "python3 server.py;bash" 

lxterminal -e "memcached -l localhost ; bash" 

lxterminal -e "python3 daemon_wrangler.py -m monitor ; bash" 

lxterminal -e "python3 agent.py -m monitor -r example_robot ; bash" 

lxterminal -e "python3 console.py ;bash"  

 