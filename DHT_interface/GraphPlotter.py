#!/usr/bin/env python3
#reference: https://engineersportal.com/blog/2018/8/14/real-time-graphing-in-python
import serial
import time
import matplotlib
import matplotlib.pyplot as matplot
import matplotlib.animation as animation
import numpy as np
import matplotlib.ticker as ticker
import queue
from threading import Thread
import sys


class RealTimePlotter:

    def __init__(self, samples = 10):
        self.size = samples
        self.plt = matplot
        self.dataQ = queue.Queue()
        self.plotterRun = False;
        
    #reference: https://engineersportal.com/blog/2018/8/14/real-time-graphing-in-python
    def live_plotter(self, x_vec,hum_data, temp_data,line1,line2,avg1, avg2,pause_time=0.1):
        
        if line1==[]:
            #print (temp_data, [(sum(temp_data)/float(len(temp_data)))]*self.size)
            line1,avg1, = self.ax.plot(x_vec,hum_data,'-bo', x_vec, [(sum(hum_data)/float(len(hum_data)))]*self.size, 'r+')
            line2,avg2, = self.bx.plot(x_vec, temp_data, '-bo',x_vec, [(sum(temp_data)/float(len(temp_data)))]*self.size, 'r+')   
            self.plt.show()
            

        self.ax.set_ylim(min(hum_data)-0.2,max(hum_data)+0.2,auto=True)
        self.bx.set_ylim(min(temp_data)-0.2,max(temp_data)+0.2,auto=True)
        # after the figure, axis, and line are created, we only need to update the y-data
        line1.set_ydata(hum_data)
        line2.set_ydata(temp_data)
        avg2.set_ydata([(sum(temp_data)/float(len(temp_data)))]*self.size)
        avg1.set_ydata([(sum(hum_data)/float(len(hum_data)))]*self.size)
        # adjust limits if new data goes beyond bounds
        #if np.min(temp_data+hum_data) <= line1.axes.get_ylim()[0] or np.max(temp_data+hum_data) >= line1.axes.get_ylim()[1]:
            #self.plt.ylim([np.min(temp_data+hum_data)-np.std(temp_data+hum_data),np.max(temp_data+hum_data)+np.std(temp_data+hum_data)])
        # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
        self.plt.pause(pause_time)
        
        # return line so we can update it again in the next iteration
        return line1, line2, avg1, avg2
    
    def isPlotterRunning(self):
        return self.plotterRun
    
    def putData(self,data):
        if self.plotterRun is True:
            self.dataQ.put(data)
    
    def stopPlotter(self):
        self.plotterRun = False
        
    
    def plotStatic(self, temp_data, hum_data):
        staticplot = matplot
        staticplot.ion()
        fig = staticplot.figure(figsize=(6,6), clear=True)
        if not temp_data:
            temp_data = [0]*10
        if not hum_data:
            hum_data = [0]*10

        ax = fig.add_subplot(211)
        staticplot.grid(True)
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        ax.set_title('Stored Sensor data')
        ax.set_xlabel('Samples')
        ax.set_ylabel('Humidity')
        ax.set_ylim(min(hum_data)-0.2,max(hum_data)+0.2,auto=True)
        
        
        bx = fig.add_subplot(212)
        staticplot.grid(True)
        bx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        bx.set_xlabel('Samples')
        bx.set_ylabel('Temperature')
        bx.set_ylim(min(temp_data)-0.2,max(temp_data)+0.2,auto=True)
        
        x_vec = range(len(temp_data))
        temp_avg = [(sum(temp_data)/float(len(temp_data)))]*len(x_vec)
        hum_avg = [(sum(hum_data)/float(len(hum_data)))]*len(x_vec)
        
        bx.plot(x_vec,temp_data,'-bs',x_vec, temp_avg, 'r+')
        ax.plot(x_vec,hum_data,'-bs',x_vec, hum_avg, 'r+')
        staticplot.show()        

    def startPlotter(self):
    
        self.plotterRun = True
        self.plt.ion()
        self.fig = self.plt.figure(figsize=(6,6), clear=True)
        
        self.ax = self.fig.add_subplot(211)
        self.plt.grid(True)
        self.ax.set_title('Sensor Real time data')
        self.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        self.ax.set_xlabel('Samples')
        self.ax.set_ylabel('Humidity')
        
        self.bx = self.fig.add_subplot(212)
        self.plt.grid(True)
        self.bx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        self.bx.set_xlabel('Samples')
        self.bx.set_ylabel('Temperature')
        
        workerThread = Thread(target=self.plotterWorker)
        workerThread.daemon = True
        workerThread.start()
        
    def plotterWorker(self):

        x_vec = np.linspace(0,self.size,self.size+1)[0:-1]
        y1_vec = np.zeros(len(x_vec))
        y2_vec = np.zeros(len(x_vec))
        readingsTemp_vec = []
        readingsHum_vec = []
        avg_temp = []
        avg_hum = []

        print("Real Time Temperature Plotter")
            
        while self.plotterRun is True:
    
            try:
                humidity, temperature = self.dataQ.get_nowait()
            except queue.Empty:
                #print ("Q data empty")
                continue;
                
            #print('Plottter: Temp: {} Hum: {}'.format(temperature,humidity),flush=True)
            
            y1_vec[-1] = humidity
            y2_vec[-1] = temperature
            readingsHum_vec, readingsTemp_vec, avg_hum, avg_temp= self.live_plotter(x_vec,y1_vec, y2_vec,readingsHum_vec,readingsTemp_vec, avg_hum, avg_temp)
            y1_vec = np.append(y1_vec[1:],0.0)
            y2_vec = np.append(y2_vec[1:],0.0)
            
        self.dataQ.queue.clear()
        