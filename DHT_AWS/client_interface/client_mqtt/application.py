#!/usr/bin/env python3
#@Author: Shreya Chakraborty
#Project 1 EID-2018
#Professor: Bruce Montgomery


import time
import datetime
import sys
import ast
import json
import matplotlib.pyplot as plt
import matplotlib
import boto3
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from clientUI import Ui_dialog
from login import Ui_login
import csv

sys.path.append('./../../commonProtocol/')
from MQTTWrapper import MQTTWrapper
from websocket import create_connection
import asyncio
from aiocoap import *


class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow,self).__init__()
        self.li = Ui_login()
        self.li.setupUi(self)
        self.li.ok.clicked.connect(self.Login)

#function for login called when pressed 'ok' on login window        
    def Login(self):
        key = self.li.password.text()
        user = self.li.username.text()
        #print(key)
        if key == 'eid' and user == 'shreya' :
            print('Logged in')
            self.accept()
            print('closed')
        elif key == 'eid' and user != 'shreya':
            self.li.username.setText('Wrong Username')
        elif key != 'eid' and user == 'shreya':
            self.li.username.setText('Wrong Password')
        else:
            self.li.username.setText('Wrong User & Password')


class AppWindow(QDialog):
    def __init__(self):
        
        with open('access.csv', 'r') as f:
            reader = csv.reader(f)
            keyList = list(reader)[0]
    
        self.sqs = boto3.client('sqs', region_name = 'us-east-2', aws_access_key_id=keyList[0],aws_secret_access_key=keyList[1])
        keyList = []
        reader = None
        self.qURL='https://sqs.us-east-2.amazonaws.com/114151835583/piSensordata.fifo'
        super(AppWindow,self).__init__()
        self.ui = Ui_dialog()
        self.ui.setupUi(self)
        self.ui.clear_data.clicked.connect(self.cleardata)
        self.ui.req_data.clicked.connect(self.get_queue_data)
        self.ui.c_to_f.clicked.connect(self.convert)
        self.ui.gen_graph.clicked.connect(self.generategraph)
        
        
        
        self.max_t_list=[]
        self.min_t_list=[]
        self.curr_t_list=[]
        self.avg_t_list=[]
        self.max_h_list=[]
        self.min_h_list=[]
        self.curr_h_list=[]
        self.avg_h_list=[]
        self.time_list=[]
        self.unit = "C"
        self.mul = 1
        self.add = 0
        self.num = 0
        self.flag = 0
        self.itemnum = 0
        
        self.testData = ""
        
        #protocol comparsion objects
        #mqtt
        self.mqtt = MQTTWrapper("shreyagunj","iot.eclipse.org")
        self.mqtt.subscribe("test/MQTTServerEcho", self.__myEchoSubscribeCallback)
        
        self.wsclient = create_connection("ws://localhost:8111/ws")
        
        #self.protocolThread = threading.Thread(target=self.__startProtocolLoop)
        #self.protocolThread.daemon = True
        #self.protocolThread.start()
        self.MQTT_timeEnd = 0
        self.MQTT_timeStart = 0
        
        self.Websocket_timeEnd = 0
        self.Websocket_timeStart = 0
        
        self.COAP_timeEnd = 0
        self.COAP_timeStart = 0
        
        self.ui.executeProtocolCompButton.clicked.connect(self.startProtocolComparision)
        self.tableIndex = {'mqttTimeStart': [1,1], 'mqttTimeEnd': [1,2], 'mqttTimeDiff': [1,3],
                           'websocketTimeStart': [2,1], 'websocketTimeEnd': [2,2], 'websocketTimeDiff': [2,3],
                           'coapTimeStart': [3,1], 'coapTimeEnd': [3,2], 'coapTimeDiff': [3,3],
                           }
        
    def __setTableItemMQTT(self, timestart, timeend, timediff):
        self.ui.comparisionTable.setItem(self.tableIndex['mqttTimeStart'][0],self.tableIndex['mqttTimeStart'][1], QTableWidgetItem(str(timestart)))
        self.ui.comparisionTable.setItem(self.tableIndex['mqttTimeEnd'][0],self.tableIndex['mqttTimeEnd'][1], QTableWidgetItem(str(timeend)))
        self.ui.comparisionTable.setItem(self.tableIndex['mqttTimeDiff'][0],self.tableIndex['mqttTimeDiff'][1], QTableWidgetItem(str(timediff)))
        self.ui.comparisionTable.move(self.ui.comparisionTable.x()+1,self.ui.comparisionTable.y())
        self.ui.comparisionTable.move(self.ui.comparisionTable.x()-1,self.ui.comparisionTable.y())
        
    def __setTableItemWebsocket(self, timestart, timeend, timediff):
        self.ui.comparisionTable.setItem(self.tableIndex['websocketTimeStart'][0],self.tableIndex['websocketTimeStart'][1], QTableWidgetItem(str(timestart)))
        self.ui.comparisionTable.setItem(self.tableIndex['websocketTimeEnd'][0],self.tableIndex['websocketTimeEnd'][1], QTableWidgetItem(str(timeend)))
        self.ui.comparisionTable.setItem(self.tableIndex['websocketTimeDiff'][0],self.tableIndex['websocketTimeDiff'][1], QTableWidgetItem(str(timediff)))
        self.ui.comparisionTable.move(self.ui.comparisionTable.x()+1,self.ui.comparisionTable.y())
        self.ui.comparisionTable.move(self.ui.comparisionTable.x()-1,self.ui.comparisionTable.y())
    
    def __setTableItemCoAP(self, timestart, timeend, timediff):
        self.ui.comparisionTable.setItem(self.tableIndex['coapTimeStart'][0],self.tableIndex['coapTimeStart'][1], QTableWidgetItem(str(timestart)))
        self.ui.comparisionTable.setItem(self.tableIndex['coapTimeEnd'][0],self.tableIndex['coapTimeEnd'][1], QTableWidgetItem(str(timeend)))
        self.ui.comparisionTable.setItem(self.tableIndex['coapTimeDiff'][0],self.tableIndex['coapTimeDiff'][1], QTableWidgetItem(str(timediff)))
        self.ui.comparisionTable.move(self.ui.comparisionTable.x()+1,self.ui.comparisionTable.y())
        self.ui.comparisionTable.move(self.ui.comparisionTable.x()-1,self.ui.comparisionTable.y())
        
    async def triggerCoapClient(self):

        context = await Context.create_client_context()
        request = Message(code=PUT, payload=self.testData.encode('UTF-8'), uri="coap://localhost/echo")

        self.COAP_timeStart = time.time()
        response = await context.request(request).response
        self.COAP_timeEnd = time.time()
        #print('COAP Echo Res %s\n%r'%(response.code, response.payload))
        print ("COAP-- Time Start:{0} Time End:{1} Diff:{2}".format(self.COAP_timeStart, self.COAP_timeEnd, str(self.COAP_timeEnd-self.COAP_timeStart)))
        self.__setTableItemCoAP(self.COAP_timeStart, self.COAP_timeEnd, self.COAP_timeEnd - self.COAP_timeStart)
                
    def __myEchoSubscribeCallback(self,mqttObject, client, userdata, message):
        #print ("Recvd Message:",str(message.payload.decode("utf-8")))
        self.MQTT_timeEnd = time.time()
        print ("MQTT -- Time Start:{0} Time End:{1} Diff:{2}".format(self.MQTT_timeStart, self.MQTT_timeEnd, str(self.MQTT_timeEnd-self.MQTT_timeStart)))
        self.__setTableItemMQTT(self.MQTT_timeStart, self.MQTT_timeEnd, (self.MQTT_timeEnd - self.MQTT_timeStart))
        
    def startProtocolComparision(self):
        #mqtt
        self.mqtt.loopStart()
        self.MQTT_timeStart = time.time()
        self.mqtt.publish("test/MQTTClient", self.testData)
        
        #websocket
        self.Websocket_timeStart = time.time()
        self.wsclient.send(self.testData)
        result =  self.wsclient.recv()
        self.Websocket_timeEnd = time.time()
        print ("WEBSOCKET -- Time Start:{0} Time End:{1} Diff:{2}".format(self.Websocket_timeStart, self.Websocket_timeEnd, str(self.Websocket_timeEnd-self.Websocket_timeStart)))
        self.__setTableItemWebsocket(self.Websocket_timeStart, self.Websocket_timeEnd, self.Websocket_timeEnd-self.Websocket_timeStart)
        #coap
        asyncio.get_event_loop().run_until_complete(self.triggerCoapClient())
        
    def get_queue_data(self):
        print("in the get queue function")
        # Receiving message from SQS queue
        #for i in range(3):
        count = 0
        displayString = ""
        itemnum = 1
        while(count< 3):
            getData = self.sqs.receive_message(QueueUrl=self.qURL , MaxNumberOfMessages=10)
            #print ("getlist: ", getlist)
            if getData is None or 'Messages' not in getData:
                print("No Messages Available. Count:" +format(count - 1))
                break
            
            # Process messages by printing out body
            list_of_values = []
            for queuedata in getData['Messages']:
                list_of_values.append(queuedata['Body'])
                # delete  the msg once retrived
                self.sqs.delete_message(QueueUrl=self.qURL,ReceiptHandle=queuedata['ReceiptHandle'])
            # Sorting individual data based on key
            #print("data comes below i")
            if list_of_values:
                for datastring in list_of_values: #please use these keys
                    data = json.loads(datastring)
                    self.curr_t_list.append(data["temperature"])
                    self.curr_h_list.append(data["humidity"])
                    self.max_t_list.append(data["maxT"])
                    self.max_h_list.append(data["maxH"])
                    self.min_t_list.append(data["minT"])
                    self.min_h_list.append(data["minH"])
                    self.avg_t_list.append(data["avgT"])
                    self.avg_h_list.append(data["avgH"])
                    self.time_list.append(data["timestamp"])
            else:
                self.ui.display_values.setText("Error Fetching Data from the Queue \n")
                break
                    #itemnum += 1
            #print(count)
            count = count + 1
            #print("count", count)
            
         #for priniting the values we use zip -Iterate over multiple lists in parallel
        for curr_t,avg_t,max_t,min_t,curr_h,avg_h,max_h,min_h,time_t in zip(self.curr_t_list,self.avg_t_list,self.max_t_list, self.min_t_list, self.curr_h_list, self.avg_h_list, self.max_h_list, self.min_h_list,self.time_list):      
        
            displayString += "Item Number : " +str(itemnum)+ "\n" + \
                        "Present Temperature: {0:.2f}".format((float(curr_t) *self.mul) + self.add)+ " " + self.unit + "\n" + \
                       "Avg Temperature: {0:.2f}".format((float(avg_t) *self.mul)+ self.add) + " " + self.unit + "\n" + \
                       "Max Temperature: {0:.2f}".format((float(max_t) *self.mul)+ self.add) + " " + self.unit + "\n" + \
                       "Min Temperature: {0:.2f}".format((float(min_t) *self.mul)+ self.add) + " " + self.unit + "\n"+ \
                       "Present Humidity: {0:0.1f}%".format(float(curr_h)) + "\n" + \
                       "Avg Humidity: {0:0.1f}%".format(float(avg_h)) + "\n" + \
                       "Max Humidity: {0:0.1f}%".format(float(max_h))+ "\n" + \
                       "Min Humidity: {0:0.1f}%".format(float(min_h)) + "\n" + \
                       "Timestamp: "+ str(time_t) + " \n\n"
            itemnum += 1
            
                
        self.ui.display_values.setText("Number of items fetched from Queue :" + str(itemnum-1) + "/30" + "\n" + "Queue Data is as follows:\n"  + displayString )
        self.testData = displayString
        
    def generategraph(self):
        f = plt.figure(1)
        #dummy_list = [1,2,3,4,5]
        xRange = len(self.curr_t_list) + 1
        plt.xticks(range(1,xRange))
        plt.plot(range(1,xRange), self.curr_t_list, 'y-', label='Present Temperature')
        plt.plot(range(1,xRange), self.avg_t_list, 'g-', label='Average Temperature')
        plt.plot(range(1,xRange), self.max_t_list, 'b-', label='Max Temperature')
        plt.plot(range(1,xRange), self.min_t_list, 'r-', label='Min Temperature')
        plt.legend(loc='best')
        plt.title('Temperature Analysis Graph' + '\nStart Timestamp:' + self.time_list[0] + '\nEnd Timestamp:' + self.time_list[len(self.time_list)-1])
        plt.ylabel('Temperature in C')
        plt.xlabel('Number of Items Retrieved')
        
        g = plt.figure(2)
        xRange = len(self.curr_h_list) + 1
        plt.xticks(range(1,xRange))
        plt.plot(range(1,xRange), self.curr_h_list, 'y-', label='Present Humidity')
        plt.plot(range(1,xRange), self.avg_h_list, 'g-', label='Average Humidity')
        plt.plot(range(1,xRange), self.max_h_list, 'b-', label='Max Humidity')
        plt.plot(range(1,xRange), self.min_h_list, 'r-', label='Min Humidity')
        plt.legend(loc='best')
        plt.title('Humidity Analysis Graph' + '\nStart Timestamp:' + self.time_list[0] + '\nEnd Timestamp:' + self.time_list[len(self.time_list)-1])
        plt.ylabel('Humidity %' )
        plt.xlabel('Number of Items Retrieved')
        
        plt.show()
        
        
    def convert(self):
        print("convert clicked filling units")
        if self.flag == 0: #celcius
            self.mul = 1
            self.add = 0
            self.unit = " C"
            self.flag = 1
            print("celcius")
        else:
            self.mul = 1.8
            self.add = 32
            self.unit = " F"
            self.flag = 0
            print("farenheit")
            
    def cleardata(self):
        self.max_t_list=[]
        self.min_t_list=[]
        self.curr_t_list=[]
        self.avg_t_list=[]
        self.max_h_list=[]
        self.min_h_list=[]
        self.curr_h_list=[]
        self.avg_h_list=[]
        self.time_list=[]
        self.ui.display_values.clear()
        self.testData = ""
                           
if __name__ == '__main__':
    app = QApplication(sys.argv)
    log = LoginWindow()
    if log.exec_() == QtWidgets.QDialog.Accepted: #reference -https://stackoverflow.com/questions/11812000/login-dialog-pyqt
       w = AppWindow()
       a=w.show()
       sys.exit(app.exec_())
