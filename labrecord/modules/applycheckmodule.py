# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot

from labrecord.controllers.labrecordscontroller import LabrecordsController
from labrecord.views.applycheck import Ui_dialog

import user

STATUS = ('待提交', '待取样', '检验中', '已完成')

class ApplycheckModule(QDialog, Ui_dialog):

    def __init__(self, autoid, parent=None):
        # autoid :labrecords里的autoid
        super(ApplycheckModule, self).__init__(parent)
        self.setupUi(self)
        self.autoid = autoid
        # 请验单内容
        self.ori_detail = dict()
        self.new_detail = dict()
        self.ori_labitemstate = []
        self.new_labitemstate = []
        self.LC = LabrecordsController()

        # 获取请验单的状态
        self.get_labreord_detail()
        # 获取来源的下拉内容
        self.get_applysourcelist()
        # 获取检验项目
        self.get_labrecord_item()

    """
    def show(self):
        if len(self.ori_detail):
            # 如果找不到对应的检验记录则不显示内容
            super(ApplycheckModule, self).show()
    """

    # 获取检验记录
    def get_labreord_detail(self):
        values_list = ('autoid', 'chkid', 'checkamount', 'caunit', 'samplesource', 'applyremark', 'status')
        key_dict = {'autoid': self.autoid}
        res = self.LC.get_labrecord(0, *values_list, **key_dict)
        if len(res):
            self.ori_detail = res[0]
            self.lineEdit_checkamount.setText(str(self.ori_detail['checkamount']))
            self.label_checkunit.setText(self.ori_detail['caunit'])
            self.lineEdit_applyremark.setText(self.ori_detail['applyremark'])
            self.label_status.setText(STATUS[self.ori_detail['status']])
            if self.ori_detail['status'] == 0:
                self.pushButton_apply.setVisible(True)
                self.pushButton_cancel.setVisible(False)
            elif self.ori_detail['status'] == 1:
                self.pushButton_apply.setVisible(False)
                self.pushButton_cancel.setVisible(True)
            else:
                self.pushButton_apply.setVisible(False)
                self.pushButton_cancel.setVisible(False)

    # 获取来源的选项
    def get_applysourcelist(self):
        value_list = ('samplesource',)
        key_dict = {'chkid': self.ori_detail['chkid']}
        res = self.LC.get_labrecord(True, *value_list, **key_dict)
        if len(res):
            self.comboBox_samplesource.addItems(res.distinct())
        self.comboBox_samplesource.setCurrentText(
            self.ori_detail['samplesource'])

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

    @pyqtSlot()
    def on_pushButton_apply_clicked(self):
        try:
            if self.ori_detail['status'] != 0:
                return ''
            else:
                self.new_detail['status'] = 1
        except KeyError:
            self.new_detail['status'] = 1
        finally:
            self.new_detail['applyerid'] = user.user_id
            self.new_detail['applyername'] = user.user_name
            self.new_detail['applydate'] = user.now_date
            res = self.LC.update_labrecord(autoid=self.autoid, **self.new_detail)
            if len(self.new_labitemstate):
                for item in self.new_labitemstate:
                    self.LC.update_labitem(**item)
            if res:
                self.ori_detail['status'] = 1
                self.pushButton_cancel.setVisible(True)
                self.pushButton_apply.setVisible(False)
                self.label_status.setText(STATUS[1])
                self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        try:
            if self.ori_detail['status'] != 1:
                return ''
            else:
                self.new_detail['status'] = 0
        except KeyError:
            self.new_detail['status'] = 0
        finally:
            self.new_detail['applyerid'] = ''
            self.new_detail['applyername'] = ''
            self.new_detail['applydate'] = None
            res = self.LC.update_labrecord(autoid=self.autoid, **self.new_detail)
            if res:
                self.ori_detail['status'] = 0
                self.pushButton_cancel.setVisible(False)
                self.pushButton_apply.setVisible(True)
                self.label_status.setText(STATUS[0])

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

    @pyqtSlot(str)
    def on_lineEdit_checkamount_textEdited(self, p_str):
        checkamount = float(p_str)
        try:
            if checkamount != self.ori_detail['checkamount']:
                self.new_detail['checkamount'] = checkamount
            else:
                try:
                    del self.new_detail['checkamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['checkamount'] = checkamount

    @pyqtSlot(str)
    def on_comboBox_samplesource_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['samplesource']:
                self.new_detail['samplesource'] = p_str
            else:
                try:
                    del self.new_detail['samplesource']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['samplesource'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_applyremark_textEdited(self, p_str):
        try:
            if p_str != self.ori_detail['applyremark']:
                self.new_detail['applyremark'] = p_str
            else:
                try:
                    del self.new_detail['applyremark']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['applyremark'] = p_str

