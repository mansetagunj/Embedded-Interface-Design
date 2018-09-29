#!/usr/bin/env python3
#reference: https://engineersportal.com/blog/2018/8/14/real-time-graphing-in-python
import serial
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.ticker as ticker

import sys


class RealTimePlotter:

    def __init__(self):
        self.size = 30
        self.plt.ion()
        self.fig = plt.figure(figsize=(13,6), clear=True)
        self.ax = fig.add_subplot(111)
        self.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        dataQ = Queue()
        
    #reference: https://engineersportal.com/blog/2018/8/14/real-time-graphing-in-python
    def live_plotter(x_vec,y1_data,line1,ylabel= '', identifier='',pause_time=0.1):
        global i
        if line1==[]:
            line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)        
            self.plt.ylabel(ylabel)
            self.plt.title('{}'.format(identifier))
            self.plt.show()

        i=i+1
        ax.set_ylim(min(y1_data)-0.2,max(y1_data)+0.2,auto=True)
        # after the figure, axis, and line are created, we only need to update the y-data
        line1.set_ydata(y1_data)
        # adjust limits if new data goes beyond bounds
        if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
            plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
        # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
        plt.pause(pause_time)
        
        # return line so we can update it again in the next iteration
        return line1
    
    def putData(self,data):
        if self.plotterRun is True:
            dataQ.put(data)
    
    def stopPlotter(self):
        self.plotterRun = False;

    def startPlotter(self):
    
        self.plotterRun = True
        self.plt.style.use('ggplot')
        
        workerThread = Thread(target=self.plotterWorker)
        workerThread.daemon = True
        workerThread.start()
        
    def plotterWorker(self):

        x_vec = np.linspace(0,size,size+1)[0:-1]
        y_vec = np.zeros(len(x_vec))
        readings_vec = []

        print("Real Time Temperature Plotter")
            
        while self.plotterRun is True:
    
            try:
                temperature = dataQ.get_nowait()
            except queue.Empty:
                continue;
                
            print('Current Temp: {} Celcius'.format(temperature_C), end="\r", flush=True)
            
            y_vec[-1] = temperature
            readings_vec = live_plotter(x_vec,y_vec,readings_vec, "Temperature", "Real-Time Data")
            y_vec = np.append(y_vec[1:],0.0)
        