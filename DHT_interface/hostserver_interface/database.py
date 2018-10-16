from threading import Thread
import sqlite3 as db
import queue
import time

class Database(Thread):
    def __init__(self, dbname = 'sensordata.db'):
        print ("init db")
        #open db
        self.dbname = dbname
        ##create queue interface
        self.dbdataQ = queue.Queue()
        self.running = 0
        Thread.__init__(self)
        
        
    def putData(self,data = []):
        if self.running == 0:
            return -1
        print ("Enqueue data")
        #push data into queue
        if (len(data) == 3):
            #print (data)
            self.dbdataQ.put(data)
            return 0
        else:
            return -2
        
    def stopThread(self):
        while(self.dbdataQ.empty() != True):
            continue
        self.running = 0
    
    def __initfunction(self):
        self.dbHandle = db.connect(self.dbname)
        dbcursor = self.dbHandle.cursor()
        dbcursor.execute('SELECT SQLITE_VERSION()')
        data = dbcursor.fetchone()
        print ("SQLite version: " + str(data))
        
        # Drop table if it already exist using execute() method.
        dbcursor.execute("DROP TABLE IF EXISTS SENSORDATA")

        # Create table as per requirement
        sql = """
                 CREATE TABLE SENSORDATA (
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 TIMESTAMP VARCHAR(255) NOT NULL,
                 TEMPERATURE FLOAT NOT NULL,
                 HUMIDITY FLOAT NOT NULL)
              """

        #try:
        dbcursor = self.dbHandle.cursor()
        dbcursor.execute(sql)
        self.running = 1
        #except:
         #   print ("DB Excepetion")
          #  self.running = 0
        
    def run(self):
        self.__initfunction()
        dbcursor = self.dbHandle.cursor()
        while self.running:
            #print ("Running")
            try:
                data = self.dbdataQ.get_nowait()
                #print (data)
                sql = "INSERT INTO SENSORDATA VALUES(NULL,'%s','%f','%f')" % (data[0],data[1],data[2])
                #print("Sql: " + sql)
                dbcursor.execute(sql)
                self.dbHandle.commit()
                
            except queue.Empty:
                continue;
            except:
                self.dbHandle.rollback()
            
            
        if self.dbHandle is not None:
            print ("Closing db connection")
            self.dbHandle.close()
        