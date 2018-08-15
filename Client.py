
"""
Created on Wed Aug  1 13:20:24 2018

@author: https://stackoverflow.com/questions/42458475/sending-image-over-sockets-only-in-python-image-can-not-be-open
"""
#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime
from random import randint

image = "Erno smiley.png"

HOST = '131.174.106.195'
PORT = 5800

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)

sock.connect(server_address)

try:
    
    # open image
    myfile = open(image, 'rb')
    bytes = myfile.read()
    size = len(bytes)
      

    # send image size to server
    
    # send image to server
    text = 'picture'
    
    sock.sendall(str.encode(text))
    data = sock.recv(4096)
    answer = data.decode('utf-8')
    print(answer)
    data = sock.recv(4096)
    answer = data.decode('utf-8')
    print(answer + "TRALALA")
    if answer == 'Received' :
      
    
        sock.send(bytes)
        print("IETS")
    
        # check what server send
        data = sock.recv(4096)
        answer = data.decode('utf-8')
        print("IETS2")
        print ('answer = %s' % answer)

    if answer == 'Received' :
        
        print ('Image successfully send to server')

    myfile.close()

finally:
    sock.close()
    