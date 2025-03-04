#!/usr/bin/env python
"""  


""" 

import os 
from os import system  
import time
import csv 
import argparse
 
 
import serial 
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
 
for p in ports:
    res =  ['device', 'hwid', 'interface', 'location', 'manufacturer', 'name', 'pid', 'product', 'serial_number', 'usb_description', 'usb_info', 'vid']
 
    print (p.device,  p.name,  p.usb_info())
    
    try:
       print (ser = serial.Serial(p[0]))
    except:
       print('blaw')
 

 