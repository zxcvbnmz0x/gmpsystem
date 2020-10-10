# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt

from labrecord.controllers.labrecordscontroller import LabrecordsController
from labrecord.views.selectoricheckpaper import Ui_Dialog


class SelectoricheckpaperModule(QDialog, Ui_Dialog):
    selected = pyqtSignal(list)
    def __init__(self, dictid, itemtype, parent=None):
        super(SelectoricheckpaperModule, self).__init__(parent)
        self.detail = []
        self.LC = LabrecordsController()
        self.setupUi(self)
        # 或取当前检品的检验报告列表
        self.get_oricheckpaper(dictid, itemtype)

    def get_oricheckpaper(self, dictid, itemtype):
        res = self.LC.select_oricheckpaper(dictid, itemtype)
        for item in res:
            if item['kind'] == '':
                qtreeitem = QTreeWidgetItem(self.treeWidget_filelist)
            else:
                itemlist =self.treeWidget_filelist.findItems(item['kind'], Qt.MatchContains, 1)
                if not len(itemlist):
                    qtreeitem_parent = QTreeWidgetItem(self.treeWidget_filelist)
                    qtreeitem_parent.setText(0, item['kind'])
                    qtreeitem_parent.setText(1, '0')
                    qtreeitem = QTreeWidgetItem(qtreeitem_parent)
                else:
                    qtreeitem = QTreeWidgetItem(itemlist[0])
            qtreeitem.setText(0, item['formatname'])
            qtreeitem.setText(1, str(item['autoid']))
        self.treeWidget_filelist.hideColumn(1)

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