#!/bin/bash

# Description: Starting script for AI Agent and sensor daemons on a OSX.
# Author: HipMonsters.com 
# License: MIT License 

osascript -e 'tell app "Terminal" to do script "cd ./Desktop/robot_freedom_ai/; python3 server.py"'

osascript -e 'tell app "Terminal" to do script "/usr/local/opt/memcached/bin/memcached -l localhost"' 

osascript -e 'tell app "Terminal" to do script "cd ./Desktop/robot_freedom_ai/; python3 daemon_wrangler.py -m monitor"'

osascript -e 'tell app "Terminal" to do script "cd ./Desktop/robot_freedom_ai/; python3 agent.py -m monitor -r number_3"'

osascript -e 'tell app "Terminal" to do script "cd ./Desktop/robot_freedom_ai/; python3 console.py"'

 
