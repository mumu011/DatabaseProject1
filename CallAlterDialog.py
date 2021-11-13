from PyQt5.QtWidgets import QDialog
from AlterDialog import Ui_Dialog
from PyQt5 import QtCore

class Dialog_Alter(QDialog, Ui_Dialog):
    signal = QtCore.pyqtSignal(str,int,int,str,str)

    def __init__(self):
        super(Dialog_Alter, self).__init__()
        self.setupUi(self)
        self.btn_Cancle.clicked.connect(self.reject)
        self.btn_OK.clicked.connect(self.slot_OK)

    def slot_OK(self):
        self.signal.emit(self.lineEdit_CourseName.text(),int(self.lineEdit_CreditHour.text()),int(self.lineEdit_CourseHour.text()),
                         self.lineEdit_PriorCourse.text(),self.lineEdit_CourseNo.text())
        self.close()