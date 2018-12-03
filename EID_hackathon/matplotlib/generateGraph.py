#!/usr/bin/env python3
import time
import datetime
import sys
import ast
import json
import matplotlib.pyplot as plt
import matplotlib
import csv       
        
        
if __name__ == '__main__':
    with open('data.csv', 'r', encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter='\n')
        #print (reader)
        datalist = list(reader)
        newDatalist = []
        plot1X = []
        plot2X = []
        plot3X = []
        plot4X = []
        plot1Y = []
        plot2Y = []
        plot3Y = []
        plot4Y = []
        for list in datalist:
            newDatalist = list[0].split(",")
            newDatalist = [int(i) for i in newDatalist]
            #print ("List:",newDatalist)
            if newDatalist[0] is 1:
                plot1X.append(newDatalist[2])
                plot1Y.append(newDatalist[3])
            elif newDatalist[0] is 2:
                plot2X.append(newDatalist[2])
                plot2Y.append(newDatalist[3])
            elif newDatalist[0] is 3:
                plot3X.append(newDatalist[2])
                plot3Y.append(newDatalist[3])
            elif newDatalist[0] is 4:
                plot4X.append(newDatalist[2])
                plot4Y.append(newDatalist[3])
            
        print ("Plot1X:",plot1X)
        print ("Plot1Y:",plot1Y)
        print ("Plot2X:",plot2X)
        print ("Plot2Y:",plot2Y)
        print ("Plot3X:",plot3X)
        print ("Plot3Y:",plot3Y)
        print ("Plot4X:",plot4X)
        print ("Plot4Y:",plot4Y)
        
        
        f = plt.figure(1)
        plt.xticks(plot1X)
        plt.plot(plot1X, plot1Y, 'y-', label='Line1')
        plt.plot(plot2X, plot2Y, 'r-', label='Line2')
        plt.plot(plot3X, plot3Y, 'g-', label='Line3')
        plt.plot(plot4X, plot4Y, 'b-', label='Line4')
        plt.legend(loc='best')
        plt.title('Graph')
        plt.ylabel('Y')
        plt.xlabel('X')
        
        plt.show()
         
        
            
