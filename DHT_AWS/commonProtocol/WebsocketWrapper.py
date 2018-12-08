#!/usr/bin/env python3
import tornado.websocket
import socket
import tornado.ioloop
import tornado.web
from threading import Thread
import asyncio
import time


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ("new connection")
            
    def on_ping(self,data):
        a = 1
      
    def on_message(self, message):
        #print ('WS protocol message received:  %s' % message)
        #print ('WS protocol sending back message: %s' % message)
        self.write_message(message)
            
    def on_close(self):
        print ('connection closed')
                
class WebsocketWrapper(Thread):
    def __init__(self, port = 8111, daemon = False):
        Thread.__init__(self)
        self.port = port
        
    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.server = tornado.web.Application([
        (r"/ws", WSHandler)
        ])
        self.server.listen(self.port)
        ipAddr= socket.gethostbyname(socket.gethostname())
        print ('___Protocol Comparision Websocket Server Started at %s:%s___' % (ipAddr,str(self.port)))
        self.ioinstance = tornado.ioloop.IOLoop.current()
        self.ioinstance.start()
        self.ioinstance.close()
        print ("Protocol Comparision Webserver stopped")
        
    def stop(self):
        self.ioinstance.add_callback(self.ioinstance.stop)
        print("Closing Protocol Comparision Websocket server")
    
 
if __name__ == "__main__":
    webserver = WebsocketWrapper()
    webserver.start()