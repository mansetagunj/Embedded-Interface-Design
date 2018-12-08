import time
from MQTTWrapper import MQTTWrapper

global MQTT_timeStart, MQTT_timeEnd

def myCallback(mqttObject, client, userdata, message):
    print ("Recvd Message:",str(message.payload.decode("utf-8")))
    MQTT_timeEnd = time.time()
    print ("Time Start:{0} Time End:{1} Diff:{2}".format(MQTT_timeStart, MQTT_timeEnd, str(MQTT_timeEnd-MQTT_timeStart)))
    
if __name__ == "__main__":
    #testcode
    mqtt = MQTTWrapper("shreyagunj", "iot.eclipse.org")
    mqtt.loopStart()
    mqtt.subscribe("test/MQTTServerEcho", myCallback)
    for i in range(3):
        
        MQTT_timeStart = time.time()
        mqtt.publish("test/MQTTClient", "Hello "+ str(i)+" from Client")
        time.sleep(2)
    
    mqtt.disconnect()
    mqtt.loopStop()