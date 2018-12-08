#!/usr/bin/env python3

## Author - Gunj Manseta
## University of Colorado Boulder

import sys
import time
import Adafruit_DHT
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtCore
from DHT_UI import Ui_Dialog
from threading import Timer
import threading
from math import ceil
from GraphPlotter import RealTimePlotter
import datetime
import matplotlib.pyplot as plt
import platform
from database import Database
from DHTServer import DHTWebserver
from AWS_interface import AWSMQTTInterface

sys.path.append('./../commonProtocol/')
from MQTTWrapper import MQTTWrapper

#Class abstraction over the DHT sensor Adafruit class
class DHTUser():
    _pin = None
    _sensorType = None
    def __init__(self, sensorType, pin):
        self._pin = pin
        self._sensorType = sensorType
        self.DHTAvail = 1
        print ("Machine:" + platform.machine())
        if 'i686' in platform.machine():
            print("Running on Pi VM")
            self.DHTAvail = 0
        
    def read(self):
        if(self.DHTAvail):
            humidity, temperature = Adafruit_DHT.read_retry(self._sensorType, self._pin)
        else:
            humidity = 41.41
            temperature = 25.25

        return humidity, temperature 

## the actual application class
class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.dht = DHTUser(22,4)
        self.tempUnit = 0  # 0 - Celcius and 1 - Fahrenheit Start with Celcius state
        
        ##database object
        self.db = Database()
        self.db.start()
        
        self.minT = 0
        self.maxT = 0
        self.minH = 0
        self.maxH = 0
        self.readingCount = 0
        
        self.ui.todaysDateLabel.setText(datetime.datetime.now().strftime("%d %b, %Y"))
        self.TempthresholdUpdateEvent()
        self.HumthresholdUpdateEvent()
        self.ui.requestDataButton.clicked.connect(self.updateTempHumUI)
        self.ui.CtempButton.clicked.connect(self.setTempCelcius)
        self.ui.FtempButton.clicked.connect(self.setTempFahrenheit)
        
        self.ui.timerResolutionSpinBox.valueChanged.connect(self.updateTimerEvent)
        self.ui.startTimerButton.clicked.connect(self.startTimerEvent)
        self.ui.stopTimerButton.clicked.connect(self.stopTimerEvent)
        self.ui.stopTimerButton.setEnabled(False)
        self.ui.CtempButton.setEnabled(False)
        self.readingsTimer = QtCore.QTimer()
        self.readingsTimer.timeout.connect(self.timerTickEvent)
        self.now = 0
        
        self.ui.tempUnitThresholdDisplaySlider.valueChanged.connect(self.TempthresholdUpdateEvent)
        self.ui.humUnitThresholdDisplaySlider.valueChanged.connect(self.HumthresholdUpdateEvent)
        self.realTimePlotter = RealTimePlotter()
        self.tempList = [];
        self.humList = [];
        self.ui.staticGraphButton.clicked.connect(self.openStaticGraph)
        self.ui.clearReadingsButton.clicked.connect(self.clearStoredReadings)
        
        
        self.AWSMQTT = AWSMQTTInterface()
        
        self.pushreadingsTimer = QtCore.QTimer()
        self.pushreadingsTimer.timeout.connect(self.__takeReadings)
        self.pushreadingsTimer.start(5000) #5sec timer
        
        #webserver
        self.server = DHTWebserver(self.db, True)
        self.server.start()
        
        #protocol comparsion objects
        #mqtt
        self.mqtt = MQTTWrapper("gunjshreya","iot.eclipse.org")
        self.mqtt.subscribe("test/MQTTClient", self.__myMQTTSubCallback)
        self.protocolThread = threading.Thread(target=self.__startProtocolLoop)
        self.protocolThread.daemon = True
        self.protocolThread.start()
        
        
    def __startProtocolLoop(self):
        self.mqtt.loopStart()
        
        
    def __myMQTTSubCallback(self, mqttObject, client, userdatta, message):
        print("publishing to MQTTServerEcho")
        #mqttObject.publish("test/MQTTServerEcho","ECHO-- "+str(message.payload.decode("utf-8")))
        mqttObject.publish("test/MQTTServerEcho", message.payload)
    
    def __takeReadings(self):
        humidity, temperature = self.dht.read()
        if humidity is not None and temperature is not None:
            self.__setSensorStatus(True)
            self.updateTempHumUIElem(humidity, temperature)
            self.updateTempHumExtraUIElem(humidity, temperature)
            timestamp = datetime.datetime.now().strftime("%x:%X")
            #humidity = "{0:.2f}".format(humidity)
            #temperature = "{0:.2f}".format(temperature)
            self.__updateDBEvent(timestamp, humidity, temperature)
            self.__awsPushData(timestamp, humidity,temperature)
            #print ("Get DB:",self.db.getLatestData(1))
        else:
            print ("ERROR SENSOR DISCONNECTED")
            self.__setSensorStatus(False)
        
    def __awsPushData(self, timestamp, humidity,temperature):
        if humidity is not None and temperature is not None:
            jsonDataPacket = {}
            jsonDataPacket['timestamp'] = timestamp
            jsonDataPacket['humidity'] = humidity
            jsonDataPacket['temperature'] = temperature
            self.AWSMQTT.publishData(jsonDataPacket)
        
    def __updateDBEvent(self, timestamp, humidity, temperature):
        if humidity is not None and temperature is not None:
            #data = [datetime.datetime.now().strftime("%x:%X"),"{0:.2f}".format(temperature),"{0:.2f}".format(humidity)]
            data = [timestamp,round(temperature,2),round(humidity,2)]
            self.db.putData(data)
            #print ("DB Data:",data)
            self.__setSensorStatus(True)
        else:
            self.__setSensorStatus(False)
        
        
    def openStaticGraph(self):
        self.realTimePlotter.plotStatic(self.tempList, self.humList)
    
    def clearStoredReadings(self):
        self.tempList.clear()
        self.humList.clear()
        
    def TempthresholdUpdateEvent(self):
        self.ui.tempValueThresholdDisplayLabel.setText(str(self.ui.tempUnitThresholdDisplaySlider.value()))

    def HumthresholdUpdateEvent(self):
        self.ui.humValueThresholdDisplayLabel.setText(str(self.ui.humUnitThresholdDisplaySlider.value()))

    def startTimerEvent(self):
        print ("Start Timer")
        self.ui.stopTimerButton.setEnabled(True)
        self.ui.startTimerButton.setEnabled(False)
        self.ui.requestDataButton.setEnabled(False)
        #print ("Timer value:" + str(self.ui.timerResolutionSpinBox.value()))
        self.now = 0
        if self.ui.realtimeGraphTimerCheckbox.isChecked() is True:
            self.realTimePlotter.startPlotter()
        self.readingsTimer.start(self.ui.timerResolutionSpinBox.value()*1000)
    
    def timerTickEvent(self):
        self.now += 1
        humidity, temperature = self.updateTempHumUI()
        if self.realTimePlotter.isPlotterRunning() is True:
            self.realTimePlotter.putData([humidity,temperature])
        
    def stopTimerEvent(self):
        print ("Stop Timer")
        self.readingsTimer.stop()
        if self.realTimePlotter.isPlotterRunning() is True:
            self.realTimePlotter.stopPlotter()
        self.ui.stopTimerButton.setEnabled(False)
        self.ui.startTimerButton.setEnabled(True)
        self.ui.requestDataButton.setEnabled(True)
        
    def updateTimerEvent(self):
        if self.readingsTimer.isActive() is True:
            self.readingsTimer.stop()
            self.now = 0
            print ("Updated Timer value:" + str(self.ui.timerResolutionSpinBox.value()))
            self.readingsTimer.start(self.ui.timerResolutionSpinBox.value()*1000)
        
    def setTempCelcius(self):
        if (self.tempUnit == 1):  #if in Fah state
            self.tempUnit = 0   ##changing back to Celcius state
            self.updateSensorReadingsUIElement(self.ui.humidityLCD.value(), self.convertTemp(self.ui.temperatureLCD.value(), True))
            self.ui.FtempButton.setEnabled(True)
            self.ui.CtempButton.setEnabled(False)
            
            ##updating the threshold related UI elements
            newTh = self.convertTemp(self.ui.tempUnitThresholdDisplaySlider.value(), True)
            self.ui.tempUnitThresholdDisplaySlider.setMinimum(-15)
            self.ui.tempUnitThresholdDisplaySlider.setMaximum(60)
            self.ui.tempUnitThresholdDisplaySlider.setValue(ceil(newTh))
            self.ui.tempValueThresholdDisplayLabel.setText(str(ceil(newTh)))
            self.ui.tempUnitThresholdDisplayLabel.setText("C")

    def setTempFahrenheit(self):
        if self.tempUnit == 0:  #if in C state
            self.tempUnit = 1   ##changing back to Fah state
            self.updateSensorReadingsUIElement(self.ui.humidityLCD.value(), self.ui.temperatureLCD.value())
            self.ui.FtempButton.setEnabled(False)
            self.ui.CtempButton.setEnabled(True)
            
            ##updating the threshold related UI elements
            newTh = self.convertTemp(self.ui.tempUnitThresholdDisplaySlider.value(), False)
            self.ui.tempUnitThresholdDisplaySlider.setMinimum(5)
            self.ui.tempUnitThresholdDisplaySlider.setMaximum(120)
            self.ui.tempUnitThresholdDisplaySlider.setValue(ceil(newTh))
            self.ui.tempValueThresholdDisplayLabel.setText(str(ceil(newTh)))
            self.ui.tempUnitThresholdDisplayLabel.setText("F")

    def convertTemp(self, tempVal, toCelcius):
        if toCelcius == True:
            return ((tempVal - 32)*(5/9))
        else:
            return ((tempVal * (9/5)) + 32)
        
    def updateSensorReadingsUIElement(self, humidity, temperature):
        if self.tempUnit == 1:  ## we need temp values in F
            temperature = self.convertTemp(temperature, False)   
        self.ui.temperatureLCD.display("{:.1f}".format(temperature))   
        self.ui.humidityLCD.display("{:.1f}".format(humidity))
        
    def updateAlarm(self, humidity, temperature):
        if(self.tempUnit == 1):
            temperature = self.convertTemp(temperature, False)
            
        ##print ("Read: hum {}, temp {} -- th h {} t {}",humidity, temperature, self.ui.humUnitThresholdDisplaySlider.value(), self.ui.tempUnitThresholdDisplaySlider.value())
        if(humidity > self.ui.humUnitThresholdDisplaySlider.value()):
            self.ui.humThresholdAlarm.setStyleSheet("QLabel { background-color : red; color : white; }");
        else:
            self.ui.humThresholdAlarm.setStyleSheet("QLabel { background-color : none; color : white; }");
            
        if(temperature > self.ui.tempUnitThresholdDisplaySlider.value()):
            self.ui.tempThresholdAlarm.setStyleSheet("QLabel { background-color : red; color : white; }");
        else:
            self.ui.tempThresholdAlarm.setStyleSheet("QLabel { background-color : none; color : white; }");

    def __setSensorStatus(self, isConnected = True):
        if isConnected:
            self.ui.sensorStatus.setText("Sensor Connected");
            self.ui.sensorStatus.setStyleSheet("QLabel { background-color : green; color : white; }");
        else:
            self.ui.sensorStatus.setText("Sensor Disconnected");
            self.ui.sensorStatus.setStyleSheet("QLabel { background-color : red; color : white; }")
            
            
    def updateTempHumUI(self):
        print ("Request Data")
        #humidity, temperature = self.dht.read()
        #self.updateTempHumUIElem(humidity, temperature)
        #self.updateTempHumExtraUIElem(humidity, temperature)
        
    def updateTempHumExtraUIElem(self, humidity, temperature):
        if temperature is not None and humidity is not None:
            if self.readingCount is 0:
                self.minT = temperature
                self.minH = humidity
                self.maxT = temperature
                self.maxH = humidity
                self.avgT = temperature
                self.avgH = humidity
                
            self.minT = min(self.minT, temperature)
            self.maxT = max(self.maxT, temperature)
            self.minH = min(self.minH, humidity)
            self.maxH = max(self.maxH, humidity)
            
            #print ("Count:",self.readingCount," Curr H:",humidity, " Before AVG H:", self.avgH)
            self.avgT = round((((self.avgT*self.readingCount) + temperature) / (self.readingCount + 1)),2)
            self.avgH = round((((self.avgH*self.readingCount) + humidity) / (self.readingCount + 1)),2)
            #print ("Count:",self.readingCount," Curr H:",humidity, " After AVG H:", self.avgH)
            
            self.readingCount += 1
            
              
            if self.tempUnit == 1:  ## we need temp values in F
                self.ui.avgtemperatureLCD.display("{0:.2f}".format(self.convertTemp(self.avgT, False)))   
                self.ui.mintemperatureLCD.display("{0:.2f}".format(self.convertTemp(self.minT, False)))
                self.ui.maxtemperatureLCD.display("{0:.2f}".format(self.convertTemp(self.maxT, False)))
            else:
                self.ui.avgtemperatureLCD.display("{0:.2f}".format(self.avgT))  
                self.ui.mintemperatureLCD.display("{0:.2f}".format(self.minT))
                self.ui.maxtemperatureLCD.display("{0:.2f}".format(self.maxT))
                
            self.ui.avghumidityLCD.display("{0:.2f}".format(self.avgH))
            self.ui.minhumidityLCD.display("{0:.2f}".format(self.minH))  
            self.ui.maxhumidityLCD.display("{0:.2f}".format(self.maxH))
        
        
    def updateTempHumUIElem(self,humidity, temperature):
        if humidity is not None and temperature is not None:
            self.tempList.append(temperature)
            self.humList.append(humidity)
            self.updateAlarm(humidity, temperature)
            self.__setSensorStatus(True)
            self.updateSensorReadingsUIElement(humidity, temperature)
            self.ui.lastRequestTime.setText(datetime.datetime.now().strftime("%X"))
            return humidity,  temperature
        else:
            self.__setSensorStatus(False)
            return 0, 0
        
    def closeEvent(self, event):
        print ("Application closing. Cleaning up resources")
        self.pushreadingsTimer.stop()
        self.readingsTimer.stop()
        
        self.mqtt.disconnect()
        self.mqtt.loopStop()
        
        self.server.stop()
        #self.server.join()
        self.db.stopThread()
        #self.db.join()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

