"""

"""
import platform
import json 
from datetime import datetime

PATH = "../data/"
DATA_PATH = "../data/settings/"
CHAT_PATH = "../data/chat/"
VOICES_PATH = "../data/voices/"
LOGS_PATH = "../data/logs/"
CONFIG_PATH = "../data/config/"
OUTPUT_PATH = "../data/output/"
UPDATES_PATH = "../data/updates/"

START_DT     = datetime.now()
START_DT_STR = START_DT.strftime("%Y-%m-%d %H:%M:%S")
START_DT_F   = START_DT.strftime("%Y_%m_%d_%H_%M_%S")

DEBUG_MODE = False
VERBOSE = False
 
config_file = open(CONFIG_PATH + "config.json")
data = ""
for line in config_file:
    data  +=  line 
CONFIG = json.loads(data)  

DEFAULT_2_NETWORKED = -1
if CONFIG["default_to_networked"] == 1:
    DEFAULT_2_NETWORKED = 1
    
    

OS = "LINUX" 
if platform.system() == 'Windows':
    OS = "WIN"
    
elif platform.system() == 'Darwin': 
    OS = "OSX"  

try:
    config_file = open(CONFIG_PATH + "net_config.json")
    data = ""
    for line in config_file:
        data  +=  line

    NET_CONFIG = json.loads(data) 
except:
    NET_CONFIG = {}
    NET_CONFIG["robots"]    = {}
    NET_CONFIG["hubs"]        = {"192.168.1.72":"number_b"}
    NET_CONFIG["repositories"]= {"192.168.1.7": "number_a"}

    config_file = open(CONFIG_PATH + "net_config.json", "w")
    config_file.write(json.dumps(NET_CONFIG ,indent=4))
     
 
API_KEY = "<your key>"
UPDATE_KEY = "<your key>" 

       