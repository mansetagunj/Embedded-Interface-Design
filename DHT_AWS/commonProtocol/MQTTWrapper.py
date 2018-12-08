#reference http://www.steves-internet-guide.com/python-mqtt-publish-subscribe/
import time
import paho.mqtt.client as paho
#broker="broker.hivemq.com"
#broker="iot.eclipse.org"    

class MQTTWrapper():
    def __init__(self, hostname= "gunjshreya", broker="iot.eclipse.org"):
        print ("Creating new instance named:",hostname)
        self.client= paho.Client(hostname)
        self.client.on_message= self.on_message
        self.callbackMap = {}
        print("connecting to broker ",broker)
        self.client.connect(broker)
    
    #define callback
    def on_message(self, client, userdata, message):
        #print("Recv on ",message.topic, " Message:",str(message.payload.decode("utf-8")))
        #print ("Calling callback")
        self.callbackMap[message.topic](self,client,userdata,message)
        print ("Callback called")
        
        
    def subscribe(self, topicName, callback):
        if callback is None or topicName is None:
            print ("Error Subscribe")
            return False
        
        self.callbackMap[topicName] = callback
        print("subscribing to ",topicName)
        self.client.subscribe(topicName)#subscribe
        return True
    
    def publish(self,topicName, message):
        if topicName is None:
            return False
        print("publishing ",message, " to topic:",topicName)
        self.client.publish(topicName,message)#publish
        return True
        
    def disconnect(self):
        self.client.disconnect()
    
    def loopStart(self):
        self.client.loop_start()
    
    def loopStop(self):
        self.client.loop_stop()