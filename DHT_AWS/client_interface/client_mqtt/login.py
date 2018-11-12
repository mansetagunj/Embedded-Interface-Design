# Author: Shreya Chakraborty
# generated from login.ui using the command : pyuic5 login.ui > login.py
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(472, 343)
        self.centralwidget = QtWidgets.QWidget(login)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 170, 191, 21))
        self.label.setObjectName("label")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(250, 160, 181, 33))
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.ok = QtWidgets.QPushButton(self.centralwidget)
        self.ok.setGeometry(QtCore.QRect(180, 240, 101, 31))
        self.ok.setObjectName("ok")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 110, 121, 21))
        self.label_2.setObjectName("label_2")
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(250, 110, 181, 29))
        self.username.setObjectName("username")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(190, 40, 67, 21))
        self.label_3.setObjectName("label_3")
        #login.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(login)
        self.statusbar.setObjectName("statusbar")
        #login.setStatusBar(self.statusbar)

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "LOGIN WINDOW"))
        self.label.setText(_translate("login", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">PASSWORD:</span></p></body></html>"))
        self.ok.setText(_translate("login", "OK"))
        self.label_2.setText(_translate("login", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">USERNAME:</span></p></body></html>"))
        self.label_3.setText(_translate("login", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">LOGIN</span></p></body></html>"))

