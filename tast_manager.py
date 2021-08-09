import threading
import time

import schedule

class Task(threading.Thread):
    def __init__(self,seconds):
        super().__init__() 
        self.delay = seconds 
        self.is_done = False 
       
    
    def done(self): 
        self.is_done = True 

    def job(self):
        # send = self.aonit.sendRequestToAonit()
        # if send == 200:
        #     print(send)
        # else:
        #     print("ПРОВЕРТЕ СЕТЬ")
        print("HELLO")
 
    def run(self): 
        schedule.every(1).minutes.do(self.job)
        while not self.is_done: 
            time.sleep(self.delay) 
            schedule.run_pending()
           
        print('thread done') 

t = Task(5) 
t.start() 
       

    

    
 
 


