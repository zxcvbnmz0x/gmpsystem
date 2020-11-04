# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from equipment.controllers.equipmentcontroller import EquipmentController

from equipment.views.generalrecord import Ui_Dialog

from lib.xmlwidget.xmlreadwrite import XMLReadWrite


class GeneralRecordModule(QDialog, Ui_Dialog):
    edited = pyqtSignal(int)

    def __init__(self, autoid, parent=None):
        super(GeneralRecordModule, self).__init__(parent)
        self.ori_detail = dict()
        self.autoid = autoid
        self.EC = EquipmentController()
        self.current_content = object
        self.setupUi(self)
        # 获取记录内容
        self.get_general_record()

    def get_general_record(self):
        values_list = ('formname', 'format')
        key_dict = {
            'autoid': self.autoid
        }
        res = self.EC.get_data(5, False, *values_list, **key_dict)
        if len(res):
            self.label_formname.setText(res[0]['formname'])
            ori_paper = res[0]['format']
            self.current_content = XMLReadWrite(self)
            self.current_content.openxml(ori_paper)
            self.gridLayout_6.addWidget(self.current_content)
            self.current_content.__setattr__('autoid', self.autoid)

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        condition = {'autoid': self.autoid}
        kwargs = {'formcontent': self.current_content.get_content()}
        res = self.EC.update_data(5, condition, **kwargs)
        if res:
            self.current_content.flat = 0
            self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.current_content.flat=0
        self.close()
