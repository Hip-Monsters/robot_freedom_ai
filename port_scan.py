# -*- coding: utf-8 -*-
  
"""
Description: Port scanner to find which port to connect to for the Arduino.
Author: HipMonsters.com 
Date Created: Jan 1, 2023
Date Modified: Oct 10, 2024
Version: 1.0 
License: MIT License  
"""
 
from os import system   
 
 
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
 

 