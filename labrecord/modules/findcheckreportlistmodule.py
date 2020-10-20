# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem

from PyQt5.QtCore import pyqtSlot

from labrecord.views.findcheckreportlist import Ui_Dialog
from labrecord.controllers.labrecordscontroller import LabrecordsController
from labrecord.modules.checkreportmodule import CheckreportModule

import datetime


class FindCheckReportModule(QDialog, Ui_Dialog):
    def __init__(self, chkid, batchno, parent=None):
        super(FindCheckReportModule, self).__init__(parent)
        self.setupUi(self)
        self.chkid = chkid
        self.batchno = batchno
        self.LC = LabrecordsController()

        self.get_report_list()

    def get_report_list(self):
        self.treeWidget_reportlist.clear()
        self.treeWidget_reportlist.hideColumn(0)
        key_dict = {
            'chkid': self.chkid,
            'batchno': self.batchno
        }
        res = self.LC.get_labrecord(False, *VALUES_TUPES_LAB, **key_dict)
        if not len(res):
            return
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_reportlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, LABTYPE[item['labtype']])
            qtreeitem.setText(2, item['paperno'])
            qtreeitem.setText(3, str(item['reportdate']) if type(
                item['reportdate']) is datetime.date else '')
            if item['status'] < 3:
                qtreeitem.setText(4, STATUS[item['status']])
            else:
                qtreeitem.setText(4, CONCLUSION[item['conclusion']])
        # for i in range(1, 5):
        #     self.treeWidget_reportlist.resizeColumnToContents(i)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_reportlist_itemDoubleClicked(self, qtreeitem, p_int):
        autoid = int(qtreeitem.text(0))
        detail = CheckreportModule(autoid, self)
        detail.show()


VALUES_TUPES_LAB = (
    'autoid', 'labtype', 'paperno', 'reportdate', 'status', 'conclusion'
)
STATUS = ('待提交', '待取样', '检验中', '合格', '不合格')
CONCLUSION = ("不合格", "其他", "合格")
LABTYPE = (
    "原料采购检验", "库存复检", "前处理检验", "半成品检验", "成品检验", "退货检验",
    "留样检验", "注射用水检验", "纯化水检验", "环境监测", "验证检验")
