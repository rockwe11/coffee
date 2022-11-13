import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.loadTable()

    def loadTable(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM info").fetchall()
        title = ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах",
                 "Описание вкуса", "Цена", "Объем упаковки"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Coffee()
    a.show()
    sys.exit(app.exec())
