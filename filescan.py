import re
import os
import threading
import time
from modules.dblite import Dblite
from hashlib import md5

class Filescan:
    __db = Dblite()
    __countScanned = 0
    __threadsCounter = 1
    __listThreat = []
    __listFile = []
    __listExec = [
            'apk',
            'bat',
            'class',
            'cmd',
            'com',
            'cpl',
            'csv',
            'djvu',
            'dll',
            'docx',
            'exe',
            'htm',
            'html',
            'inf1',
            'ins',
            'inx',
            'isu',
            'jar',
            'job',
            'js',
            'jse',
            'msc',
            'msi',
            'msp',
            'mst',
            'paf',
            'pdf',
            'pif',
            'ps1',
            'py',
            'reg',
            'rgs',
            'scr',
            'sct',
            'shb',
            'shs',
            'txt',
            'u3p',
            'vb',
            'vbe',
            'vbs',
            'vbscript',
            'ws',
            'wsf',
            'wsh',
                ]
    def __init__(self):
        self.__db.createTb()
        self.__db.updateTb("base.txt")
        
        
    def __add(self,path):
        global __listExec,__listFile,__threadsCounter
        self.__threadsCounter = 1
        path = path + "\\"
        if(os.path.exists(path)):
            for r in os.walk(path):
                self.__threadsCounter += 1
                threading._start_new_thread(Filescan.__appenFile,(self,r[0],r[2]))
                #if self.__threadsCounter < 0: self.__threadsCounter = 1
                if self.__threadsCounter == len(r[2]):
                    while self.__threadsCounter != 0:
                       pass
            #grep total__number_of_file
            #implement hashmd5 for next
            time.sleep(1)
            print("total file will scan :",len(self.__listFile))
            return True
        else:
            return False

    @staticmethod
    def __appenFile(self,r,f):
        global __listExec,__listFile,__threadsCounter
        for file in f:
            filepath = os.path.join(r,file)
            for word in self.__listExec:
                if re.search(word+"$",filepath):
                    try:
                        if os.stat(filepath).st_size <= 5485760:
                            self.__listFile.append(filepath)
                    except IOError:
                        pass
                    break
            self.__threadsCounter += -1

    def __scanFile(self,numThreads):
        global __listThreat,__listFile,__threadsCounter,__db
        start = 0
        end = 0
        infect = []
        self.__threadsCounter = 1
        totalsize = len(self.__listFile)
        if totalsize > numThreads:
            compleThread = int(totalsize%numThreads)
            maxPerThread = int((totalsize-compleThread) / numThreads)
            threading._start_new_thread(Filescan.__hashMatch,(self,maxPerThread * numThreads,maxPerThread * numThreads + compleThread))
            for i in range(1,numThreads+1):
                self.__threadsCounter += 1
                threading._start_new_thread(Filescan.__hashMatch,(self,maxPerThread * (i-1),maxPerThread * i))
        else:
            threading._start_new_thread(Filescan.__hashMatch,(self,0,len(self.__listFile)))
        while self.__threadsCounter != 0:
            time.sleep(0.5)
            print("file scanned :",self.__countScanned,"/",len(self.__listFile))
            end = self.__countScanned
            for i in range(start,end):
                if self.__db.query(str(self.__listThreat[i])[0:32]):
                    infect.append(i)
            start = end

        if start != len(self.__listThreat):
            end = self.__countScanned
            for i in range(start,end):
                if self.__db.query(str(self.__listThreat[i])[0:32]):
                    infect.append(i)
            #print(start," ",end)
        print("file scanned :",self.__countScanned,"/",len(self.__listFile))
        print("File infection :",len(infect),"/",len(self.__listFile))
        index = 0
        for i in infect:
            index += 1
            print(index,". ",str(self.__listThreat[i])[32:])
    @staticmethod
    def __hashMatch(self,start,end):
        global __listThreat,__listFile,__threadsCounter,__db,__countScanned
        for i in range(start,end):
            try:   
                binary = open(self.__listFile[i],'rb')
                hashbin = md5(binary.read()).hexdigest()
                self.__listThreat.append(hashbin+self.__listFile[i])
                self.__countScanned +=1
            except (PermissionError,OSError):
                pass
        self.__threadsCounter -= 1
        

    # @staticmethod
    # def __filterFile(self,filepath):
    #     global __listExec,__listFile,__threadsCounter
    #     for word in self.__listExec:
    #         if re.search(word+"$",filepath):
    #             self.__listFile.append(filepath)  
    #             break
    #     self.__threadsCounter += -1 

    def customScan(self,path):
        if self.__add(path):
            self.__scanFile(8) #number of threads
            self.clean()
            return True
        else:
            print("Directory not found! ...") 
            return True

    def clean(self):
        self.__threadsCounter = 0
        self.__countScanned = 0
        self.__threadsCounter = 1
        self.__listThreat.clear()
        self.__listFile.clear()
        self.__db.conn.commit()