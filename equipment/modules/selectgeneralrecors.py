# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt

from selfdefinedfirmat.controllers.selfdefinedformatcontroller import SelfdefinedformatController
from labrecord.views.selectoricheckpaper import Ui_Dialog


class SelectGeneralRecordsModule(QDialog, Ui_Dialog):
    selected = pyqtSignal(list)
    def __init__(self, parent=None):
        super(SelectGeneralRecordsModule, self).__init__(parent)
        self.detail = []
        self.SC = SelfdefinedformatController()
        self.setupUi(self)
        self.treeWidget_filelist.hideColumn(1)
        # 或取设备一般记录
        self.get_generalrecords()

    def get_generalrecords(self):
        res = self.SC.get_selfdefinedformat(False, *VALUES_TUPLE_SD).extra(
            where=['formtype&8']
        )
        for item in res:
            if item['subkind'] == '':
                qtreeitem = QTreeWidgetItem(self.treeWidget_filelist)
            else:
                itemlist =self.treeWidget_filelist.findItems(
                    item['subkind'], Qt.MatchContains, 0
                )
                if not len(itemlist):
                    qtreeitem_parent = QTreeWidgetItem(self.treeWidget_filelist)
                    qtreeitem_parent.setText(0, item['subkind'])
                    qtreeitem_parent.setText(1, '0')
                    qtreeitem = QTreeWidgetItem(qtreeitem_parent)
                else:
                    qtreeitem = QTreeWidgetItem(itemlist[0])
            qtreeitem.setText(0, item['formatname'])
            qtreeitem.setText(1, str(item['autoid']))


    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_filelist_itemDoubleClicked(self, qitem, p_int):
        if qitem.text(1) != '0':
            self.selected.emit([qitem.text(1),])
            self.accept()

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        items = self.treeWidget_filelist.selectedItems()
        select_list = []
        for item in items:
            if item.text(1) != '0':
                select_list.append(item.text(1))
        if len(select_list):
            self.selected.emit(select_list)
            self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

VALUES_TUPLE_SD = ('autoid', 'formatname', 'subkind')