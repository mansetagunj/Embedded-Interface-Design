import time
from MQTTWrapper import MQTTWrapper


def myCallback(mqttObject, client, userdata, message):
    print("publishing to MQTTServerEcho")
    mqttObject.publish("test/MQTTServerEcho","ECHO-- "+str(message.payload.decode("utf-8")))
    
if __name__ == "__main__":
    #testcode
    mqtt = MQTTWrapper("gunjshreya","iot.eclipse.org")
    mqtt.subscribe("test/MQTTClient", myCallback)
    mqtt.loopStart()
    time.sleep(500)
    mqtt.disconnect()
    mqtt.loopStop()
