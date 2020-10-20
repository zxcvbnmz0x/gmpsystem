# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QDate

from supplyer.views.editpurchasingplan import Ui_Dialog

from supplyer.controllers.supplyercontroller import SupplyerController

from lib.utils.messagebox import MessageBox

import user

import datetime
import re


class EditpurchasingplanModule(QDialog, Ui_Dialog):

    def __init__(self, autoid=None, parent=None):
        super(EditpurchasingplanModule, self).__init__(parent)
        self.ori_detail = dict()
        self.new_detail = dict()
        self.SC = SupplyerController()
        self.setupUi(self)
        row = ('autoid', 'supid', 'supname')
        key = ('supid', 'supname', 'inputcode')
        row_name = ("id", "供应商编号", "供应商名称")
        self.lineEdit_supplyer.setup('Supplyer', row, key, row_name, 539, 240)

        self.autoid = autoid

        self.get_detail()

    def get_detail(self):
        if not self.autoid:
            self.pushButton_creator.setSign(user.user_id + ' ' + user.user_name)
            self.dateEdit_createdate.setDate(user.now_date)
            self.dateEdit_invaliddate.setDate(
                user.now_date + datetime.timedelta(weeks=4)
            )
            self.lineEdit_paperno.setText(self.get_max_paperno())
            return
        key_dict = {
            'autoid': self.autoid
        }
        res = self.SC.get_purchasingplan(False, *VALUES_TUPLE, **key_dict)
        if len(res) != 1:
            return
        self.ori_detail = res[0]
        self.lineEdit_paperno.setText(self.ori_detail['paperno'])
        self.lineEdit_supplyer.setText(
            self.ori_detail['supid'] + ' ' + self.ori_detail['supname']
        )
        self.pushButton_creator.setSign(
            self.ori_detail['creatorid'] + ' ' + self.ori_detail['creatorname']
        )
        self.dateEdit_createdate.setDate(self.ori_detail['createdate'])
        self.dateEdit_invaliddate.setDate(self.ori_detail['invaliddate'])
        self.lineEdit_remark.setText(self.ori_detail['remark'])
        self.pushButton_warrantor.setSign(
            self.ori_detail['warrantorid'] + ' ' + self.ori_detail[
                'warrantorname']
        )

    def get_max_paperno(self):
        res = self.SC.get_purchasingplan(True, *VALUES_TUPLE_PAPERNO)
        if not len(res):
            return ''
        max_paperno = res.order_by('-paperno')[0]
        num = re.findall('\d+', max_paperno)[-1]
        new_num = str(int(num) + 1)
        i = len(new_num)
        while i < len(num):
            new_num = '0' + new_num
            i += 1

        return max_paperno.replace(num, new_num)


    @pyqtSlot(str)
    def on_lineEdit_paperno_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['paperno']:
                self.new_detail['paperno'] = p_str
            else:
                try:
                    del self.new_detail['paperno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['paperno'] = p_str

    @pyqtSlot(object)
    def on_lineEdit_supplyer_getItem(self, p_obj):
        id = p_obj.text(1)
        name = p_obj.text(2)
        spid = 0
        if id not in ('', ' '):
            key_dict = {'supid': id, 'supname': name}
            res = self.SC.get_supply(True, *VALUES_TUPLE_SUPPLYER, **key_dict)
            if len(res):
                spid = res[0]
        try:
            if id != self.ori_detail['supid'] or name != self.ori_detail[
                'supname']:
                self.new_detail['supid'] = id
                self.new_detail['supname'] = name
                self.new_detail['spid'] = spid
            else:
                try:
                    del self.new_detail['supid']
                    del self.new_detail['supname']
                    del self.new_detail['spid']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['supid'] = id
            self.new_detail['supname'] = name
            self.new_detail['spid'] = spid

    @pyqtSlot(str)
    def on_pushButton_creator_signChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['creatorid'] or name != self.ori_detail[
                'creatorname']:
                self.new_detail['creatorid'] = id
                self.new_detail['creatorname'] = name
            else:
                try:
                    del self.new_detail['creatorid']
                    del self.new_detail['creatorname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['creatorid'] = id
            self.new_detail['creatorname'] = name

    @pyqtSlot(QDate)
    def on_dateEdit_createdate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['createdate']) is str:
                self.new_detail['createdate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['createdate']):
                self.new_detail['createdate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['createdate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['createdate'] = q_date.toPyDate()

    @pyqtSlot(QDate)
    def on_dateEdit_invaliddate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['invaliddate']) is str:
                self.new_detail['invaliddate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['invaliddate']):
                self.new_detail['invaliddate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['invaliddate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['invaliddate'] = q_date.toPyDate()

    @pyqtSlot(str)
    def on_lineEdit_remark_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['remark']:
                self.new_detail['remark'] = p_str
            else:
                try:
                    del self.new_detail['remark']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['remark'] = p_str

    @pyqtSlot(str)
    def on_pushButton_warrantor_signChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['warrantorid'] or name != self.ori_detail[
                'warrantorname']:
                self.new_detail['warrantorid'] = id
                self.new_detail['warrantorname'] = name
            else:
                try:
                    del self.new_detail['warrantorid']
                    del self.new_detail['warrantorname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['warrantorid'] = id
            self.new_detail['warrantorname'] = name

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if 'paperno' in self.new_detail:
            key_dict = {
                'paperno': self.new_detail['paperno']
            }
            res = self.SC.get_purchasingplan(
                True, *VALUES_TUPLE_PAPERNO, **key_dict
            )
            if len(res) > 0:
                message = MessageBox(
                    self, text="单号重复，请修改后重新提交",
                    informative="已经存在单号为" + self.new_detail['paperno'] +
                                "的记录了！"
                )
                message.show()
                self.lineEdit_paperno.setFocus()
                return
        if len(self.new_detail):
            res = self.SC.update_purchasingplan(self.autoid, **self.new_detail)
            self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

VALUES_TUPLE_SUPPLYER = ('autoid',)
VALUES_TUPLE_PAPERNO = ('paperno',)

VALUES_TUPLE = (
    "autoid", "paperno", "createdate", "creatorid", "creatorname", "supid",
    "supname", "warrantorid", "warrantorname", "remark", "invaliddate"
)
