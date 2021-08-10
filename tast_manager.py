import threading
import time
from aonit import IntegrationAonit
from perco import Perco
from datetime import date, datetime,timedelta
import schedule
import sqlite3

today = date.today()

class Task(threading.Thread):
    def __init__(self,seconds):
        super().__init__() 
        self.delay = seconds 
        self.intAo = IntegrationAonit()
        self.con = sqlite3.connect("mydb.db",check_same_thread=False) 
        self.cursor = self.con.cursor()
        self.perco = Perco()
        self.is_done = False 
       
    
    def done(self): 
        self.is_done = True 

    def getJob(self):
        self.cursor.execute("DELETE FROM events WHERE created_at = ?;", (today, ))
        events = self.perco.loadEvents()
        self.cursor.executemany("INSERT INTO events VALUES (NULL,?,?,?,?,?,?)", events)
        print(events)
        self.con.commit()

    def sendJob(self):
        send = self.intAo.sendRequestToAonit()
        if send == 200:
            print(send)
        else:
            print("ПРОВЕРТЕ СЕТЬ")
        print("HELLO")
 
    def run(self):
        schedule.every().day.at("23:30").do(self.getJob)
        schedule.every().day.at("23:55").do(self.sendJob)
        while not self.is_done: 
            time.sleep(self.delay) 
            schedule.run_pending()
           
        print('thread done') 

       

    

    
 
 


