from threading import Thread
import sqlite3 as db
import queue
import sys
import datetime

referenceCount = 0;



class Database(Thread):
    def __init__(self, dbname = 'sensordata.db'):
        print ("init db")
        global referenceCount
        if(referenceCount == 0):
            referenceCount += 1;
            #open db
            self.dbname = dbname
            ##create queue interface
            self.dbdataQ = queue.Queue()
            self.dbcmdQ = queue.Queue()
            self.running = 0
            Thread.__init__(self)
            
    def __POSTMESSAGE(self,cmdstring, dataList = []):
        if self.running == 0:
            return -1
        self.dbdataQ.put(dataList)
        self.dbcmdQ.put(cmdstring)
        return 0;
        
    def putData(self,data = []):
        #print ("Enqueue data")
        #push data into queue
        ret = -2
        if (len(data) == 3):
            ret = self.__POSTMESSAGE("PUT",data)
            
        return ret
    
    def getLatestData(self, latestN = 10):
        data = ["latest",latestN]
        self.__POSTMESSAGE("GET",data)
        #print ("Waiting for data to be filled")
        while(len(data) == 2):
            continue
        #print ("Data filled:",data)
        return data[2:]
    
    #what 0  = avg, 2 = high, 3 = low
    def getTemp(self,what=0):
        data = ["temperature",what]
        self.__POSTMESSAGE("GET",data)
        #print ("Waiting for data to be filled")
        while(len(data) == 2):
            continue
        #print ("Data filled:",data)
        return data[2:]
    
    #what 0 = avg, 2 = high, 3 = low
    def getHum(self,what =0):
        data = ["humidity",what]
        self.__POSTMESSAGE("GET",data)
        #print ("Waiting for data to be filled")
        while(len(data) == 2):
            continue
        #print ("Data filled:",data)
        return data[2:]
        
    def stopThread(self):
        global referenceCount
        referenceCount -= 1
        print("Ref count:",referenceCount)
        if referenceCount == 0:
            while(self.dbdataQ.empty() != True):
                continue
            self.running = 0
    
    def __initfunction(self):
        self.dbHandle = db.connect(self.dbname)
        self.dbcursor = self.dbHandle.cursor()
        self.dbcursor.execute('SELECT SQLITE_VERSION()')
        data = self.dbcursor.fetchone()
        print ("SQLite version: " + str(data))
        
        # Drop table if it already exist using execute() method.
        self.dbcursor.execute("DROP TABLE IF EXISTS SENSORDATA")

        # Create table as per requirement
        sql = """
                 CREATE TABLE SENSORDATA (
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 TIMESTAMP VARCHAR(255) NOT NULL,
                 TEMPERATURE FLOAT NOT NULL,
                 HUMIDITY FLOAT NOT NULL)
              """

        #try:
        self.dbcursor = self.dbHandle.cursor()
        self.dbcursor.execute(sql)
        self.running = 1
        #except:
         #   print ("DB Excepetion")
          #  self.running = 0
        
    def __cmdHandler(self,cmd, args = []):
        if len(cmd) == 0:
            return
        
        if cmd is "PUT":
            try:
                #print ("CMD: "+cmd)
                data = self.dbdataQ.get_nowait()
                #print (data)
                sql = "INSERT INTO SENSORDATA VALUES(NULL,'%s','%f','%f')" % (data[0],data[1],data[2])
                #print("Sql: " + sql)
                self.dbcursor.execute(sql)
                self.dbHandle.commit()                
                
            except queue.Empty:
                print ("CMD DATA MISMATCH")
            except:
                self.dbHandle.rollback()
        
        if cmd is "GET":
            try:
                #print ("CMD: "+cmd)
                data = self.dbdataQ.get_nowait()
                
                if ("latest" in data[0]):
                    limit = data[1]
                    self.dbcursor = self.dbHandle.cursor()
                    sql = "SELECT TIMESTAMP,TEMPERATURE,HUMIDITY FROM SENSORDATA ORDER BY ID DESC LIMIT %d" % (limit)
                    #sql = "SELECT (TEMPERATURE) FROM SENSORDATA"
                    #print("Sql: " + sql)
                    self.dbcursor.execute(sql)
                    rows = self.dbcursor.fetchall()
                    #print ("Len of rows: " + str(len(rows)))
                    #for row in rows:
                    #    print (row)
                    #print ("Rows:",rows)
                    data[2:] = rows
                    
                else:
                    if "temperature" in data[0]:
                        #parse which temp
                        #avg
                        if (data[1] == 0):
                            sql = "SELECT AVG(TEMPERATURE) FROM SENSORDATA"
                        elif (data[1] == 1):
                            sql = "SELECT MIN(TEMPERATURE) FROM SENSORDATA"
                        elif (data[1] == 2):
                            sql = "SELECT MAX(TEMPERATURE) FROM SENSORDATA"

                    elif "humidity" in data[0]:
                        #parse which hum
                        #avg
                        if (data[1] == 0):
                            sql = "SELECT AVG(HUMIDITY) FROM SENSORDATA"
                        elif (data[1] == 1):
                            sql = "SELECT MIN(HUMIDITY) FROM SENSORDATA"
                        elif (data[1] == 2):
                            sql = "SELECT MAX(HUMIDITY) FROM SENSORDATA"
                        
                    self.dbcursor = self.dbHandle.cursor()
                    #print("Sql: " + sql)
                    self.dbcursor.execute(sql)
                    rows = self.dbcursor.fetchall()
                    #print ("Len of rows: " + str(len(rows)))
                    my = []
                    #print ("Date",datetime.datetime.now().strftime("%x:%X"))
                    my.append(datetime.datetime.now().strftime("%x:%X"))
                    my.extend(list(rows))
                    data[3:] = my
                
            except queue.Empty:
                print ("CMD DATA MISMATCH")
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print (message)
                self.dbHandle.rollback()
        
    def run(self):
        self.__initfunction()
        self.dbcursor = self.dbHandle.cursor()
        while self.running:
            #print ("Running")
            try:
                cmd = self.dbcmdQ.get_nowait()
                #print ("Cmd: " + cmd)
                self.__cmdHandler(cmd)   
            except queue.Empty:
                continue;
            
        if self.dbHandle is not None:
            print ("Closing db connection")
            self.dbHandle.close()
        