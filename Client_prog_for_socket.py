# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 13:35:41 2021

@author: pcochang
"""

import socket
import time

host = 'replace with ip of server (raspi with camera)'
port = 1403
execution_wait_time = 3600 # set to 1Hr interval



def setupClient_to_ServerConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    return s
    

    
    
while True:
    try: 
        s = setupClient_to_ServerConnection()
        #user = input("")
        client_data = "This is the CLient: What is the lettuce area ?"
        s.send(str.encode(client_data)
       
        # this line is where the client hear back from server
        lettuce_area = s.recv(1024)
        s.close()
        print("Data from server (lettuce area): ",lettuce_area.decode('utf-8'))
        
        #######define the function to measure sensors
        ######define function here for Naive Bayles Probability

        time.sleep(execution_wait_time)
    except:
        time.sleep(1)
        
    
