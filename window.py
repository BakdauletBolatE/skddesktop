
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton,QBoxLayout,QDialog,QTabWidget
from PyQt5.QtCore import QSize, Qt
from datetime import date, datetime,timedelta
import sqlite3
from era import Ent
from aonit import IntegrationAonit
from tast_manager import Task

today = date.today()
print(today)



class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)
        self.con = sqlite3.connect("mydb.db",check_same_thread=False) 
        self.cursor = self.con.cursor()
        self.era = Ent()
        self.aonit = IntegrationAonit()
        
        self.setMinimumSize(QSize(800, 400))             # Устанавливаем размеры
        self.setWindowTitle("Приложение Интеграций")    # Устанавливаем заголовок окна
        central_widget = QWidget(self)                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        grid_layout = QGridLayout()             # Создаём QGridLayout
        central_widget.setLayout(grid_layout)   # Устанавливаем данное размещение в центральный виджет

        self.tabs = QTabWidget()
        self.table = QTableWidget(self)
        self.responseTable = QTableWidget(self)
        self.responseTable.setColumnCount(3)
        self.table.setColumnCount(5)     # Устанавливаем три колонки
             # и одну строку в таблице
 
        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(["ИИН","ИМЯ","СОБЫИТИЕ","ВРЕМЯ", "ДАТА"])
        self.responseTable.setHorizontalHeaderLabels(["Статус","ТЕКСТ","ДАТА"])
 
       
       
 
        # заполняем первую строк
            
        

        self.collectDataBtn = QPushButton("Обновить данные")
        self.createDataBtn = QPushButton("Создать данные")   
        self.pushDataBtn = QPushButton("Отправить данные")
     
        grid_layout.addWidget(self.collectDataBtn,1,0)
        grid_layout.addWidget(self.createDataBtn,1,1)
        grid_layout.addWidget(self.pushDataBtn,1,2)
        
        self.table.resizeColumnsToContents()
        self.responseTable.resizeColumnsToContents()
        self.tabs.addTab(self.table, "Собитий")
        self.tabs.addTab(self.responseTable,"Отправленные данные")
        grid_layout.addWidget(self.tabs, 20, 0)  

    def createBase(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS events
                (id INTEGER PRIMARY KEY,f_iin text, f_fio text,
                f_event text, f_date text,created_at date)
            """)
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS responses
                (
                    id INTEGER PRIMARY KEY,
                    status_code text,
                    response_text text,
                    created_at date
                )
        """)
        self.con.commit()
        

    def collectData(self):
            self.cursor.execute("SELECT * FROM events ORDER BY created_at DESC;")
            events = self.cursor.fetchall()
            self.cursor.execute("SELECT * FROM responses;")
            responses = self.cursor.fetchall()
            self.table.setRowCount(len(events))  
            self.responseTable.setRowCount(len(responses)) 
            for index,item in enumerate(responses):
                self.responseTable.setItem(index,0,QTableWidgetItem(item[1]))
                self.responseTable.setItem(index,1,QTableWidgetItem(item[2]))
                self.responseTable.setItem(index,2,QTableWidgetItem(item[3]))
            for index,item in enumerate(events):
                self.table.setItem(index, 0, QTableWidgetItem(item[1]))
                self.table.setItem(index, 1, QTableWidgetItem(item[2]))
                self.table.setItem(index, 2, QTableWidgetItem(item[3]))
                self.table.setItem(index, 3, QTableWidgetItem(item[4]))
                self.table.setItem(index, 4, QTableWidgetItem(item[5]))
    
            
    def showDialog(self,name):
        dlg = QDialog()
        b1 = QPushButton(name,dlg)
        b1.move(50,50)
        dlg.setWindowTitle("Модальное окно")
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

    def createData(self):

        self.cursor.execute("DELETE FROM events WHERE created_at = ?;", (today, ))
        events = self.era.collect_events()
        self.cursor.executemany("INSERT INTO events VALUES (?,?,?,?,?,?)", events)
        self.collectData()
        self.con.commit()

    def sendData(self):
        send = IntegrationAonit().sendRequestToAonit()
        if send == 200:
            self.showDialog("Данные успешно отправлены")
        else:
            self.showDialog("Проверьте подключение к сети")
        

    def start(self):
        self.createBase()
    
        self.collectDataBtn.clicked.connect(self.collectData)
        self.pushDataBtn.clicked.connect(self.sendData)
        self.createDataBtn.clicked.connect(self.createData)
 
 
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    mw = MainWindow()
    task = Task(1)
    task.start()
    mw.start()
    mw.show()
    def closeApp():
        app.exec()
        task.done()
    sys.exit(closeApp())