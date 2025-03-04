#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name 
#https://www.aranacorp.com/en/serial-communication-between-raspberry-pi-and-arduino/

import serial,time
import platform
import serial.tools.list_ports

from .sequences import RESETS

class MOBILITY(object):

    def __init__(self, default_device, strict=True):
        """
        
        """
        self.strict  = strict
        self.connections = {}
        self.default_device   = default_device

    def reset(self):    
        """
        
        """
        res = {}
        for cmd in RESETS:
            res[cmd] = True
            self.write(cmd)
        return res 
    
    def connect_to_devices(self,  devices):
       """

       """ 
       connected = False
       self.devices = devices
       try:
           for name,  data in self.devices.items():
                port, snd  = data 
                self.connections[name] = serial.Serial(port, 9600, timeout=1) 
                connected = True
                time.sleep(4) #wait for serial to open
       except:
            
            ports = list(serial.tools.list_ports.comports()) 
            for p in ports:
              #  print(p.device)
                if str(p.manufacturer).find("arduino") > -1:
                    port = p.device
                    self.connections[name] = serial.Serial(port, 9600, timeout=1) 
                    self.devices = {name: (port, 1)}
                    connected = True
                    time.sleep(4) #wait for serial to open
                    break
             
             
       return connected
    
    def write(self, cmd, device = None): 
        """
 
        """ 
        answer = ''
        if device is None:
           device =  self.default_device


        if device not in self.connections:

            found = self.connect_to_devices(self.devices)
            if found is False:
                 return "Not Connected" 

        arduino = self.connections[device] 
 
        
        if arduino.isOpen() == False: 
            port = arduino.port
            self.connections[name] = serial.Serial(port, 9600, timeout=1)
            time.sleep(.1) #wait for serial to open
            print("{} connected!".format(arduino.port)) 

        try:  
            arduino.write(cmd.encode()) 
            time.sleep(0.05) #wait for arduino to answer
          #  while arduino.inWaiting()==0: 
           #     pass
          #  if  arduino.inWaiting() > 0: 
           #     answer=arduino.readline() 
            arduino.flushInput() #remove data after reading
             #   time.sleep(0.05) #wait for arduino to answer

        except:
            answer = "Error"
            print("error")

        return answer
    
    def write_read(self, cmd, device = None): 
        """
 
        """ 
        answer = ''
        if device is None:
           device =  self.default_device

        arduino = self.connections[device] 
        
        if arduino.isOpen() == False: 
            port = arduino.port
            self.connections[name] = serial.Serial(port, 9600, timeout=1)
            time.sleep(.1) #wait for serial to open
            print("{} connected!".format(arduino.port)) 

        try:  
            arduino.write(cmd.encode()) 
            time.sleep(0.05) #wait for arduino to answer
            while arduino.inWaiting()==0: 
                pass
            if arduino.inWaiting() > 0: 
                answer=arduino.readline() 
                arduino.flushInput() #remove data after reading
             #   time.sleep(0.05) #wait for arduino to answer

        except:
            answer = "Error"
            print("error")

        return answer
        
    def run(self):
      
      if  platform.system() == "Darwin": 
         port = '/dev/cu.usbmodem14201' 
      else:
         port = "/dev/ttyACM0" 
      print('Running. Press CTRL-C to exit.')

      with serial.Serial(port, 9600, timeout=1) as arduino:
        time.sleep(.05) #wait for serial to open
        if arduino.isOpen():

            
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    cmd  =input("Enter command : ") 
                    cmd = cmd.strip()
                    arduino.write(cmd.encode())
                    time.sleep(0.05) #wait for arduino to answer
                    #while arduino.inWaiting()==0: 
                    #    pass
                    #if  arduino.inWaiting()>0: 
                     #  answer=arduino.readline() 
                     #  print(answer)
                    arduino.flushInput() #remove data after reading

            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")

if __name__ == '__main__':
     
    name = "test"
    controller = Controller(name) 
    device_connections = {}  

    if  platform.system() == "Darwin": 
        device_connections[name] = ('/dev/cu.usbmodem14201',"113") 
    else:
         device_connections[name] = ("/dev/ttyACM0", "1")

    controller.connect_to_devices(device_connections) 
   
    for i in range(2):
       print("write 5")
       answer = controller.write('5', "test" ) 
       print(answer)
       time.sleep(2)
       print("write 0")  
       answer  = controller.write('0', "test" ) 
       print(answer)
       time.sleep(2) 

    controller.run()