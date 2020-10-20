# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from warehouse.views.purchaseregistration import Ui_Form

from warehouse.controllers.warehousecontroller import WarehouseController
from labrecord.controllers.labrecordscontroller import LabrecordsController
from labrecord.controllers.checkitem import CheckItem
from supplyer.controllers.supplyercontroller import SupplyerController
from stuff.controllers.stuffcontroller import StuffController
from warehouse.modules.newpurchregmodule import NewPurchRegModule
from warehouse.modules.editregstuffmodule import EditRegStuffModule
from reject.modules.applyrejectmodule import ApplyRejectModule
from labrecord.modules.applycheckmodule import ApplycheckModule

import decimal

import user


class PurchaseRegistrationModule(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(PurchaseRegistrationModule, self).__init__(parent)
        self.setupUi(self)
        self.WC = WarehouseController()
        self.LC = LabrecordsController()
        self.SC = SupplyerController()
        self.SFC = StuffController()
        self.CI = CheckItem()
        self.groupBox.setVisible(False)
        self.spid=0
        self.paperno=''
        self.supid=''
        self.supname=''

        self.get_order_list()

    def get_order_list(self):
        self.treeWidget_orderlist.clear()
        self.treeWidget_orderlist.hideColumn(0)
        index = self.tabWidget.currentIndex()
        key_dict = {'status': index, 'papertype': 0}
        order_list = self.WC.get_stuffcheckin(
            False, *VALUES_TUPLE_ORDER ,**key_dict
        )
        if not len(order_list):
            return
        for item in order_list:
            qtreeitem = QTreeWidgetItem(self.treeWidget_orderlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['paperno'])
            qtreeitem.setText(2, item['supid'] + ' ' + item['supname'])
            qtreeitem.setText(3, item['creatorid'] + ' ' + item['creatorname'])
            qtreeitem.setText(4, str(item['buydate']))
            qtreeitem.setText(5, item['buyerid'] + ' ' + item['buyername'])
            qtreeitem.setText(6, item['pppaperno'])
            qtreeitem.setText(7, item['remark'])
        for i in range(1, 8):
            self.treeWidget_orderlist.resizeColumnToContents(i)

    def get_stuff_list(self):

        self.treeWidget_stufflist.clear()
        self.treeWidget_stufflist.hideColumn(0)
        index = self.tabWidget.currentIndex()
        key_dict = {'paperno': self.paperno, 'papertype': 0}
        stuff_list = self.WC.get_stuffcheckinlist(
            False, *VALUES_TUPLE_STUFF ,**key_dict
        )
        if not len(stuff_list):
            return
        for item in stuff_list:
            qtreeitem = QTreeWidgetItem(self.treeWidget_stufflist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, STATUS[item['status']])
            qtreeitem.setText(2, item['stuffid'] + ' ' + item['stuffname'])
            qtreeitem.setText(3, item['batchno'])
            qtreeitem.setText(4, item['mbatchno'])
            qtreeitem.setText(5, STUFF_KIND[item['stufftype']])
            qtreeitem.setText(6, item['spec'])
            qtreeitem.setText(7, item['package'])
            qtreeitem.setText(8, item['position'])
            qtreeitem.setText(9, str(item['amount']))
            qtreeitem.setText(10, str(item['piamount']))
            qtreeitem.setText(11, item['unit'])
            qtreeitem.setText(12, item['producer'])
        for i in range(1, 13):
            self.treeWidget_stufflist.resizeColumnToContents(i)

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        tab = getattr(self, 'tab_' + str(p_int))
        tab.setLayout(self.gridLayout_2)
        self.groupBox.setVisible(False)
        self.get_order_list()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_orderlist_itemClicked(self, qtreeitem, p_int):
        self.groupBox.setVisible(True)

        self.paperno = qtreeitem.text(1)
        self.supid = qtreeitem.text(2).split(' ')[0]
        self.supname = qtreeitem.text(2).split(' ')[1]
        key_dict = {
            'supid': self.supid,
            'supname': self.supname
        }
        res = self.SC.get_supply(True, *VALUES_TUPLE_SUPPLYER, **key_dict)
        if len(res):
            self.spid = res[0]
        self.get_stuff_list()

    @pyqtSlot(QPoint)
    def on_treeWidget_orderlist_customContextMenuRequested(self, pos):
        id = 0
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
            # 返回调用者的对象
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is not None:
            id = int(current_item.text(0))

        menu = QMenu()
        button1 = menu.addAction("新增登记单")
        button2 = menu.addAction("设置为完成状态")
        button3 = menu.addAction("设置为其他状态")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:
            detail = NewPurchRegModule(self)
            detail.accepted.connect(self.get_order_list)
            detail.show()

        elif action == button2:
            if id is None:
                return
            key_dict = {
                'status': 1
            }
            self.WC.update_stuffcheckin(id, **key_dict)
            self.get_order_list()
        elif action == button3:
            if id is None:
                return
            key_dict = {
                'status': 2
            }
            self.WC.update_stuffcheckin(id, **key_dict)
            self.get_order_list()

    @pyqtSlot(QPoint)
    def on_treeWidget_stufflist_customContextMenuRequested(self, pos):
        id = 0
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
            # 返回调用者的对象
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is not None:
            id = int(current_item.text(0))

        menu = QMenu()
        button1 = menu.addAction("增加")
        button2 = menu.addAction("修改")
        button3 = menu.addAction("删除")
        button4 = menu.addAction("请验单")
        button5 = menu.addAction("不合格品处理申请")
        button6 = menu.addAction("不合格品处理意见")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:
            detail = EditRegStuffModule(spid=self.spid,paperno=self.paperno,parent=self)
            detail.accepted.connect(self.get_stuff_list)
            detail.show()

        elif action == button2:
            if not id:
                return
            detail = EditRegStuffModule(autoid=id, parent=self)
            detail.accepted.connect(self.get_stuff_list)
            detail.show()
        elif action == button3:
            if not id:
                return
            if current_item.text(1) not in ("登记", "请验中"):
                return
            key_dict_lab = {'autoid': id}
            lab_list = self.WC.get_stuffcheckinlist(
                True, *VALUES_TUPLE_LAB, **key_dict_lab
            )
            self.LC.delete_labrecord(list(lab_list))
            self.LC.delete_labitem(list(lab_list))
            self.WC.delete_stuffcheckinlist(id)
            self.get_stuff_list()
        elif action == button4:
            if not id:
                return
            status = current_item.text(1)
            if status not in ("登记", "请验中"):
                return
            stuffid = current_item.text(2).split(' ')[0]
            stuffname = current_item.text(2).split(' ')[1]
            key_dict = {
                'stuffid': stuffid,
                'stuffname': stuffname
            }
            checkunit = ''
            res = self.SFC.get_stuffdict(True, *VALUES_TUPLE_SD, **key_dict)
            if len(res):
                checkunit = res[0]
            key_dict_lab = {
                'ciid': id,
                'labtype':0
            }
            labrecord_list = self.LC.get_labrecord(False, **key_dict_lab)
            if not len(labrecord_list):
                kwargs = {
                    'labtype': 0,
                    'chkid': stuffid,
                    'chkname': stuffname,
                    'batchno': current_item.text(3),
                    'mbatchno': current_item.text(4),
                    'spec': current_item.text(6),
                    'package': current_item.text(7),
                    'producer': current_item.text(12),
                    'supplyer': self.supname,
                    'ciid': int(current_item.text(0)),
                    'createdate': user.now_date,
                    'checkamount': decimal.Decimal(current_item.text(9)),
                    'caunit': current_item.text(11),
                    'sampleunit': checkunit,
                    'samplesource': self.supname
                }
                labrecord = self.LC.update_labrecord(**kwargs)
                key_dict_checkitem = {'stuffid': stuffid, 'itemtype':0}
                checkitems = self.CI.get_checkitems(
                    False, *VALUES_TUPLE_CHECKITEM, **key_dict_checkitem
                )
                for item in checkitems:
                    kwargs_checkitem = {
                        'lrid': labrecord.autoid,
                        'seqid': item['seqid'],
                        'itemname': item['itemname'],
                        'kind': item['kind'],
                        'referencevalue': item['referencevalue'],
                        'labvalue': item['referencevalue'],
                        'putintype': item['putintype'],
                        'startdate': user.now_date,
                        'enddate': user.now_date,
                        'checked': 2

                    }
                    self.LC.update_labitem(**kwargs_checkitem)
            else:
                labrecord = labrecord_list[0]
            self.WC.update_stuffcheckinlist(id, lrid=labrecord.autoid)
            detail = ApplycheckModule(labrecord.autoid, self)
            detail.accepted.connect(self.get_stuff_list)
            detail.show()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_stufflist_itemDoubleClicked(self, qtreeitem, p_int):
        status = qtreeitem.text(1)
        if status != "登记":
            return
        id = int(qtreeitem.text(0))
        detail = EditRegStuffModule(autoid=id, parent=self)
        detail.accepted.connect(self.get_stuff_list)
        detail.show()

VALUES_TUPLE_SUPPLYER = ('autoid',)
VALUES_TUPLE_SD = ('checkunit',)
VALUES_TUPLE_LAB = ('lrid',)

VALUES_TUPLE_CHECKITEM = (
    'seqid', 'itemname', 'kind', 'referencevalue', 'putintype'
)


VALUES_TUPLE_ORDER = (
    'autoid', 'paperno', 'supid', 'supname', 'creatorid', 'creatorname',
    'createdate', 'buyerid', 'buyername', 'buydate', 'pppaperno', 'remark'
)

VALUES_TUPLE_STUFF = (
    'autoid', 'status', 'stuffid', 'stuffname', 'stufftype', 'batchno', 'unit',
    'mbatchno', 'spec', 'package', 'position', 'amount', 'piamount', 'producer'
)
STUFF_KIND = ("主材料", "前处理", "辅材料", "内包材", "外包材")
STATUS = ("登记", "请验中", "检验中", "合格", "不合格", "已入库", "不合格处理中",
          "不合格处理完成")