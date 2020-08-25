# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QDialog, QLabel
from PyQt5.QtCore import pyqtSlot, QTimer, Qt

from cleanfirmity.views.cleanconfirmity_copy import Ui_Form
from cleanfirmity.controllers.cleanfirmitycontroller import CleanfirmityController

from lib.utils.formatdatetime import format_datetime

import user


class CleanconfirmityCopyModule(QWidget, Ui_Form):

    def __init__(self, autoid, parent=None):
        super().__init__(parent)
        self.autoid = autoid
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
            self.lineEdit_old_product.setText(self.ori_detail.lastprodid + ' ' + self.ori_detail.lastprodname)
            self.lineEdit_old_batchno.setText(self.ori_detail.lastbatchno)
            self.lineEdit_new_product.setText(self.ori_detail.prodid + ' ' + self.ori_detail.prodname)
            self.lineEdit_new_batchno.setText(self.ori_detail.batchno)
            self.pushButton_cleaner.setText(self.ori_detail.cleanerid + ' ' + self.ori_detail.cleanername)
            self.lineEdit_cleandate.setText(format_datetime(self.ori_detail.cleandate))
            self.pushButton_checker.setText(self.ori_detail.checkerid + ' ' + self.ori_detail.checkername)
            self.lineEdit_checkdate.setText(format_datetime(self.ori_detail.checkdate))
            self.lineEdit_validdate.setText(format_datetime(self.ori_detail.validdate))
            self.pushButton_sec_cleaner.setText(self.ori_detail.seccleanerid + ' ' + self.ori_detail.seccleanername)
            self.lineEdit_sec_cleandate.setText(format_datetime(self.ori_detail.seccleandate))
            self.pushButton_sec_checker.setText(self.ori_detail.seccheckerid + ' ' + self.ori_detail.seccheckername)
            self.lineEdit_sec_checkdate.setText(format_datetime(self.ori_detail.seccheckdate))

            # self.pushButton_sec_cleaner.changed.

    @pyqtSlot(str)
    def on_pushButton_sec_cleaner_signChanged(self, p_str):
        self.flat = 1
        try:
            if p_str != '':
                self.lineEdit_sec_cleandate.setText(str(user.now_date))
                self.new_detail['seccleandate'] = user.now_date
                seccleanerid, seccleanername = p_str.split(' ')
            else:
                self.lineEdit_sec_cleandate.setText('')
                self.new_detail['seccleandate'] = user.unsigndate
                seccleanerid, seccleanername = '', ''
            if seccleanerid != self.ori_detail.seccleanerid:
                self.new_detail['seccleanerid'] = seccleanerid
            else:
                try:
                    del self.new_detail['seccleanerid']
                    del self.new_detail['seccleandate']
                except KeyError:
                    pass

            if seccleanername != self.ori_detail.seccleanername:
                self.new_detail['seccleanername'] = seccleanername
            else:
                try:
                    del self.new_detail['seccleanername']
                except KeyError:
                    pass
            pass

        except ValueError:
            pass

    @pyqtSlot(str)
    def on_pushButton_sec_checker_signChanged(self, p_str):
        self.flat = 1
        try:
            if p_str != '':
                self.lineEdit_sec_checkdate.setText(str(user.now_date))
                self.new_detail['seccheckdate'] = user.now_date
                seccheckerid, seccheckername = p_str.split(' ')
            else:
                self.lineEdit_sec_checkdate.setText('')
                self.new_detail['seccheckdate'] = user.unsigndate
                seccheckerid, seccheckername = '', ''
            if seccheckerid != self.ori_detail.seccheckerid:
                self.new_detail['seccheckerid'] = seccheckerid
            else:
                try:
                    del self.new_detail['seccheckerid']
                    del self.new_detail['seccheckdate   ']
                except KeyError:
                    pass

            if seccheckername != self.ori_detail.seccheckername:
                self.new_detail['seccheckername'] = seccheckername
            else:
                try:
                    del self.new_detail['seccheckername']
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
                #dialog = QDialog(self)
                #dialog.resize(200, 200)
                #dialog.setWindowTitle("提示")

                label.setText('<font color="blue" opacity="0.3" size=140><b>保存成功！</b></font>')
            else:
                label.setText('<font color="red" opacity="0.3" size=140><b>保存失败！请重试</b></font>')

            label.show()
            QTimer.singleShot(1000, label.close)
