from PyQt5.QtWidgets import QDialog
from DeleteDialog import Ui_Dialog
from PyQt5 import QtCore

class Dialog_Delete(QDialog, Ui_Dialog):
    signal = QtCore.pyqtSignal()
    def __init__(self):
        super(Dialog_Delete, self).__init__()
        self.setupUi(self)
        self.btn_Cancle.clicked.connect(self.reject)
        self.btn_OK.clicked.connect(self.slot_OK)

    def slot_OK(self):
        self.signal.emit()
        self.close()
