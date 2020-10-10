# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QWidget

from PyQt5.QtCore import Qt, pyqtSlot
from workshop.controllers.workshopcontroller import WorkshopController

from workshop.modules.scanqrcodemodule import ScanqrcodeModule

from workshop.views.qrcodelist import Ui_Form


class QrcodelistModule(QWidget, Ui_Form):

    def __init__(self, ppid, parent=None):
        super(QrcodelistModule, self).__init__(parent)
        self.setupUi(self)

        self.ppid = ppid
        self.WC = WorkshopController()

        # 获取现有的二维码列表
        self.get_qrcode_list()

    def get_qrcode_list(self):
        self.treeWidget_qrcode.clear()
        self.treeWidget_qrcode.hideColumn(1)
        self.treeWidget_qrcode.hideColumn(2)
        value_list = ('autoid', 'qrcode0', 'qrcode1', 'qrcode2', 'qrcode3')
        key_dict = {
            'ppid': self.ppid
        }
        res = self.WC.get_prodqrcode(False, *value_list, **key_dict)
        if not len(res):
            return
        for item in res:
            self.add_qrcode_to_treewidget(item)
        self.treeWidget_qrcode.resizeColumnToContents(0)

    def add_qrcode_to_treewidget(self, item, i=0):
        # i：二维码级别，默认为0，巨包装二维码，3为小包装二维码

        if i == 3:
            qtreeitem = QTreeWidgetItem(self.treeWidget_qrcode)
            qtreeitem.setText(0, item['qrcode3'])
            qtreeitem.setText(1, str(item['autoid']))
            qtreeitem.setText(2, '3')
            return qtreeitem

        qrcode = item['qrcode' + str(i)]
        qrcode_parent = item['qrcode' + str(i + 1)]
        # 上一级包装码不为空
        if qrcode_parent != '':
            # 检查是否已经存上级二维码
            match_list_qr = self.treeWidget_qrcode.findItems(
                qrcode_parent, Qt.MatchFixedString | Qt.MatchRecursive, 0
            )
            # 如果不存在且上一级包装码
            if not len(match_list_qr):
                new_parent = self.add_qrcode_to_treewidget(item, i=i+1)
                qtreeitem = QTreeWidgetItem(new_parent)
            else:
                qtreeitem = QTreeWidgetItem(match_list_qr[0])
        else:
            qtreeitem = QTreeWidgetItem(self.treeWidget_qrcode)
        qtreeitem.setText(0, qrcode)
        qtreeitem.setText(1, str(item['autoid']))
        qtreeitem.setText(2, str(i))
        return qtreeitem

    @pyqtSlot()
    def on_pushButton_scanqrcode_clicked(self):
        detail = ScanqrcodeModule(self.ppid, self)
        detail.applyed.connect(self.addqrcode)
        detail.show()

    @pyqtSlot()
    def on_pushButton_deleteqrcode_clicked(self):
        pass

    @pyqtSlot()
    def on_pushButtonchangeqrcode_clicked(self):
        pass

    def addqrcode(self, q_list, batchno):
        for item in q_list:
            detail = {
                'ppid': self.ppid,
                'qrcode0': item[0],
                'qrcode1': item[1],
                'qrcode2': item[2],
                'qrcode3': item[3],
                'batchno': batchno
            }
            self.WC.update_prodqrcode(**detail)
            self.get_qrcode_list()