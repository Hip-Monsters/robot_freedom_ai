#!/usr/bin/python
# -*- coding: utf-8 -*- 
"""
Description: Memcache client for daemons and agent.
Author: HipMonsters.com 
License: MIT License
"""  

import sys
import socket 
import time
import errno 
import socket   

class Client(object):

    
    def __init__(self, robot  , ip=None):
        """
        
        """
        
        self.header_length = 10
        
        if ip is None:    
           self.ip =   "127.0.0.1"
        else:
           self.ip =  ip
        
        self.port = 1234
        self.robot = robot
        self.b_connected = False
        self.reconnect_tries = 0


    def connect(self):
        """
        
        """ 
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
        # Connect to a given ip and port 
        #print(self.ip, self.port)
        try:
           self.client_socket.connect((self.ip, self.port))
        except Exception as e:
            print(e)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            return False 
        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        self.client_socket.setblocking(False)
        
        # Prepare username and header and send them
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username = self.robot
        username = username.encode('utf-8')
        username_header = f"{len(username):<{self.header_length}}".encode('utf-8')
        self.client_socket.send(username_header + username) 
        return True
    
    def check_connection(self):
        """
        
        """  
        return True  
        try:
           username_header = self.client_socket.recv(self.header_length)
           if not len(username_header): 
              connected = False
              self.reconnect_tries  += 1
              if self.reconnect_tries  >= 30:
                  connected = self.connect()
                  self.reconnect_tries  = 0

              return connected 
          # self.connect()
        except:
              try:
                  connected = False
                  self.reconnect_tries  += 1
                  if self.reconnect_tries  >= 30:
                      connected = self.connect()
                      self.reconnect_tries  = 0
              except:
                   print("Not Connected...")
              return connected 
             

        return True
    
        try:
             self.client_socket.connect((self.ip, self.port))
             self.client_socket.setblocking(False)
 
        
        except socket.error as e:
              if e.errno == 56: 
                 return True
              elif str(e.strerror).find("already connected") > -1: 
                 return True
              else: 
                  print(str(e.errno))
                  print(str(e.strerror))
                  print("Socket Error:", e)
                  self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  return False
          
        except ConnectionResetError:
             return False
        
        except Exception as e:
             print(str(e)) 
             return False
        
        return True 
         
    
    def check_for_a_message(self, recipient,  expected_reply , sent_from):
        """
        check_for_a_message("number2", "step 1 done?", "yes")

        """  
        b_announced = False
        b_connected = self.check_connection()
      
        if b_connected: 
            try:
                    # Receive our "header" containing username length, it's size is defined and constant
                    username_header = self.client_socket.recv(self.header_length)
        
                    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                    if not len(username_header):
                        print('Connection closed by the server')
                        return False, "Connection closed by the server"
        
                    # Convert header to int value
                    username_length = int(username_header.decode('utf-8').strip())
        
                    # Receive and decode username
                    username = self.client_socket.recv(username_length).decode('utf-8')
        
                    # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                    message_header = self.client_socket.recv(self.header_length)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = self.client_socket.recv(message_length).decode('utf-8')
                    parts  = message.split("@")
                    to, reply  = parts[1].split(">") 
                    if sent_from.upper() == "ANYONE":
                        if reply == expected_reply and to == recipient:
                             b_announced = True 

                    elif   to.upper()  == "ANYONE":
                             b_announced = True 
                    else:
                        if reply == expected_reply and to == recipient and username == sent_from :
                             b_announced = True 
        
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e))) 
                    b_announced = False  
        else:
            print("\nNOT CONNECTED TO SERVER\n")

        return  b_announced
        
    def check_messages(self):
        """ 

        """  

        b_connected = self.check_connection()
        b_new_messages = False
        message        = ""

        if b_connected:  
            try:
                    
                    # Receive our "header" containing username length, it's size is defined and constant
                    username_header = self.client_socket.recv(self.header_length)
        
                    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                    if not len(username_header):
                        print('Connection closed by the server')
                        return [False, "error"]
        
                    # Convert header to int value
                    username_length = int(username_header.decode('utf-8').strip())
        
                    # Receive and decode username
                    username = self.client_socket.recv(username_length).decode('utf-8')
        
                    # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                    message_header = self.client_socket.recv(self.header_length)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = self.client_socket.recv(message_length).decode('utf-8')
                    parts  = message.split("@")
                    to, reply  = parts[1].split(">")  

                    if to.lower() == "announcement": 
                        b_new_messages = True 
                        message = reply

                    elif to.lower() == "all": 
                        b_new_messages = True 
                        message = reply
                         
                    elif to.lower() == "notification": 
                        b_new_messages = True 
                        message = reply
                         
                    elif to == self.robot:
                        b_new_messages = True 
                        message = reply
        
            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e))) 
                    b_new_messages = False  

        return [b_new_messages, message]
    
    def check_messages_for(self, mess):
        """ 

        """  
        b_connected = self.check_connection()
        b_new_messages = False
        message        = ""

        if  b_connected :  
            try:
                    # Receive our "header" containing username length, it's size is defined and constant
                    username_header = self.client_socket.recv(self.header_length)
        
                    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                    if not len(username_header):
                        print('Connection closed by the server')
                        return [False, "error"]
        
                    # Convert header to int value
                    username_length = int(username_header.decode('utf-8').strip())
        
                    # Receive and decode username
                    username = self.client_socket.recv(username_length).decode('utf-8')
        
                    # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                    message_header = self.client_socket.recv(self.header_length)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = self.client_socket.recv(message_length).decode('utf-8')
                    parts  = message.split("@")
                    to, reply  = parts[1].split(">") 

                    if to.lower() == "notification" and   reply.lower() == mess.lower(): 
                        b_new_messages = True 
                        message = reply
 
        
            except IOError as e:
                   if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e))) 
                    b_new_messages = False 
         

        return [b_new_messages, message]
    
    def update(self): 

        b_connected = self.check_connection()  
        if b_connected:
            message = self.robot + "@" + "recipient" + ">"  + 'sys:update'
        
        
    def send(self, recipient, message):
        """
            
        """

        b_connected = self.check_connection()  
        if b_connected:
            message = self.robot + "@" + recipient + ">"  + message
        
            # If message is not empty - send it
            
            if 1 ==1:# message:
        
                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                message = message.encode('utf-8')
                message_header = f"{len(message):<{self.header_length}}".encode('utf-8')
                self.client_socket.send(message_header + message)
                
        
            try:
                # Now we want to loop over received messages (there might be more than one) and print them
                b_continue = True
                while b_continue:
        
                    # Receive our "header" containing username length, it's size is defined and constant
                    username_header = self.client_socket.recv(self.header_length)
        
                    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                    if not len(username_header):
                        print('Connection closed by the server')
                        sys.exit()
        
                    # Convert header to int value
                    username_length = int(username_header.decode('utf-8').strip())
        
                    # Receive and decode username
                    username = self.client_socket.recv(username_length).decode('utf-8')
        
                    # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                    message_header = self.client_socket.recv(self.header_length)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = self.client_socket.recv(message_length).decode('utf-8')
        
                    # Print message
                    b_continue = False
        
            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
        
                # We just did not receive anything
                 
        
            except Exception as e:
                # Any other exception - something happened, exit
                print('Reading error: '.format(str(e)))  

        return  message


if __name__ == "__main__":
    print("Creating a connection socket and start listening to the clients")
    comd = Client("test", "192.168.1.4")
    comd.connect()
    while comd.check_connection() == False:
        print("Waiting ....")
        time.sleep(1)

    comd.send("all", "Hi")