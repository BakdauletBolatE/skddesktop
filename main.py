import sys
from PyQt5.QtWidgets import QApplication, QWidget
import schedule
import time
import threading
from tast_manager import Task
import sqlite3

if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    
    Task().start()
 
    conn = sqlite3.connect("mydb.db") 
    cursor = conn.cursor()


    try:
        cursor.execute("""CREATE TABLE albums
                    (f_areas_name text, f_iin text, f_fio text,
                    f_event text, f_time text f_date text)
                """)
        conn.commit()
    except sqlite3.OperationalError:
        print('Hello')
 

    albums = [('Exodus', 'Andy Hunter', '7/9/2002', 'Sparrow Records', 'CD'),
            ('Until We Have Faces', 'Red', '2/1/2011', 'Essential Records', 'CD'),
            ('The End is Where We Begin', 'Thousand Foot Krutch', '4/17/2012', 'TFKmusic', 'CD'),
            ('The Good Life', 'Trip Lee', '4/10/2012', 'Reach Records', 'CD')]
    
    cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)", albums)
    conn.commit()

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    sys.exit(app.exec_())