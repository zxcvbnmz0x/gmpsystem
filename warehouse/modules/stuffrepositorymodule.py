# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from warehouse.views.stuffrepository import Ui_Form

from warehouse.controllers.warehousecontroller import WarehouseController
from labrecord.controllers.labrecordscontroller import LabrecordsController

from stuff.controllers.stuffcontroller import StuffController
from warehouse.modules.modifystuffparametermodule import ModifyStuffParmeter
from labrecord.modules.findcheckreportlistmodule import FindCheckReportModule
from labrecord.modules.applycheckmodule import ApplycheckModule
from labrecord.controllers.checkitem import CheckItem

from django.db.models import Sum

import decimal

import user


class StuffRepositoryModule(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(StuffRepositoryModule, self).__init__(parent)
        self.setupUi(self)
        self.WC = WarehouseController()
        self.CI = CheckItem()
        self.LC = LabrecordsController()
        self.SFC = StuffController()
        self.current_button = self.radioButton_batchno
        self.get_stuff_list()

    def get_stuff_list(self):
        if self.current_button == self.radioButton_batchno:
            values_tuple = VALUES_TUPLE_BATCHNO
            self.treeWidget_stuffbatchnolist.setVisible(True)
            self.treeWidget_stuffkindlist.setVisible(False)
            current_tree = self.treeWidget_stuffbatchnolist
            current_tree.hideColumn(0)
            current_tree.hideColumn(1)
        elif self.current_button == self.radioButton_kind:
            values_tuple = VALUES_TUPLE_KIND
            self.treeWidget_stuffbatchnolist.setVisible(False)
            self.treeWidget_stuffkindlist.setVisible(True)
            current_tree = self.treeWidget_stuffkindlist
        else:
            return

        current_tree.clear()
        index = self.tabWidget.currentIndex()
        key_dict = {'amount__gt': 0}
        if index != 0:
            key_dict['stufftype'] = index - 1
        stuff_list = self.WC.get_stuffrepository(
            False, *values_tuple, **key_dict
        )
        if not len(stuff_list):
            return
        if current_tree == self.treeWidget_stuffbatchnolist:
            self.set_batchno_tree(current_tree, stuff_list)
            for i in range(2, 25):
                current_tree.resizeColumnToContents(i)
        elif current_tree == self.treeWidget_stuffkindlist:
            self.set_kind_tree(current_tree, stuff_list)
            for i in range(0, 3):
                current_tree.resizeColumnToContents(i)
        else:
            return

    def set_batchno_tree(self, current_tree, stuff_list):
        for item in stuff_list:
            qtreeitem = QTreeWidgetItem(current_tree)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, str(item['lrid']))
            qtreeitem.setText(2, STATUS[item['status']])
            qtreeitem.setText(3, item['stuffid'] + ' ' + item['stuffname'])
            qtreeitem.setText(4, item['stuffkind'])
            qtreeitem.setText(5, STUFF_KIND[item['stufftype']])
            qtreeitem.setText(6, item['batchno'])
            qtreeitem.setText(7, item['mbatchno'])
            qtreeitem.setText(8, item['spec'])
            qtreeitem.setText(9, item['package'])
            qtreeitem.setText(10, str(item['piamount']))
            qtreeitem.setText(11, str(item['amount']))
            qtreeitem.setText(12, item['basicunit'])
            qtreeitem.setText(13, item['position'])
            qtreeitem.setText(14, str(item['makedate']))
            qtreeitem.setText(15, str(item['putindate']))
            qtreeitem.setText(16, str(item['expireddate']))
            qtreeitem.setText(17, str(item['nextcheckdate']))
            qtreeitem.setText(18, item['supid'] + ' ' + item['supname'])
            qtreeitem.setText(19, item['producer'])
            qtreeitem.setText(20, str(item['content']) + item['cunit'])
            qtreeitem.setText(21, str(item['water']) + '%')
            qtreeitem.setText(22, str(item['rdensity']))
            qtreeitem.setText(23, str(item['impurity']) + '%')
            qtreeitem.setText(
                24, item['warehousemanid'] + item['warehousemanname']
            )

    def set_kind_tree(self, current_tree, stuff_list):
        kind_list = stuff_list.annotate(amount=Sum('amount'),
                                        piamount=Sum('piamount'))
        for item in kind_list:
            qtreeitem = QTreeWidgetItem(current_tree)
            qtreeitem.setText(0, item['stuffkind'])
            qtreeitem.setText(1, str(item['piamount']))
            qtreeitem.setText(2, str(item['amount']))
            qtreeitem.setText(3, item['basicunit'])

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        curent_tab = getattr(self, 'tab_' + str(p_int))
        curent_tab.setLayout(self.gridLayout_2)
        self.get_stuff_list()

    pyqtSlot(bool)
    def on_radioButton_batchno_toggled(self, p_bool):
        if p_bool:
            self.current_button = self.radioButton_batchno
            self.get_stuff_list()

    pyqtSlot(bool)
    def on_radioButton_kind_toggled(self, p_bool):
        if p_bool:
            self.current_button = self.radioButton_kind
            self.get_stuff_list()

    @pyqtSlot(QPoint)
    def on_treeWidget_stuffbatchnolist_customContextMenuRequested(self, pos):
        id = 0
        lrid = 0
        stuffid = ''
        batchno = ''
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is None:
            return

        id = int(current_item.text(0))
        lrid = int(current_item.text(1))
        stuffid, stuffname = current_item.text(3).split(' ')
        batchno = current_item.text(6)

        menu = QMenu()
        button1 = menu.addAction("修改记录")
        button2 = menu.addAction("查看检验报告")
        button3 = menu.addAction("新建库存复检申请单")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:
            detail = ModifyStuffParmeter(id, self)
            detail.accepted.connect(self.get_stuff_list)
            detail.show()

        elif action == button2:
            detail = FindCheckReportModule(stuffid, batchno, self)
            detail.show()

        elif action == button3:
            key_dict = {
                'stuffid': stuffid,
                'stuffname': stuffname
            }
            checkunit = ''
            res = self.SFC.get_stuffdict(True, *VALUES_TUPLE_SD, **key_dict)
            if len(res):
                checkunit = res[0]
            kwargs = {
                'labtype': 1,
                'chkid': stuffid,
                'chkname': stuffname,
                'batchno': current_item.text(6),
                'mbatchno': current_item.text(7),
                'spec': current_item.text(8),
                'package': current_item.text(9),
                'producer': current_item.text(19),
                'supplyer': current_item.text(18) if current_item.text(18) in (
                    '', ' ') else current_item.text(18).split(' ')[2],
                'ciid': int(current_item.text(0)),
                'createdate': user.now_date,
                'checkamount': decimal.Decimal(current_item.text(11)),
                'caunit': current_item.text(12),
                'sampleunit': checkunit,
                'samplesource': current_item.text(13)
            }
            labrecord = self.LC.update_labrecord(**kwargs)
            key_dict_checkitem = {'stuffid': stuffid, 'itemtype': 0}
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
            detail = ApplycheckModule(labrecord.autoid, self)
            detail.rejected.connect(
                lambda: self.delete_check_report(labrecord.autoid))
            detail.show()

    def delete_check_report(self, lrid):
        self.LC.delete_labrecord(lrid)
        self.LC.delete_labitem(lrid)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_stuffbatchnolist_itemDoubleClicked(self, qtreeitem,
                                                         p_int):

        id = int(qtreeitem.text(0))
        lrid = int(qtreeitem.text(1))
        detail = ModifyStuffParmeter(id, self)
        detail.accepted.connect(self.get_stuff_list)
        detail.show()


VALUES_TUPLE_SUPPLYER = ('autoid',)
VALUES_TUPLE_SD = ('checkunit',)

VALUES_TUPLE_CHECKITEM = (
    'seqid', 'itemname', 'kind', 'referencevalue', 'putintype'
)

VALUES_TUPLE_ORDER = (
    'autoid', 'paperno', 'supid', 'supname', 'creatorid', 'creatorname',
    'createdate', 'buyerid', 'buyername', 'buydate', 'pppaperno', 'remark'
)

VALUES_TUPLE_BATCHNO = (
    'autoid', 'lrid', 'stuffid', 'stuffname', 'stufftype', 'stuffkind',
    'batchno', 'mbatchno', 'spec', 'package', 'piamount', 'amount',
    'basicunit', 'makedate', 'putindate', 'expireddate', 'nextcheckdate',
    'supid', 'supname', 'producer', 'content', 'cunit', 'water', 'rdensity',
    'impurity', 'warehousemanid', 'warehousemanname', 'status', 'position'
)
VALUES_TUPLE_KIND = ('stuffkind', 'basicunit')
STUFF_KIND = ("主材料", "前处理", "辅材料", "内包材", "外包材")
STATUS = ("合格", "待复检", "即将过期", "已过期", "其他")
