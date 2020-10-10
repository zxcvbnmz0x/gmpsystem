# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSlot

from labrecord.controllers.labrecordscontroller import LabrecordsController

from labrecord.views.sampling import Ui_Dialog

import user


class SamplingModule(QDialog, Ui_Dialog):
    def __init__(self, autoid, parent=None):
        super(SamplingModule, self).__init__(parent)
        self.autoid = autoid
        self.LC = LabrecordsController()
        self.ori_detail = dict()
        self.new_detail = dict()

        self.ori_labitemstate = []
        self.new_labitemstate = []

        self.setupUi(self)

        # 获取当前取样单的信息
        self.get_records()
        # 获取检验项目
        self.get_labrecord_item()
        # 设置样品数量校验器
        self.set_sampleamount_valitor()

    def get_records(self):
        values_list = (
            'chkid', 'chkname', 'checkamount', 'caunit', 'samplesource',
            'applyerid', 'applyername','applydate', 'sampleamount',
            'sampleunit'
            ''
        )
        key_dict = {'autoid': self.autoid}
        res = self.LC.get_labrecord(False, *values_list, **key_dict)
        if len(res):
            self.ori_detail = res[0]
            self.label_chkitem.setText(self.ori_detail['chkid'] + ' ' + self.ori_detail['chkname'])
            self.label_checkamount.setText(str(self.ori_detail['checkamount']) + self.ori_detail['caunit'])
            self.label_applyer.setText(self.ori_detail['applyerid'] + ' ' + self.ori_detail['applyername'])
            self.dateEdit_applydate.setDate(self.ori_detail['applydate'])
            self.label_sampleunit.setText(self.ori_detail['sampleunit'])
            self.dateEdit_sampledate.setDate(user.now_date)

    def set_sampleamount_valitor(self):
        doublevalitor = QDoubleValidator()
        self.lineEdit_sampleamount.setValidator(doublevalitor)

    # 获取检验项目
    def get_labrecord_item(self):
        if len(self.ori_detail):
            values_list = ('autoid', 'kind', 'itemname', 'checked')
            key_dict = {'lrid': self.autoid}
            res = self.LC.get_labitem(False, *values_list, **key_dict)
            self.ori_labitemstate = res
            if len(res):
                for item in res:
                    treeitem = QTreeWidgetItem(self.treeWidget_labitem)
                    treeitem.setText(0, str(item['autoid']))
                    treeitem.setText(1, item['kind'])
                    treeitem.setCheckState(1, item['checked'])
                    treeitem.setText(2, item['itemname'])

                self.treeWidget_labitem.hideColumn(0)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_labitem_itemDoubleClicked(self, qtreeitem, p_int):
        newstate = 0
        if qtreeitem.checkState(1) != 0:
            qtreeitem.setCheckState(1, 0)
        else:
            qtreeitem.setCheckState(1, 2)
            newstate = 2
        for item in self.ori_labitemstate:
            if int(qtreeitem.text(0)) == item['autoid']:
                if newstate != item['checked']:
                    it = {'autoid': int(qtreeitem.text(0)),
                          'checked': newstate
                          }
                    self.new_labitemstate.append(it)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_labitem_itemClicked(self, qtreeitem, p_int):
        if p_int == 1:
            newstate = qtreeitem.checkState(1)
            for item in self.ori_labitemstate:
                if int(qtreeitem.text(0)) == item['autoid']:
                    if newstate != item['checked']:
                        it = {'autoid': int(qtreeitem.text(0)),
                              'checked': newstate
                              }
                        self.new_labitemstate.append(it)

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if len(self.new_detail):
            self.new_detail['sampledate'] = self.dateEdit_sampledate.text()
            self.new_detail['samplerid'] = user.user_id
            self.new_detail['samplername'] = user.user_name
            self.new_detail['status'] = 2
            res = self.LC.update_labrecord(autoid=self.autoid, **self.new_detail)
            if len(self.new_labitemstate):
                for item in self.new_labitemstate:
                    self.LC.update_labitem(**item)
            if res:
                self.accept()

    @pyqtSlot(str)
    def on_lineEdit_sampleamount_textEdited(self, p_str):
        sampleamount = float(p_str)
        try:
            if sampleamount != self.ori_detail['sampleamount']:
                self.new_detail['sampleamount'] = sampleamount
            else:
                try:
                    del self.new_detail['sampleamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['sampleamount'] = sampleamount

    @pyqtSlot(str)
    def on_lineEdit_remark_textEdited(self, p_str):
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