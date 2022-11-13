import sqlite3
import sys
from addEditCoffeeForm import Ui_Form
from main_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class Coffee(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi("main.ui", self)
        self.setupUi(self)
        self.loadTable()
        self.pushButton.clicked.connect(self.add_button)

    def loadTable(self):
        cur = con.cursor()
        self.res = cur.execute("SELECT * FROM info").fetchall()
        title = ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах",
                 "Описание вкуса", "Цена", "Объем упаковки"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.cellDoubleClicked.connect(self.edit_cell)

    def edit_cell(self, i, j):
        self.edit_form = EditForm(self, self.res[i])
        self.edit_form.show()

    def add_button(self):
        self.edit_form = EditForm(self)
        self.edit_form.show()


class EditForm(QWidget, Ui_Form):
    def __init__(self, parent, data=[]):
        super().__init__()
        self.parent = parent
        self.data = data
        # uic.loadUi("addEditCoffeeForm.ui", self)
        self.setupUi(self)
        self.init_data()
        self.pushButton.clicked.connect(self.confirm)

    def init_data(self):
        if self.data:
            self.lineEdit.setText(self.data[1])
            self.spinBox_2.setValue(int(self.data[2]))
            self.lineEdit_2.setText(self.data[3])
            self.lineEdit_3.setText(self.data[4])
            self.spinBox_3.setValue(int(self.data[5]))
            self.spinBox_4.setValue(int(self.data[6]))

    def confirm(self):
        cur = con.cursor()
        if self.data:
            cur.execute("""UPDATE info
                        SET 'название сорта'=?,
                        'степень обжарки'=?,
                        'молотый/в зернах'=?,
                        'описание вкуса'=?,
                        'цена'=?,
                        'объем упаковки' = ? WHERE id = ?""",
                        (self.lineEdit.text(), self.spinBox_2.value(), self.lineEdit_2.text(),
                         self.lineEdit_3.text(), self.spinBox_3.value(), self.spinBox_4.value(), self.data[0]))
        else:
            keys = ["'название сорта'", "'степень обжарки'", "'молотый/в зернах'", "'описание вкуса'", "'цена'",
                    "'объем упаковки'"]
            cur.execute(f"""INSERT INTO info({','.join(keys)}) VALUES(?, ?, ?, ?, ?, ?)""",
                        (self.lineEdit.text(), self.spinBox_2.value(), self.lineEdit_2.text(),
                         self.lineEdit_3.text(), self.spinBox_3.value(), self.spinBox_4.value()))
        con.commit()
        self.parent.loadTable()
        self.close()


if __name__ == '__main__':
    con = sqlite3.connect("data/coffee.sqlite")
    app = QApplication(sys.argv)
    a = Coffee()
    a.show()
    sys.exit(app.exec())
