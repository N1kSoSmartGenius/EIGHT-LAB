import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout, QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Shedule")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_shedule_tab()
        self._create_subjects_tab()


    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="tg_bot", user="postgres", password="5591", host="localhost", port="5432")
        self.cursor = self.conn.cursor()


    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")
        self.monday_gbox = QGroupBox("Monday")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.monday_gbox)
        self._create_monday_table()
        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)
        self.shedule_tab.setLayout(self.svbox)
    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(4)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", "", ""])
        self._update_monday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)
    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM timetable2 WHERE day='Monday'")
        records = list(self.cursor.fetchall())
        self.monday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.monday_table.setItem(i, 0,
            QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 1,
            QTableWidgetItem(str(r[4])))
            self.monday_table.setCellWidget(i, 2, joinButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r:self._change_day_from_table(num,data))
            self.monday_table.resizeRowsToContents()
    def _change_day_from_table(self, rowNum, data):
        row = list()
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"UPDATE timetable2 SET subject='{row[0]}', start_time='{row[2]}', room_numb='{row[1]}', teacher='{row[3]}' WHERE subject='{data[2]}'")
            self.conn.commit()
            self._update_monday_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    
    def _create_subjects_tab(self):
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab,"Subjects")
        self.subjects_tab_gbox = QGroupBox("Subjects")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.subjects_tab_gbox)
        # self._create_all_subjects_table()
        self.update_subjects_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_subjects_button)
        # self.update_subjects_button.clicked.connect(self._update_subject)
        self.subjects_tab.setLayout(self.svbox)

    def _update_shedule(self):
        self._update_monday_table()




app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())


    