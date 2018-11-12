#!/usr/bin/env python3
import tornado.websocket
import socket
import tornado.ioloop
import tornado.web
import json
from PIL import Image
from threading import Thread
import asyncio
from database import Database
import time

clients = []
db = None

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        if self not in clients:
            print ("new connection")
            clients.append(self)
            
    def on_ping(self,data):
        a = 1
      
    def on_message(self, message):
        #print ('message received:  %s' % message)
        # Reverse Message and send it back
        #print ('sending back message: %s' % message)
        #self.write_message(message[::-1])
        requestObject = json.loads(message)
        #print ("Json:", requestObject)
        if ("request" in requestObject.keys()):
            global db
            entity = requestObject["request"][0]["entity"]
            requestObject["response"] = requestObject.pop("request")
            print ("Entity:",entity)
            if "temperature" in entity:
                #handle temperature
                type = requestObject["response"][0]["type"]
                if "latest" in type:
                    latestData = list(db.getLatestData(1)[0])
                    print ("Retrieved data:",latestData)
                elif "average" in type:
                    latestData = list(db.getTemp(0))
                    print ("Retrieved data:",latestData)
                elif "lowest" in type:
                    latestData = list(db.getTemp(1))
                    print ("Retrieved data:",latestData)
                elif "highest" in type:
                    latestData = list(db.getTemp(2))
                    print ("Retrieved data:",latestData)
                else:
                    print("Error")
                requestObject["response"][0]["value"] = latestData[1]
                
            elif "humidity" in entity:
                #handle humidity
                #print("Handle hum")
                type = requestObject["response"][0]["type"]
                if "latest" in type:
                    latestData = list(db.getLatestData(1)[0])
                    latestData[1] = latestData[2]
                    #print ("Retrieved data:",latestData)
                elif "average" in type:
                    latestData = list(db.getHum(0))
                    #print ("Retrieved data:",latestData)
                elif "lowest" in type:
                    latestData = list(db.getHum(1))
                    #print ("Retrieved data:",latestData)
                elif "highest" in type:
                    latestData = list(db.getHum(2))
                    #print ("Retrieved data:",latestData)
                else:
                    print("Error")
                    
                requestObject["response"][0]["value"] = latestData[1]
            
            requestObject["response"][0]["timestamp"] = latestData[0]
            
            #print ("Json:", requestObject)
            #print ("response:",requestObject)
            self.write_message(requestObject)
            
        elif ("ping" in requestObject.keys()):
            #print ("Ping")
            a = 1
        else:
            print ("Invalid Method")
 
    def on_close(self):
        if self in clients:
            clients.remove(self)
            print ('connection closed')
 
    def check_origin(self, origin):
        return True
 
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("www/index.html")
            
class PagesHandler(tornado.web.RequestHandler):
    def get(self, url):
        print ("URL:",url)
        #req_uri = self.request.uri
        #print ("URL ", req_uri)
        if url is not None:
            if ".jpg" in url:
                #img = Image.open("www/"+url)
                #data = cStringIO.StringIO()
                #image.save(data, 'JPEG')
                #self.render(data.getvalue().encode("base64"))
                self.render("www/"+url)
            else:
                self.render("www/"+url)
                
class DHTWebserver(Thread):
    def __init__(self,DBInstance = None, daemon = False):
        if(DBInstance is None):
            print("No DB")
            DBInstance = Database()
        Thread.__init__(self)
        global db
        db = DBInstance
        #t = Thread(target=self.run)
        #t.daemon = daemon
        #t.start()
        
    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.server = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/(.*.html)", PagesHandler),
        (r"/(.*.js)", PagesHandler),
        (r"/(.*.css)", PagesHandler),
        (r"/(.*.jpg)", PagesHandler),
        (r"/ws", WSHandler)
        ])
        self.server.listen(8888)
        ipAddr= socket.gethostbyname(socket.gethostname())
        print ('___Websocket Server Started at %s___' % (ipAddr))
        self.ioinstance = tornado.ioloop.IOLoop.current()
        self.ioinstance.start()
        self.ioinstance.close()
        print ("Webserver stopped")
        
    def stop(self):
        self.ioinstance.add_callback(self.ioinstance.stop)
        print("Closing Websocket server")
        
    
 
if __name__ == "__main__":
    webserver = DHTWebserver()
    webserver.start()
 