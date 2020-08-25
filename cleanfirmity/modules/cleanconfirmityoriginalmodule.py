# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QDialog, QLabel
from PyQt5.QtCore import pyqtSlot, QTimer, Qt

from cleanfirmity.views.cleanconfirmity_original import Ui_Form
from cleanfirmity.controllers.cleanfirmitycontroller import CleanfirmityController

from lib.utils.formatdatetime import format_datetime

import user
import _datetime

class CleanconfirmityOriginalModule(QWidget, Ui_Form):

    def __init__(self, autoid, validdate, parent=None):
        super().__init__(parent)
        self.autoid = autoid
        self.validdate = _datetime.timedelta(days=int(validdate))
        self.flat = 0
        self.setupUi(self)
        self.ori_detail = {}
        self.new_detail = {}

        self.CC = CleanfirmityController()
        self.get_data()

    def get_data(self):
        res = self.CC.get_confirmity(self.autoid)

        if len(res):
            self.ori_detail = res[0]
            print(self.ori_detail)
            self.lineEdit_roomname.setText(self.ori_detail.roomname)
            self.lineEdit_postname.setText(self.ori_detail.linepostname)

            self.lineEdit_product.setText(self.ori_detail.prodid + ' ' + self.ori_detail.prodname)
            self.lineEdit_batchno.setText(self.ori_detail.batchno)
            self.pushButton_cleaner.setText(self.ori_detail.cleanerid + ' ' + self.ori_detail.cleanername)
            self.lineEdit_cleandate.setText(format_datetime(self.ori_detail.cleandate))
            self.pushButton_checker.setText(self.ori_detail.checkerid + ' ' + self.ori_detail.checkername)
            self.lineEdit_checkdate.setText(format_datetime(self.ori_detail.checkdate))
            self.lineEdit_validdate.setText(format_datetime(self.ori_detail.validdate))


    @pyqtSlot(str)
    def on_pushButton_cleaner_signChanged(self, p_str):
        self.flat = 1
        try:
            if p_str != '':
                self.lineEdit_cleandate.setText(str(user.now_date))
                self.new_detail['cleandate'] = user.now_date
                self.new_detail['validdate'] = user.now_date + self.validdate
                cleanerid, cleanername = p_str.split(' ')
            else:
                self.lineEdit_cleandate.setText('')
                self.new_detail['cleandate'] = user.unsigndate
                cleanerid, cleanername = '', ''
            if cleanerid != self.ori_detail.cleanerid:
                self.new_detail['cleanerid'] = cleanerid
            else:
                try:
                    del self.new_detail['cleanerid']
                    del self.new_detail['cleandate']
                except KeyError:
                    pass

            if cleanername != self.ori_detail.cleanername:
                self.new_detail['cleanername'] = cleanername
            else:
                try:
                    del self.new_detail['cleanername']
                except KeyError:
                    pass
            pass

        except ValueError:
            pass

    @pyqtSlot(str)
    def on_pushButton_checker_signChanged(self, p_str):
        self.flat = 1
        try:
            if p_str != '':
                self.lineEdit_checkdate.setText(str(user.now_date))
                self.new_detail['checkdate'] = user.now_date
                checkerid, checkername = p_str.split(' ')
            else:
                self.lineEdit_checkdate.setText('')
                self.new_detail['checkdate'] = user.unsigndate
                checkerid, checkername = '', ''
            if checkerid != self.ori_detail.checkerid:
                self.new_detail['checkerid'] = checkerid
            else:
                try:
                    del self.new_detail['checkerid']
                    del self.new_detail['checkdate']
                except KeyError:
                    pass

            if checkername != self.ori_detail.checkername:
                self.new_detail['checkername'] = checkername
            else:
                try:
                    del self.new_detail['checkername']
                except KeyError:
                    pass
            pass

        except ValueError:
            pass

    def get_new_detail(self):
        return self.new_detail

    def save(self):
        if len(self.new_detail):
            condition = {'autoid': self.autoid}
            res = self.CC.update_confirmity(condition, **self.new_detail)
            label = QLabel(self)
            label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
            if res:
                self.flat = 0
                label.setText('<font color="blue" opacity="0.3" size=140><b>保存成功！</b></font>')
            else:
                label.setText('<font color="red" opacity="0.3" size=140><b>保存失败！请重试</b></font>')

            label.show()
            QTimer.singleShot(1000, label.close)
