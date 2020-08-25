# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signmodule.py'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from hashlib import md5

from db.models import Clerks
from django.db.models import Q

from lib.sign.sign import Ui_Dialog


class SignModule(QDialog, Ui_Dialog):
    userchanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SignModule, self).__init__(parent)
        self.setupUi(self)
        # 修改名字标记，0：未签名可以随意修改名字，1：已签名，不允许修改名字
        self.flat = 0
        # 签名标记，0：签名，1：取消签名
        self.sign = 0
        self.tipslabel.setVisible(False)
        self.username.setup('Clerks', ('clerkid', 'pid', 'clerkname'), ('pid', 'clerkname'),['id', '编号', '姓名'])
        self.username.namelist.resize(180, 130)
    
    def exec(self):
        self.password.clear()
        self.tipslabel.setVisible(False)
        self.RadioButton_sign.setChecked(True)
        self.RadioButton_unsign.setChecked(False)
        self.username.namelist.resize(180, 130)

        if len(self.username.text()):
            self.password.setFocus()
        else:
            self.username.setFocus()
        super(SignModule, self).exec()


    @pyqtSlot()
    def on_acceptButton_clicked(self):
        p_str = self.username.text()
        password = self.password.text()
        md = md5()
        md.update(password.encode(encoding='utf-8'))
        token = md.hexdigest()
        try:
            pid, clerkname = p_str.split(' ')
            res = Clerks.objects.filter(pid=pid, clerkname=clerkname, password=token)
            # 必须只能返回一条结果
            if len(res) == 1:
                # 返回结果的clerkid和当前选中的名称的clerkid必须一致
                #if str(res[0].clerkid) == self.username.namelist.currentItem().text(0):
                if self.sign == 0:
                    # 签名
                    self.userchanged.emit(p_str)
                    self.flat = 1
                    self.username.setEnabled(False)

                else:
                    self.userchanged.emit('')
                    self.flat = 0
                    self.username.setEnabled(True)
                self.close()
            else:
                self.tipslabel.setVisible(True)
        except (ValueError, AttributeError):
            self.close()


    @pyqtSlot()
    def on_cancelButton_clicked(self):
        self.close()

    @pyqtSlot()
    def on_RadioButton_sign_clicked(self):
        self.sign = 0

    @pyqtSlot()
    def on_RadioButton_unsign_clicked(self):
        self.sign = 1