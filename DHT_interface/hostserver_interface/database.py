from threading import Thread
import sqlite3 as db
import queue
import time

class Database(Thread):
    referenceCount = 0
    def __init__(self, dbname = 'sensordata.db'):
        print ("init db")
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
        print ("Enqueue data")
        #push data into queue
        ret = -2
        if (len(data) == 3):
            ret = self.__POSTMESSAGE("PUT",data)
            
        return ret
    
    def getLatestData(self, latestN = 10):
        data = [latestN]
        self.__POSTMESSAGE("GET",data)
        print ("Waiting for data to be filled")
        while(len(data) == 1):
            continue
        print ("Data filled")
        return data[1:]
        
    def stopThread(self):
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
                print ("CMD: "+cmd)
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
                print ("CMD: "+cmd)
                data = self.dbdataQ.get_nowait()
                limit = data[0]
                self.dbcursor = self.dbHandle.cursor()
                sql = "SELECT TIMESTAMP,TEMPERATURE,HUMIDITY FROM SENSORDATA ORDER BY ID DESC LIMIT %d" % (limit)
                #sql = "SELECT (TEMPERATURE) FROM SENSORDATA"
                print("Sql: " + sql)
                self.dbcursor.execute(sql)
                rows = self.dbcursor.fetchall()
                print ("Len of rows: " + str(len(rows)))
                #for row in rows:
                #    print (row)
                data[1:] = rows
                
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
                print ("Cmd: " + cmd)
                self.__cmdHandler(cmd)   
            except queue.Empty:
                continue;
            
        if self.dbHandle is not None:
            print ("Closing db connection")
            self.dbHandle.close()
        