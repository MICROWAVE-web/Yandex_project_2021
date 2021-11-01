# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(730, 460)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(-10, -11, 751, 80))
        self.frame.setStyleSheet("background-color: #f0f0f0;\n"
"border: 1px solid black;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(-1, 69, 741, 391))
        self.frame_2.setStyleSheet("background-color: #fff;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(-20, 0, 761, 101))
        font = QtGui.QFont()
        font.setFamily("URW Gothic")
        font.setPointSize(23)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("color: #000\n"
";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(520, 340, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(".QPushButton {\n"
"    background-color: #0079fe; \n"
"    border-radius: 15px;\n"
"    color: white;\n"
"    border-top: 1px solid #00a8ff;\n"
"    border-bottom: 2px solid #0055fa;\n"
"} \n"
".QPushButton:pressed {\n"
"    border: none;\n"
"    background-color: #013d7d; \n"
"} ")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit.setGeometry(QtCore.QRect(113, 130, 491, 61))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("color: #000;\n"
"border: none;\n"
"border-top-left-radius: 5px;\n"
"border-top-right-radius: 5px;\n"
"border-bottom: 1px solid #666;\n"
"background-color: rgb(240, 240, 240);\n"
"padding-left: 20px;")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-40, 200, 811, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(210, 290, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setLineWidth(4)
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 340, 131, 30))
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed {\n"
"    color: rgb(200, 200, 200);\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Введите ссылку на необходимый ресурс"))
        self.pushButton.setText(_translate("Dialog", "Продолжить ➜"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Введите ссылку"))
        self.pushButton_2.setText(_translate("Dialog", "←  Назад"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
