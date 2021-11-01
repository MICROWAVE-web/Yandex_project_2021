import math
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(434, 393)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 231, 25))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 50, 411, 281))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 434, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "загрузить нечётные строки"))


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file = open('lines.txt', mode='r', encoding='utf-8')
        self.lines = self.file.readlines().copy()
        self.nechet = True
        self.ui.pushButton.clicked.connect(self.display)

    def display(self):
        if len(self.lines) > 0:
            self.ui.textEdit.setText('')
            if self.nechet:
                output = ''
                for line in range(0, len(self.lines), 2):
                    output += str(self.lines[line])
                self.ui.textEdit.setText(output)
                self.ui.pushButton.setText('загрузить чётные строки')
                self.nechet = False
            else:
                output = ''
                for line in range(1, len(self.lines), 2):
                    output += str(self.lines[line])
                self.ui.textEdit.setText(output)
                self.ui.pushButton.setText('загрузить нечётные строки')
                self.nechet = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
