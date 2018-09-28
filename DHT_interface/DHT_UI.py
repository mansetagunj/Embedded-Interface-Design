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
        self.temperatureLCD.setGeometry(QtCore.QRect(50, 110, 181, 111))
        self.temperatureLCD.setObjectName("temperatureLCD")
        self.humidityLCD = QtWidgets.QLCDNumber(Dialog)
        self.humidityLCD.setGeometry(QtCore.QRect(560, 110, 181, 111))
        self.humidityLCD.setObjectName("humidityLCD")
        self.requestDataButton = QtWidgets.QPushButton(Dialog)
        self.requestDataButton.setGeometry(QtCore.QRect(290, 230, 191, 171))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.requestDataButton.setFont(font)
        self.requestDataButton.setObjectName("requestDataButton")
        self.lastRequestTime = QtWidgets.QLabel(Dialog)
        self.lastRequestTime.setEnabled(True)
        self.lastRequestTime.setGeometry(QtCore.QRect(270, 160, 251, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lastRequestTime.setFont(font)
        self.lastRequestTime.setToolTip("")
        self.lastRequestTime.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lastRequestTime.setAutoFillBackground(False)
        self.lastRequestTime.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lastRequestTime.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lastRequestTime.setLineWidth(1)
        self.lastRequestTime.setAlignment(QtCore.Qt.AlignCenter)
        self.lastRequestTime.setIndent(-1)
        self.lastRequestTime.setObjectName("lastRequestTime")
        self.temperatureIconLabel = QtWidgets.QLabel(Dialog)
        self.temperatureIconLabel.setGeometry(QtCore.QRect(80, 220, 141, 151))
        self.temperatureIconLabel.setText("")
        self.temperatureIconLabel.setPixmap(QtGui.QPixmap("Resources/temp1.png"))
        self.temperatureIconLabel.setObjectName("temperatureIconLabel")
        self.humidityIconLabel = QtWidgets.QLabel(Dialog)
        self.humidityIconLabel.setGeometry(QtCore.QRect(590, 220, 141, 151))
        self.humidityIconLabel.setText("")
        self.humidityIconLabel.setPixmap(QtGui.QPixmap("Resources/hum.png"))
        self.humidityIconLabel.setObjectName("humidityIconLabel")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(240, 20, 20, 571))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(530, 20, 20, 571))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.sensorStatus = QtWidgets.QLabel(Dialog)
        self.sensorStatus.setGeometry(QtCore.QRect(320, 80, 161, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.sensorStatus.setFont(font)
        self.sensorStatus.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sensorStatus.setStyleSheet("QLabel { background-color : red; color : white; }")
        self.sensorStatus.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sensorStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.sensorStatus.setObjectName("sensorStatus")
        self.stopTimerButton = QtWidgets.QPushButton(Dialog)
        self.stopTimerButton.setGeometry(QtCore.QRect(410, 520, 101, 61))
        self.stopTimerButton.setObjectName("stopTimerButton")
        self.startTimerButton = QtWidgets.QPushButton(Dialog)
        self.startTimerButton.setGeometry(QtCore.QRect(280, 520, 101, 61))
        self.startTimerButton.setObjectName("startTimerButton")
        self.timerResolutionSpinBox = QtWidgets.QSpinBox(Dialog)
        self.timerResolutionSpinBox.setGeometry(QtCore.QRect(400, 450, 91, 41))
        self.timerResolutionSpinBox.setMinimum(1)
        self.timerResolutionSpinBox.setMaximum(10)
        self.timerResolutionSpinBox.setObjectName("timerResolutionSpinBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(270, 460, 131, 31))
        self.label.setObjectName("label")
        self.CtempButton = QtWidgets.QPushButton(Dialog)
        self.CtempButton.setGeometry(QtCore.QRect(50, 50, 51, 51))
        self.CtempButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../Downloads/celsius.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.CtempButton.setIcon(icon)
        self.CtempButton.setIconSize(QtCore.QSize(100, 100))
        self.CtempButton.setObjectName("CtempButton")
        self.FtempButton = QtWidgets.QPushButton(Dialog)
        self.FtempButton.setGeometry(QtCore.QRect(100, 50, 51, 51))
        self.FtempButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Resources/farh.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.FtempButton.setIcon(icon1)
        self.FtempButton.setIconSize(QtCore.QSize(100, 100))
        self.FtempButton.setObjectName("FtempButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.requestDataButton.setText(_translate("Dialog", "Request Data"))
        self.lastRequestTime.setText(_translate("Dialog", "Last Request Time"))
        self.sensorStatus.setText(_translate("Dialog", "Sensor Disconnected"))
        self.stopTimerButton.setText(_translate("Dialog", "Stop Timer"))
        self.startTimerButton.setText(_translate("Dialog", "Start Timer"))
        self.label.setText(_translate("Dialog", "Timer Resolution"))

