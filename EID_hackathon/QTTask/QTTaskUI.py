# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTTask.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(562, 467)
        self.loadListData = QtWidgets.QPushButton(Dialog)
        self.loadListData.setGeometry(QtCore.QRect(60, 420, 161, 31))
        self.loadListData.setObjectName("loadListData")
        self.graphData = QtWidgets.QPushButton(Dialog)
        self.graphData.setGeometry(QtCore.QRect(340, 380, 141, 31))
        self.graphData.setObjectName("graphData")
        self.listData = QtWidgets.QTextEdit(Dialog)
        self.listData.setGeometry(QtCore.QRect(10, 20, 271, 381))
        self.listData.setObjectName("listData")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.loadListData.setText(_translate("Dialog", "Load Tuple Data"))
        self.graphData.setText(_translate("Dialog", "Graph Tuple Data"))

