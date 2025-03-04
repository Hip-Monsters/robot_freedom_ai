# -*- coding: utf-8 -*-
"""
Description: Sensor daemon for tempature and humidity.
Author: HipMonsters.com 
License: MIT License
"""
import json 

from ._sense  import SenseBase
 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode")  
parser.add_argument("-r", "--robot") 
parser.add_argument("-a", "--args")    


class  TempatureHumidity(SenseBase):

    def __init__(self, robot, nerves, config, settings, pins ={"pin_1":37}):
        """
        
        """
        super().__init__(robot, nerves, config, settings, "tempature_humidity") 
        
        self.pins = pins
        if self.os == "LINUX":
            import board
            import adafruit_dht 
            #pip install adafruit-circuitpython-dht
            self.dhtDevice = adafruit_dht.DHT11(board.D26)
               
        self.sense_1 = "tempature" 
        self.sense_2 = "humidity"  
        self.counter = 0
        self.start_temp = 0
        self.start_humid  = 0
            
    def poll(self):
        """
        """ 
           
        if self.os == "LINUX":
            
            temperature_c = self.dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32

            humidity = self.dhtDevice.humidity

            print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))

            if abs(temperature_f - self.start_temp) > 10: 
               self.start_humd =    temperature_f                      
               return [True ,temperature_f,  "temperature"]
            
            if abs(humidity - self.start_humd) > 10:       
               self.start_humd =    humidity       
               return [True , humidity, "humidity"]
            
        elif self.os == "OSX":
            
           if self.counter  >= self.args["max"]:
               self.counter = 0
               return [True, "timeout"]

        
        return [False, ""]
     

if __name__ == "__main__":
    """ 
    
    """
    args =  parser.parse_args() 

    mode    = args.mode 
    robot   = args.robot   
    args    = json.loads(args.args  ) 

    print(  "\r" + mode , end ="")
    touch  = TempatureHumidity(robot, args )
    if mode == "serve":
        touch.serve_forever()
