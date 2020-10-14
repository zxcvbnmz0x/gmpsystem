# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from warehouse.views.purstuffcheckin import Ui_Form

from warehouse.controllers.warehousecontroller import WarehouseController
from labrecord.controllers.labrecordscontroller import LabrecordsController
from supplyer.controllers.supplyercontroller import SupplyerController
from stuff.controllers.stuffcontroller import StuffController
from warehouse.modules.editstuffcheckin import EditStuffCheckInModule
from warehouse.modules.editregstuffmodule import EditRegStuffModule
from labrecord.modules.checkreportmodule import CheckreportModule
from labrecord.modules.applycheckmodule import ApplycheckModule

from lib.utils.messagebox import MessageBox

import decimal

import user


class PurStuffCheckInModule(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(PurStuffCheckInModule, self).__init__(parent)
        self.setupUi(self)
        self.WC = WarehouseController()
        self.LC = LabrecordsController()
        self.SC = SupplyerController()
        self.SFC = StuffController()

        self.get_stuff_list()

    def get_stuff_list(self):

        self.treeWidget_stufflist.clear()
        self.treeWidget_stufflist.hideColumn(0)
        key_dict = {'status': 3, 'papertype': 0}
        stuff_list = self.WC.get_stuffcheckinlist(
            False, *VALUES_TUPLE_STUFF ,**key_dict
        )
        if not len(stuff_list):
            return
        for item in stuff_list:
            qtreeitem = QTreeWidgetItem(self.treeWidget_stufflist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, str(item['lrid']))
            qtreeitem.setText(2, STUFF_KIND[item['stufftype']])
            qtreeitem.setText(3, item['stuffid'] + ' ' + item['stuffname'])
            qtreeitem.setText(4, item['batchno'])
            qtreeitem.setText(5, item['mbatchno'])
            qtreeitem.setText(6, item['spec'])
            qtreeitem.setText(7, item['package'])
            qtreeitem.setText(8, str(item['amount']))
            qtreeitem.setText(9, item['unit'])
            qtreeitem.setText(10, item['supid'] + ' ' + item['supname'])
            qtreeitem.setText(11, item['producer'])
        for i in range(1, 12):
            self.treeWidget_stufflist.resizeColumnToContents(i)

    @pyqtSlot(QPoint)
    def on_treeWidget_stufflist_customContextMenuRequested(self, pos):
        id = 0
        lrid = 0
        # 返回调用者的对象
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is None:
            return

        id = int(current_item.text(0))
        lrid = int(current_item.text(1))

        menu = QMenu()
        button1 = menu.addAction("登记入库")
        button2 = menu.addAction("查看检验报告")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:
            detail = EditStuffCheckInModule(id, lrid, self)
            detail.accepted.connect(self.get_stuff_list)
            detail.show()

        elif action == button2:
            if lrid == 0:
                message = MessageBox(text="没有找到对应的检验报告", parent=self)
                message.show()
                return
            detail = CheckreportModule(lrid, self)
            detail.show()


    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_stufflist_itemDoubleClicked(self, qtreeitem, p_int):

        id = int(qtreeitem.text(0))
        lrid = int(qtreeitem.text(1))
        detail = EditStuffCheckInModule(id, lrid, self)
        detail.accepted.connect(self.get_stuff_list)
        detail.show()

VALUES_TUPLE_SUPPLYER = ('autoid',)
VALUES_TUPLE_SD = ('checkunit',)

VALUES_TUPLE_ORDER = (
    'autoid', 'paperno', 'supid', 'supname', 'creatorid', 'creatorname',
    'createdate', 'buyerid', 'buyername', 'buydate', 'pppaperno', 'remark'
)

VALUES_TUPLE_STUFF = (
    'autoid', 'lrid', 'stuffid', 'stuffname', 'stufftype', 'batchno', 'unit',
    'mbatchno', 'spec', 'package', 'amount', 'producer', 'supid', 'supname'
)
STUFF_KIND = ("主材料", "前处理", "辅材料", "内包材", "外包材")
STATUS = ("登记", "请验中", "检验中", "合格", "不合格", "已入库", "不合格处理中",
          "不合格处理完成")