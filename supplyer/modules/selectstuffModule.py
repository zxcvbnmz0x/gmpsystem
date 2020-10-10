# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from supplyer.controllers.supplyercontroller import SupplyerController
from stuff.controllers.stuffcontroller import StuffController
from supplyer.views.selectstuff import Ui_Dialog


class SelectstuffModule(QDialog, Ui_Dialog):
    selected = pyqtSignal(int)

    def __init__(self, spid, parent=None):
        super(SelectstuffModule, self).__init__(parent)
        self.setupUi(self)
        self.spid = spid
        self.SC = SupplyerController()
        self.SFC = StuffController()

        self.get_stufflist()

    def get_stufflist(self):
        self.treeWidget_stufflist.clear()
        self.treeWidget_stufflist.hideColumn(0)
        key_dict = {
            'spid': self.spid
        }
        id_list = self.SC.get_stuffsupplyer(True, *VALUES_TUPLES_SD, **key_dict)
        if not len(id_list):
            return
        key_dict_stuff = {
            'autoid__in': id_list
        }
        res = self.SFC.get_stuffdict(False, *VALUES_TUPLES_STUFF, **key_dict_stuff)

        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_stufflist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['stuffid'])
            qtreeitem.setText(2, item['stuffname'])
            qtreeitem.setText(3, item['spec'])
            qtreeitem.setText(4, item['package'])

        for i in range(1, 5):
            self.treeWidget_stufflist.resizeColumnToContents(i)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_stufflist_itemDoubleClicked(self, qtreeitem, p_int):
        self.selected.emit(int(qtreeitem.text(0)))
        self.accept()

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        current_item = self.treeWidget_stufflist.currentItem()
        if current_item is not None:
            self.selected.emit(int(current_item.text(0)))
            self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

VALUES_TUPLES_SD = ('sdid',)
VALUES_TUPLES_STUFF = ('autoid', 'stuffid', 'stuffname', 'spec', 'package')