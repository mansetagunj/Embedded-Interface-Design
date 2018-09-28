#!/usr/bin/env python3
import sys
#import datetime
import time
#sys.path.append("/home/pi/gunjproject/AdafruitLib/Adafruit_Python_DHT") 
import Adafruit_DHT
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtCore
from DHT_UI import Ui_Dialog
from threading import Timer

class DHTUser():
    _pin = None
    _sensorType = None
    def __init__(self, sensorType, pin):
        self._pin = pin
        self._sensorType = sensorType
        
    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(self._sensorType, self._pin)
        return humidity, temperature 

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.dht = DHTUser(22,4)
        self.tempUnit = 0  # 0 - Celcius and 1 - Fahrenheit Start with Celcius state
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
        
    def startTimerEvent(self):
        print ("Start Timer")
        self.ui.stopTimerButton.setEnabled(True)
        self.ui.startTimerButton.setEnabled(False)
        self.ui.requestDataButton.setEnabled(False)
        print ("Timer value:" + str(self.ui.timerResolutionSpinBox.value()))
        #self.readingsTimer = Timer(self.ui.timerResolutionSpinBox.value(), self.updateTempHumUI)
        self.now = 0
        self.readingsTimer.start(self.ui.timerResolutionSpinBox.value()*1000)
    
    def timerTickEvent(self):
        self.now += 1
        self.updateTempHumUI()
        
    def stopTimerEvent(self):
        print ("Stop Timer")
        self.readingsTimer.stop()
        self.ui.stopTimerButton.setEnabled(False)
        self.ui.startTimerButton.setEnabled(True)
        self.ui.requestDataButton.setEnabled(True)
        
    def updateTimerEvent(self):
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

    def setTempFahrenheit(self):
        if self.tempUnit == 0:  #if in C state
            self.tempUnit = 1   ##changing back to Fah state
            self.updateSensorReadingsUIElement(self.ui.humidityLCD.value(), self.ui.temperatureLCD.value())
            self.ui.FtempButton.setEnabled(False)
            self.ui.CtempButton.setEnabled(True)

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
        
    
    def updateTempHumUI(self):
        print ("Request Data")
        humidity, temperature = self.dht.read()
        if humidity is not None and temperature is not None:
            self.ui.sensorStatus.setText("Sensor Connected");
            self.ui.sensorStatus.setStyleSheet("QLabel { background-color : green; color : white; }");
            self.updateSensorReadingsUIElement(humidity, temperature)
            self.ui.lastRequestTime.setText(str(time.asctime(time.localtime(time.time()))))
        else:
            self.ui.sensorStatus.setText("Sensor Disconnected");
            self.ui.sensorStatus.setStyleSheet("QLabel { background-color : red; color : white; }")
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())