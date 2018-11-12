#!/usr/bin/env python3

#reference: https://aws.amazon.com/blogs/iot/how-to-implement-mqtt-with-tls-client-authentication-on-port-443-from-client-devices-python/
from __future__ import print_function
import sys
import ssl
import time
import datetime
import json
import logging, traceback
import paho.mqtt.client as mqtt
from readConfig import AWSConfigReader

AWSConfig = AWSConfigReader(sys.argv)
print ("Keys:", AWSConfig.getConfigItemKeys())
print (AWSConfig.getConfigItem('port'))

IoT_protocol_name = "x-amzn-mqtt-ca"
aws_iot_endpoint = AWSConfig.getConfigItem('host') #"AWS_IoT_ENDPOINT_HERE" # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)

ca = "AWSConfig/certs/"+AWSConfig.getConfigItem('caCert')#"YOUR/ROOT/CA/PATH" 
cert = "AWSConfig/certs/"+AWSConfig.getConfigItem('clientCert')#"YOUR/DEVICE/CERT/PATH"
private = "AWSConfig/certs/"+AWSConfig.getConfigItem('privateKey')#"YOUR/DEVICE/KEY/PATH"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

def ssl_alpn():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

if __name__ == '__main__':
    
    #topic = "rpi/sensordata"
    topic = AWSConfig.getConfigItem('mqttTopic')
    try:
        mqttc = mqtt.Client()
        ssl_context= ssl_alpn()
        mqttc.tls_set_context(context=ssl_context)
        logger.info("start connect")
        mqttc.connect(aws_iot_endpoint, port=AWSConfig.getConfigItem('port'))
        logger.info("connect success")
        mqttc.loop_start()

        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            jsonData = {}
            jsonData["time"] = now
            jsonData["data"] = "Hello From RPI"
            jsonData["sensorVal"] = 10
            logger.info("try to publish:{}".format(jsonData))
            mqttc.publish(topic, json.dumps(jsonData))
            time.sleep(3)
            
    except Exception as e:
        logger.error("exception main()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
            