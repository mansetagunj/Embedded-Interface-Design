#!/usr/bin/env python3
import sys
import json

class AWSConfigReader():
    
    def __init__(self, sysargs):
        self.configFile = self.__parseArgs(sysargs)
        self.configDict = self.__getConfiguration(self.configFile)

    def __getConfiguration(self, filename):
        print (filename)
        with open(filename) as f:
            dataDict = json.load(f)
            print (dataDict)
            return dataDict

    def __parseArgs(self, sysargs):
        if(len(sysargs) < 3):
            print ("No config file")
            sys.exit(0);
        
        print (sysargs[1])
        if('-f' in sysargs[1]):  
            return sysargs[2]
        else:
            print ("Invalid Option")
            
    def getConfigItem(self, itemKey):
        if itemKey in self.configDict.keys():
            return self.configDict[itemKey]
        else:
            return None
        
    def getConfigItemKeys(self):
        return list(self.configDict.keys())
    
    def getConfigDictDump(self):
        return self.configDict
    

if __name__ == '__main__':
    AWSConfig = AWSConfigReader(sys.argv)
    print ("Keys:", AWSConfig.getConfigItemKeys())
    print (AWSConfig.getConfigItem('port'))
    print (AWSConfig.getConfigItem('host'))
    print (AWSConfig.getConfigItem('clientIds'))

