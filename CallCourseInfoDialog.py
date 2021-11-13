from PyQt5.QtWidgets import QDialog
from CourseInfoDialog import Ui_Dialog

class Dialog_CourseInfo(QDialog, Ui_Dialog):
    def __init__(self):
        super(Dialog_CourseInfo, self).__init__()
        self.setupUi(self)
        self.btn_OK.clicked.connect(self.reject)
        self.btn_Cancle.clicked.connect(self.reject)