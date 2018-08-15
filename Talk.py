#!/usr/bin/env python
import socket
import sys
from _thread import *

basename = "image.png"
textname = "text.txt"
host = ''
port = 5800                         #The port that you want to open
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Making socket

try:
    s.bind((host,port))
except socket.error as e:
    print(str(e))

s.listen(1)                         #Amount of devices that can connect simultaniously

print('Waiting for a connection')

def threaded_clientTalk(conn):
    conn.send(str.encode("Welcome, please send no more than 64 characters" + '\n' ))
    while True:
        data = conn.recv(4000)                  #gets data from device
        reply = "We got this from you: " + data.decode('utf-8')     #The data needs to be decoded when using python3, if you use python 2 than remove the decode part
        if not data:
            break
        conn.sendall(str.encode(reply))                             #again encode is only for python3
        myFile = open(textname, "w")
        myFile.write((data.decode('utf-8')+"}"))
        myFile.close()
        conn.close()                                        #Stop the connection so someone else can send text

def threaded_clientPicture(conn):
    conn.send(str.encode("Received"))                   
    data = conn.recv(409600000)                             #get data of the picture
    
    if (len(data)>10):
            
            myfile = open(basename, 'wb')
            
            myfile.write(data)
        
            myfile.close()
            
            print("done")
            conn.send(str.encode("Received"))
            
    conn.close()
    
while True:
    conn, addr = s.accept()
    print('connected to: ' + addr[0] + ':' + str(addr[1]))
    conn.send(str.encode("Start by sending only the word text" + '\n' ))
    data = conn.recv(4096)                
    text = data.decode('utf-8')
    if data:
        print(text)
    if 'picture' in text:
        start_new_thread(threaded_clientPicture,(conn,))
    if 'text' in text:
        start_new_thread(threaded_clientTalk,(conn,))
    


