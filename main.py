from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from checkbox import *
import sys
import MySQLdb as mdb
ssl = {'ca': 'certs/ca.pem'}
conn = mdb.connect("localhost", "root", "", "pixmap", ssl=ssl)

class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        data = self.get_books()

        height = 0
        self.checks = []
        for i in data:
            height += 30
            self.chLeft = QtWidgets.QCheckBox(parent=self.groupBox)
            self.chLeft.setObjectName(f"{i[0]}")
            self.chLeft.setGeometry(QtCore.QRect(20, height, 180, 21))
            self.checks.append(self.chLeft)
            self.chLeft.setText(f"{i[1]}")

        self.pushButton.clicked.connect(self.onCliclCheck_up)
        self.pushButton_2.clicked.connect(self.onCliclCheck_down)


    def onCliclCheck_up(self):
        checked = ' '.join([checkbox.objectName() for checkbox in self.checks if checkbox.isChecked()])
        if checked:
            for i in checked.split(" "):
                self.change_price(1, int(i))

    def onCliclCheck_down(self):
        checked = ' '.join([checkbox.objectName() for checkbox in self.checks if checkbox.isChecked()])
        if checked:
            for i in checked.split(" "):
                self.change_price(0, int(i))


    def get_books(self):
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM books;")
        res = cur.fetchall()
        cur.close()
        return res

    def change_price(self, way: int, book_id: int):
        cur = conn.cursor()
        rows = cur.execute(f"CALL change_price({way}, {book_id});")
        conn.commit()






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec())
