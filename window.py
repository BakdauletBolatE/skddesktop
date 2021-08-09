
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton,QBoxLayout
from PyQt5.QtCore import QSize, Qt
from datetime import date, datetime,timedelta
import sqlite3


today = date.today()
prevDat = today-timedelta(days=2)
print(today)

events = [('1651651651', 'Bakdaulet Bolat', 'Вышел',today),
        ('1651651651', 'Bakdaulet Bolat', 'Вход',today),
        ('1651651651', 'Bakdaulet Bolat', 'Вышел',today),
        ('6468468466', 'Djars', 'Вышел',today),
        ('6468468466', 'Djars', 'Вход',today),
         ('64684684asda66', 'Kjars', 'Вход',today),
        ('6541651650', 'Nurbek', 'Вышел',today)]

class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)
        self.con = sqlite3.connect("mydb.db") 
        self.cursor = self.con.cursor()
 
        self.setMinimumSize(QSize(800, 400))             # Устанавливаем размеры
        self.setWindowTitle("Работа с QTableWidget")    # Устанавливаем заголовок окна
        central_widget = QWidget(self)                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        grid_layout = QGridLayout()             # Создаём QGridLayout
        central_widget.setLayout(grid_layout)   # Устанавливаем данное размещение в центральный виджет


        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.setColumnCount(4)     # Устанавливаем три колонки
             # и одну строку в таблице
 
        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(["id собитий", "ИИН", "ИМЯ","СОБЫИТИЕ"])
 
        # Устанавливаем всплывающие подсказки на заголовки
        self.table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.table.horizontalHeaderItem(1).setToolTip("Column 2 ")
        self.table.horizontalHeaderItem(2).setToolTip("Column 3 ")
        self.table.horizontalHeaderItem(3).setToolTip("Column 4 ")
 
        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
 
        # заполняем первую строк
            
        

        self.collectDataBtn = QPushButton("Обновить данные")
        self.createDataBtn = QPushButton("Создать данные")   
     
        grid_layout.addWidget(self.collectDataBtn,1,0)
        grid_layout.addWidget(self.createDataBtn,1,1)
        
        self.table.resizeColumnsToContents()
        grid_layout.addWidget(self.table, 20, 0)  

    def createBase(self):
        try:
            self.cursor.execute("""CREATE TABLE events
                    (id INTEGER PRIMARY KEY,f_iin text, f_fio text,
                    f_event text, f_date text)
                """)
            self.con.commit()
        except sqlite3.OperationalError:
            print('Уже сущетвует')

    def collectData(self):
            self.cursor.execute("SELECT * FROM events;")
            events = self.cursor.fetchall()
            self.table.setRowCount(len(events))   
            for index,item in enumerate(events):
                self.table.setItem(index, 0, QTableWidgetItem(item[1]))
                self.table.setItem(index, 1, QTableWidgetItem(item[1]))
                self.table.setItem(index, 2, QTableWidgetItem(item[2]))
                self.table.setItem(index, 3, QTableWidgetItem(item[3]))
    
            

    def createData(self):

        self.cursor.execute("DELETE FROM events WHERE f_date = ?;", (today, ))


        self.cursor.executemany("INSERT INTO events VALUES (NULL,?,?,?,?)", events)
        self.collectData()

        self.con.commit()
        
    def start(self):
        self.createBase()
        self.collectDataBtn.clicked.connect(self.collectData)
        self.createDataBtn.clicked.connect(self.createData)
 
 
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.start()
    mw.show()
    
    sys.exit(app.exec())