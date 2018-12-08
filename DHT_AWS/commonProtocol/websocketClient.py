#!/usr/bin/python3

from websocket import create_connection
ws = create_connection("ws://localhost:8111/ws")
print ("Sending 'Hello, World'...")
ws.send("Humara Bajaj")
print ("Sent")
print ("Reeiving...")
result =  ws.recv()
print ("Received '%s'" % result)
ws.close()
