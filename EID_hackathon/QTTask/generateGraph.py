#!/usr/bin/env python3
import time
import datetime
import sys
import ast
import json
import matplotlib.pyplot as plt
import matplotlib
import csv       
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtCore
from QTTaskUI import Ui_Dialog
from math import ceil

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #self.ui.listDataElement.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.loadListData.clicked.connect(self.loadListDataFunc)
        self.ui.graphData.clicked.connect(self.showgraphData)
        self.plot1X = []
        self.plot2X = []
        self.plot3X = []
        self.plot4X = []
        self.plot1Y = []
        self.plot2Y = []
        self.plot3Y = []
        self.plot4Y = []

    def loadListDataFunc(self):
        self.plot1X = []
        self.plot2X = []
        self.plot3X = []
        self.plot4X = []
        self.plot1Y = []
        self.plot2Y = []
        self.plot3Y = []
        self.plot4Y = []
        #print (self.ui.listData.toPlainText())
        datalist = self.ui.listData.toPlainText().split('\n')
        print ("Datalist:",datalist)
        newDatalist = []
        
        for ellist in datalist:
            #print("List:",ellist)
            
            newDatalist = ellist.split(",")
            newDatalist = [int(i) for i in newDatalist]
            print ("List:",newDatalist)
            if newDatalist[0] is 1:
                self.plot1X.append(newDatalist[2])
                self.plot1Y.append(newDatalist[3])
            elif newDatalist[0] is 2:
                self.plot2X.append(newDatalist[2])
                self.plot2Y.append(newDatalist[3])
            elif newDatalist[0] is 3:
                self.plot3X.append(newDatalist[2])
                self.plot3Y.append(newDatalist[3])
            elif newDatalist[0] is 4:
                self.plot4X.append(newDatalist[2])
                self.plot4Y.append(newDatalist[3])
        
        print ("Plot1X:",self.plot1X)
        print ("Plot1Y:",self.plot1Y)
        print ("Plot2X:",self.plot2X)
        print ("Plot2Y:",self.plot2Y)
        print ("Plot3X:",self.plot3X)
        print ("Plot3Y:",self.plot3Y)
        print ("Plot4X:",self.plot4X)
        print ("Plot4Y:",self.plot4Y)
        
        
    def showgraphData(self):
        print("Show graph")
        f = plt.figure(1)
        plt.xticks(self.plot1X)
        plt.plot(self.plot1X, self.plot1Y, 'y-', label='Line1')
        plt.plot(self.plot2X, self.plot2Y, 'r-', label='Line2')
        plt.plot(self.plot3X, self.plot3Y, 'g-', label='Line3')
        plt.plot(self.plot4X, self.plot4Y, 'b-', label='Line4')
        plt.legend(loc='best')
        plt.title('Graph')
        plt.ylabel('Y')
        plt.xlabel('X')
        
        plt.show()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())
            
    
        
         
        
            
