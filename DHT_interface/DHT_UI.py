# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DHT_interface.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 604)
        self.temperatureLCD = QtWidgets.QLCDNumber(Dialog)
        self.temperatureLCD.setGeometry(QtCore.QRect(50, 120, 181, 111))
        self.temperatureLCD.setObjectName("temperatureLCD")
        self.humidityLCD = QtWidgets.QLCDNumber(Dialog)
        self.humidityLCD.setGeometry(QtCore.QRect(530, 120, 181, 111))
        self.humidityLCD.setObjectName("humidityLCD")
        self.requestDataButton = QtWidgets.QPushButton(Dialog)
        self.requestDataButton.setGeometry(QtCore.QRect(300, 230, 151, 81))
        self.requestDataButton.setObjectName("requestDataButton")
        self.lastRequestTime = QtWidgets.QLabel(Dialog)
        self.lastRequestTime.setGeometry(QtCore.QRect(260, 110, 251, 91))
        self.lastRequestTime.setToolTip("")
        self.lastRequestTime.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lastRequestTime.setAutoFillBackground(False)
        self.lastRequestTime.setFrameShape(QtWidgets.QFrame.Box)
        self.lastRequestTime.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lastRequestTime.setLineWidth(1)
        self.lastRequestTime.setIndent(-1)
        self.lastRequestTime.setObjectName("lastRequestTime")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(100, 240, 101, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(590, 240, 91, 31))
        self.label_3.setObjectName("label_3")
        self.sensorConnected = QtWidgets.QCheckBox(Dialog)
        self.sensorConnected.setGeometry(QtCore.QRect(310, 30, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.sensorConnected.setFont(font)
        self.sensorConnected.setObjectName("sensorConnected")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.requestDataButton.setText(_translate("Dialog", "Request Data"))
        self.lastRequestTime.setText(_translate("Dialog", "Last Request Time"))
        self.label_2.setText(_translate("Dialog", "Temperature"))
        self.label_3.setText(_translate("Dialog", "Humidity"))
        self.sensorConnected.setText(_translate("Dialog", "Sensor Connected"))

