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
        
            
        #print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))  

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.dht = DHTUser(22,4)
        self.ui.requestDataButton.clicked.connect(self.updateTempHumUI)
        self.ui.lastRequestTime.setEnabled(False)
    
    def updateTempHumUI(self):
        humidity, temperature = self.dht.read()
        if humidity is not None and temperature is not None:
            self.ui.sensorConnected.setChecked(True)
            self.ui.temperatureLCD.display(temperature)
            self.ui.humidityLCD.display(humidity)
            self.ui.lastRequestTime.setText(str(time.asctime(time.localtime(time.time()))))
            #self.ui.lastRequestTime.setText(str(datetime.datetime.now().time()))
        else:
            self.ui.sensorConnected.setChecked(False)
        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())