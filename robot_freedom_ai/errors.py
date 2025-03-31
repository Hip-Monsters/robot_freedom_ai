# -*- coding: utf-8 -*-
"""
 
""" 

####    Libraries   ################
 
import traceback

def handle_exceptions(f):
    def wrapper(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception as e:
            self = args[0] 
            print("ERROR   ")
            print(e)   
            print(args)
            print(kw)
            print(traceback.format_exc()) 
            print("END ERROR ")  
            raise
            stop
            #exception_handler(self.log, True)

    return wrapper 
     