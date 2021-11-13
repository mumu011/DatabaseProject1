from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from InsertDialog import Ui_Dialog

class Dialog_Insert(QDialog,Ui_Dialog):
    signal = QtCore.pyqtSignal(str,str,str,str,str)
    def __init__(self):
        super(Dialog_Insert, self).__init__()
        self.setupUi(self)
        self.btn_Cancle.clicked.connect(self.reject)
        self.btn_OK.clicked.connect(self.slot_OK)

    def slot_OK(self):
        CourseNo = self.lineEdit_CourseNo.text()
        CourseName = self.lineEdit_CourseName.text()
        CreditHour = self.lineEdit_CreditHour.text()
        CourseHour = self.lineEdit_CourseHour.text()
        PriorCourse = self.lineEdit_PriorCourse.text()
        self.signal.emit(CourseNo,CourseName,CreditHour,CourseHour,PriorCourse)
        self.close()