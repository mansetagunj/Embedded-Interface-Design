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
from Configuration_Reader import AWSConfigReader

class AWSMQTTInterface():
    def __init__(self, topicName = "topic/default"): 
        self.AWSConfig = AWSConfigReader("../AWSConfig/configfile.json")
        #print ("Keys:", self.AWSConfig.getConfigItemKeys())
        print ("AWS MQTT Publish on Topic:", self.AWSConfig.getConfigItem('mqttTopic'))

        self.IoT_protocol_name = "x-amzn-mqtt-ca"
        aws_iot_endpoint = self.AWSConfig.getConfigItem('host') #"AWS_IoT_ENDPOINT_HERE" # <random>.iot.<region>.amazonaws.com
        url = "https://{}".format(aws_iot_endpoint)
        
        
        self.topic = self.AWSConfig.getConfigItem('mqttTopic')
        if self.topic is None:
            self.topic = topicName

        #"../AWSConfig/certs/"
        self.ca = self.AWSConfig.getConfigItem('certRelPath')+self.AWSConfig.getConfigItem('caCert')#"YOUR/ROOT/CA/PATH" 
        self.cert = self.AWSConfig.getConfigItem('certRelPath')+self.AWSConfig.getConfigItem('clientCert')#"YOUR/DEVICE/CERT/PATH"
        self.private = self.AWSConfig.getConfigItem('certRelPath')+self.AWSConfig.getConfigItem('privateKey')#"YOUR/DEVICE/KEY/PATH"

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(log_format)
        self.logger.addHandler(handler)
        
        self.mqttc = mqtt.Client()
        self.ssl_context = self.__ssl_alpn()
        self.mqttc.tls_set_context(context=self.ssl_context)
        self.logger.info("start connect")
        self.mqttc.connect(aws_iot_endpoint, port=self.AWSConfig.getConfigItem('port'))
        self.logger.info("connect success")
        self.mqttc.loop_start()
        self.logger.info("AWS Loop start")

    def __ssl_alpn(self):
        try:
            #debug print opnessl version
            self.logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
            ssl_context = ssl.create_default_context()
            ssl_context.set_alpn_protocols([self.IoT_protocol_name])
            ssl_context.load_verify_locations(cafile=self.ca)
            ssl_context.load_cert_chain(certfile=self.cert, keyfile=self.private)
            return  ssl_context
        
        except Exception as e:
            print("exception ssl_alpn()")
            raise e
        
    def publishData(self, jsonData = {}):
        if self.topic is not None and jsonData is not None:
            try:
                self.mqttc.publish(self.topic, json.dumps(jsonData))
            except Exception as e:
                self.logger.error("exception publishData()")
                self.logger.error("e obj:{}".format(vars(e)))
                self.logger.error("message:{}".format(e.message))
                self.traceback.print_exc(file=sys.stdout)
                
    def subscribeData(self, handler = None):
        self.logger.info("TODO: register handler")


if __name__ == '__main__':
    
    # -f pathToConfigFile.json
    AWSMQTT = AWSMQTTInterface()
    while True:
        AWSMQTT.publishData({"testdata":"hello from test", "metadata": 1234})
        time.sleep(3)
