from string import ascii_lowercase, digits
import sqlite3
import re
import os

class Dblite():
    def __init__(self):
        self.conn = sqlite3.connect("base.db")
        self.c = self.conn.cursor()
        self.createTb()   
    def createTb(self):
        Tb = digits+ascii_lowercase
        for table in Tb:
            try:
                self.c.execute("CREATE TABLE %s(Hash TEXT UNIQUE)"%("\""+table+"\""))
            except sqlite3.OperationalError:
                pass
        self.conn.commit()
    
    def updateTb(self,filepath):
        hashList = []
        try:
            file = open(filepath)
            while True:
                tmp = file.readline().replace("\n","")
                if tmp != '':
                    hashList.append(tmp)
                else : 
                    break
            file.close()
        except FileNotFoundError:
            pass #break

        for hashString in hashList:
            try:
                self.c.execute("INSERT INTO %s(Hash) VALUES(?)"%("\""+hashString[0]+"\""),(hashString,))
            except sqlite3.IntegrityError:
                pass
        self.conn.commit()
        
        try:
            os.remove(filepath)
        except FileNotFoundError:
            pass
    
    def query(self,hash):
        self.c.execute("SELECT Hash FROM \"%s\" WHERE Hash = \"%s\""%(hash[0],hash))
        if self.c.fetchone():
            self.conn.commit()
            return True
        else:
            self.conn.commit() 
            return False