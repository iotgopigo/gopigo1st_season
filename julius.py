#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
  
host = 'localhost'
port = 10500
  
clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsock.connect((host, port))
  
while True:
        recv_data = clientsock.recv(1024)
	print(recv_data)
