import threading
import time

class Task(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def job(self):
        print("Работаю")


    def save_data(self):
        schedule.every(1).minutes.do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(1)


