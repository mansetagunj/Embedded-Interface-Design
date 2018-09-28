#!/usr/bin/env python3
import sys
#import datetime
import time
#sys.path.append("/home/pi/gunjproject/AdafruitLib/Adafruit_Python_DHT") 
import Adafruit_DHT
from PyQt5.QtWidgets import QApplication, QDialog
from DHT_UI import Ui_Dialog

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
        self.ui.CtempButton.setEnabled(False)
        
    def setTempCelcius():
        if (self.tempUnit == 1):  #if in Fah state
            self.tempUnit = 0   ##changing back to Celcius state
            #updateSensorReadingsUIElement(humidity, convertTemp(self.ui.temperatureLCD.value(), False))
            self.ui.FtempButton.setEnabled(True)
            self.ui.CtempButton.setEnabled(False)

    def setTempFahrenheit():
        if (self.tempUnit == 0):  #if in C state
            print ("In click Fah, tempunit to 1")
            self.tempUnit = 1   ##changing back to Fah state
            #updateSensorReadingsUIElement(humidity, convertTemp(self.ui.temperatureLCD.value(), True))
            self.ui.FtempButton.setEnabled(False)
            self.ui.CtempButton.setEnabled(True)

    def convertTemp(tempVal, toCelcius):
        if(toCelcius):
            return ((tempVal - 32)*(5/9))
        else:
            return ((tempVal * (9/5)) + 32)
        
    def updateSensorReadingsUIElement(humidity, temperature):
        if(self.tempUnit == 1):  ## we need temp values in F
            temperature = convertTemp(tempVal, False)   
        self.ui.temperatureLCD.display("{:.1f}".format(temperature))   
        self.ui.humidityLCD.display("{:.1f}".format(humidity))
        
    
    def updateTempHumUI(self):
        humidity, temperature = self.dht.read()
        if humidity is not None and temperature is not None:
            self.ui.sensorStatus.setText("Sensor Connected");
            self.ui.sensorStatus.setStyleSheet("QLabel { background-color : green; color : white; }");
            #updateUISensorReadings(humidity, temperature)
            if(self.tempUnit == 1):  ## we need temp values in F
                temperature = convertTemp(tempVal, False)   
            self.ui.temperatureLCD.display("{:.1f}".format(temperature))   
            self.ui.humidityLCD.display("{:.1f}".format(humidity))
            self.ui.lastRequestTime.setText(str(time.asctime(time.localtime(time.time()))))
        else:
            self.ui.sensorStatus.setText("Sensor Disconnected");
            self.ui.sensorStatus.setStyleSheet("QLabel { background-color : red; color : white; }")
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())