import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QTableWidgetItem,QAbstractItemView
from mainwindow import Ui_MainWindow
from CallInsertDialog import Dialog_Insert
from CallDeleteDialog import Dialog_Delete
from CallAlterDialog import Dialog_Alter
from CallCourseInfoDialog import Dialog_CourseInfo
import os
import cx_Oracle

class App(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        self.connect_Oracle()
        self.showClassInfo()
        self.btn_close.clicked.connect(self.slot_close)
        self.btn_insert.clicked.connect(self.slot_insert)
        self.ChildInsertDialog = Dialog_Insert()
        self.ChildInsertDialog.signal.connect(self.insert)
        self.btn_delete.clicked.connect(self.btnClicked_delete)
        self.ChildDeleteDialog = Dialog_Delete()
        self.ChildDeleteDialog.signal.connect(self.slot_delete)
        self.btn_alter.clicked.connect(self.btnClicked_alter)
        self.ChildAlterDialog = Dialog_Alter()
        self.ChildAlterDialog.signal.connect(self.slot_alter)
        self.ChildCourseInfoDialog = Dialog_CourseInfo()
        self.btn_classinfo.clicked.connect(self.slot_CourseInfo)

    def connect_Oracle(self):
        os.environ['path'] = r'D:/Python/Python39/instantclient_21_3'
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
        self.conn = cx_Oracle.connect('s2019011371/cominghome458@166.111.68.220:1521/dbta')
        self.cur = self.conn.cursor()

    def showClassInfo(self):
        sql = "select * from course"
        self.cur.execute(sql)
        content = self.cur.fetchall()
        # print(content)

        # 设置表头
        self.tableWidget_classinfo.clear()
        key_list = ["COURSENO","COURSENAME","CREDITHOUR","COURSEHOUR","PRIORCOURSE"]
        self.tableWidget_classinfo.setColumnCount(len(key_list))
        self.tableWidget_classinfo.setRowCount(len(content))
        self.tableWidget_classinfo.setHorizontalHeaderLabels(key_list)
        self.tableWidget_classinfo.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_classinfo.verticalHeader().setVisible(True)
        # 设置不可编辑
        self.tableWidget_classinfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置整行选择
        self.tableWidget_classinfo.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置一次只能选择一行
        self.tableWidget_classinfo.setSelectionMode(QAbstractItemView.SingleSelection)

        for i in range(0,len(content)):
            row = content[i]
            for j in range(0,len(row)):
                self.tableWidget_classinfo.setItem(i,j,QTableWidgetItem(str(row[j])))

    def slot_CourseInfo(self):
        # 获取选中行数据
        row = self.tableWidget_classinfo.selectedItems()[0].row()
        courseno = self.tableWidget_classinfo.item(row,0).text()

        # 查询选课人的姓名、学号和成绩
        sql = "select t.studentno,score,studentname from score s, student t where s.courseno = '%s' and s.studentno = t.studentno"
        # print(sql % courseno)
        self.cur.execute(sql % courseno)
        content = self.cur.fetchall()

        # 查询总人数、平均成绩
        sql = "select count(studentno), avg(score) from score where courseno = '%s'"
        # print(sql % courseno)
        self.cur.execute(sql % courseno)
        info = self.cur.fetchall()

        # 设置表头
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.clear()
        key_list = ["STUDENTNO", "STUDENTNAME", "SCORE"]
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.setColumnCount(len(key_list))
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.setRowCount(len(content)+2)
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.setHorizontalHeaderLabels(key_list)
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.horizontalHeader().setStretchLastSection(True)
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.verticalHeader().setVisible(True)
        # 设置不可编辑
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i in range(0,len(content)):
            row = content[i]
            for j in range(0, len(row)):
                self.ChildCourseInfoDialog.tableWidget_CourseInfo.setItem(i, j, QTableWidgetItem(str(row[j])))

        self.ChildCourseInfoDialog.tableWidget_CourseInfo.setItem(len(content), 0, QTableWidgetItem("总人数"))
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.setItem(len(content), 1, QTableWidgetItem(str(info[0][0])))
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.setItem(len(content)+1, 0, QTableWidgetItem("平均成绩"))
        self.ChildCourseInfoDialog.tableWidget_CourseInfo.setItem(len(content)+1, 1, QTableWidgetItem(str(info[0][1])))

        self.ChildCourseInfoDialog.show()

    def slot_insert(self):
        self.ChildInsertDialog.show()

    def insert(self,CourseNo,CourseName,CreditHour,CourseHour,PriorCourse):
        sql = "insert into course values ('%s', '%s', %d, %d, '%s')"
        data = (CourseNo, CourseName, int(CreditHour), int(CourseHour), PriorCourse)
        # print(sql % data)
        self.cur.execute(sql % data)
        self.conn.commit()
        self.showClassInfo()

    def btnClicked_delete(self):
        # 获取选中行数据
        row = self.tableWidget_classinfo.selectedItems()[0].row()
        content = []
        for i in range(0,self.tableWidget_classinfo.columnCount()):
            item = self.tableWidget_classinfo.item(row,i).text()
            content.append(item)
        # print(content)
        self.toDelete_Courseno = content[0]
        self.ChildDeleteDialog.lineEdit_CourseNo.setText(content[0])
        self.ChildDeleteDialog.lineEdit_CourseName.setText(content[1])
        self.ChildDeleteDialog.lineEdit_CreditHour.setText(content[2])
        self.ChildDeleteDialog.lineEdit_CourseHour.setText(content[3])
        self.ChildDeleteDialog.lineEdit_PriorCourse.setText(content[4])
        self.ChildDeleteDialog.show()

    def btnClicked_alter(self):
        # 获取选中行数据
        row = self.tableWidget_classinfo.selectedItems()[0].row()
        content = []
        for i in range(0, self.tableWidget_classinfo.columnCount()):
            item = self.tableWidget_classinfo.item(row, i).text()
            content.append(item)
        self.ChildAlterDialog.lineEdit_CourseNo.setText(content[0])
        self.ChildAlterDialog.lineEdit_CourseName.setText(content[1])
        self.ChildAlterDialog.lineEdit_CreditHour.setText(content[2])
        self.ChildAlterDialog.lineEdit_CourseHour.setText(content[3])
        self.ChildAlterDialog.lineEdit_PriorCourse.setText(content[4])
        self.ChildAlterDialog.show()

    def slot_delete(self):
        sql = "delete from course where courseno = '%s'"
        data = self.toDelete_Courseno
        self.cur.execute(sql % data)
        self.conn.commit()
        self.showClassInfo()

    def slot_alter(self, coursename, credithour, coursehour, priorcourse, courseno):
        sql = "update course set coursename = '%s', credithour = %d, coursehour = %d, priorcourse = '%s' where courseno = '%s'"
        if (priorcourse == 'None'):
            priorcourse = ""
        data = (coursename, credithour, coursehour, priorcourse, courseno)
        # print(sql % data)
        self.cur.execute(sql % data)
        self.conn.commit()
        self.showClassInfo()

    def slot_close(self):
        self.cur.close()
        self.conn.close()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = App()
    myWin.show()
    sys.exit(app.exec_())