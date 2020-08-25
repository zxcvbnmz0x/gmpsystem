# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot

from labrecord.controllers.labrecordscontroller import LabrecordsController
from labrecord.views.applycheck import Ui_dialog

STATUS = ('待提交', '待取样', '检验中', '已完成')

class ApplycheckModule(QDialog, Ui_dialog):

    def __init__(self, autoid, parent=None):
        # autoid :labrecords里的autoid
        super(ApplycheckModule, self).__init__(parent)
        self.setupUi(self)
        self.autoid = autoid
        # 请验单内容
        self.detail = dict()
        self.new_detail = dict()
        self.LC = LabrecordsController()
        # 获取请验单的状态
        self.get_labreord_detail()
        # 获取检验项目
        self.get_labrecord_item()
    
    def show(self):
        if len(self.detail):
            # 如果找不到对应的检验记录则不显示内容
            super(ApplycheckModule, self).show()

    # 获取检验记录
    def get_labreord_detail(self):
        values_list = ('autoid', 'checkamount', 'caunit', 'samplesource', 'applyremark', 'status')
        key_dict = {'autoid': self.autoid}
        res = self.LC.get_labrecord(0, *values_list, **key_dict)
        if len(res):
            self.detail = res[0]
            self.lineEdit_checkamount.setText(str(self.detail['checkamount']))
            self.label_checkunit.setText(self.detail['caunit'])
            self.comboBox_samplesource.setCurrentText(self.detail['samplesource'])
            self.lineEdit_applyremark.setText(self.detail['applyremark'])
            self.label_status.setText(STATUS[self.detail['status']])
            if self.detail['status'] == 0:
                self.pushButton_apply.setVisible(True)
                self.pushButton_cancel.setVisible(False)
            elif self.detail['status'] == 1:
                self.pushButton_apply.setVisible(False)
                self.pushButton_cancel.setVisible(True)
            else:
                self.pushButton_apply.setVisible(False)
                self.pushButton_cancel.setVisible(False)

    # 获取检验项目
    def get_labrecord_item(self):
        if len(self.detail):
            values_list = ('autoid', 'kind', 'itemname', 'checked')
            key_dict = {'lrid': self.autoid}
            res = self.LC.get_labitem(0, *values_list, **key_dict)
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
        pass

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        pass

    @pyqtSlot()
    def on_treeWidget_labitem_itemDoubleClicked(self):
        pass

    @pyqtSlot()
    def on_lineEdit_checkamount_textEdited(self, p_str):
        checkamount = int(p_str)
        try:
            if checkamount != self.oridetail['checkamount']:
                self.new_detail['checkamount'] = checkamount
            else:
                try:
                    del self.new_detail['checkamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['checkamount'] = checkamount


    @pyqtSlot()
    def on_comboBox_samplesource_currentTextChanged(self):
        pass
        print("adds")


    @pyqtSlot()
    def on_lineEdit_applyremark_textEdited(self):
        pass

