# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from warehouse.views.productrepository import Ui_Form

from warehouse.controllers.warehousecontroller import WarehouseController
from labrecord.controllers.labrecordscontroller import LabrecordsController
from product.controllers.productcontroller import ProductController

from labrecord.modules.findcheckreportlistmodule import FindCheckReportModule

from django.db.models import Sum
from lib.utils.util import to_str

import datetime


class ProductRepositoryModule(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(ProductRepositoryModule, self).__init__(parent)
        self.setupUi(self)
        self.WC = WarehouseController()
        self.LC = LabrecordsController()
        self.PC = ProductController()
        self.current_button = self.radioButton_batchno
        self.get_product_list()

    def get_product_list(self):
        if self.current_button == self.radioButton_batchno:
            self.treeWidget_productbatchnolist.setVisible(True)
            self.treeWidget_productkindlist.setVisible(False)
            current_tree = self.treeWidget_productbatchnolist
            current_tree.hideColumn(0)
        elif self.current_button == self.radioButton_kind:
            self.treeWidget_productbatchnolist.setVisible(False)
            self.treeWidget_productkindlist.setVisible(True)
            current_tree = self.treeWidget_productkindlist
        else:
            return

        current_tree.clear()
        key_dict = {'stockamount__gt': 0}
        product_list = self.WC.get_productrepository(
            False, **key_dict
        )
        if not len(product_list):
            return

        if current_tree == self.treeWidget_productbatchnolist:
            self.set_batchno_tree(current_tree, product_list)
            for i in range(1, 15):
                current_tree.resizeColumnToContents(i)
        elif current_tree == self.treeWidget_productkindlist:
            self.set_kind_tree(current_tree, product_list)
            for i in range(0, 6):
                current_tree.resizeColumnToContents(i)
        else:
            return

    def set_batchno_tree(self, current_tree, product_list):
        p_list = product_list.values(*VALUES_TUPLE_BATCHNO)
        """
        .extra(
            select={
                'prodid': 'prodid', 'prodname': 'prodname', 'spec': 'spec',
                'commonname': 'commonname', 'batchno': 'batchno',
                'package': 'package', 'spunit': 'spunit',
                'makedate': 'makedate', 'expireddates': 'expireddates'
            },
            tables=['producingplan'],
            where=['producingplan.autoid=ppid']
        )
        """
        for item in p_list:
            qtreeitem = QTreeWidgetItem(current_tree)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, SOURCE[item['pisource']])
            qtreeitem.setText(2, item['prodid'] + ' ' + item['prodname'])
            qtreeitem.setText(3, item['commonname'])
            if item['pisource'] == 2:
                key_dict = {'autoid': item['hxid']}
                hx_batchno_list = self.PC.get_producingplan(
                    True, *VALUES_TUPLE_PRODUCINGPLAN, **key_dict
                )
                hx_batchno = ''
                if len(hx_batchno_list):
                    hx_batchno = hx_batchno_list[0]
                qtreeitem.setText(4, item['batchno'] + ' ' + hx_batchno)

                qtreeitem.setText(
                    7, to_str((item['piamount'] - item[
                        'hxamount'])) + '+' +
                       to_str(item['hxamount'])
                )
                qtreeitem.setText(
                    8, to_str(item['stockamount'] - item[
                        'hxstockamount']) + '+' + to_str(item['hxstockamount'])
                )
            else:
                qtreeitem.setText(4, item['batchno'])
                qtreeitem.setText(7, str(item['piamount']))
                qtreeitem.setText(8, str(item['stockamount']))

            qtreeitem.setText(5, item['spec'])
            qtreeitem.setText(6, item['package'])
            qtreeitem.setText(9, item['spunit'])
            qtreeitem.setText(10, item['position'])

            qtreeitem.setText(11, str(item['indate']))
            if type(item['makedate']) is datetime.date:
                qtreeitem.setText(12, str(item['makedate']))
                qtreeitem.setText(13, str(item['expireddate']))
            qtreeitem.setText(
                14, item['warehousemanid'] + item['warehousemanname']
            )

    def set_kind_tree(self, current_tree, product_list):
        kind_list = product_list.values(*VALUES_TUPLE_KIND).annotate(
            stockamount=Sum('stockamount'), piamount=Sum('piamount')
        )
        """
        .extra(
            select={
                'prodid': 'prodid', 'prodname': 'prodname', 'spec': 'spec',
                'commonname': 'commonname', 'package': 'package',
                'spunit': 'spunit'
            },
            tables=['producingplan'],
            where=['producingplan.autoid=ppid']
        ). \
        """
        for item in kind_list:
            qtreeitem = QTreeWidgetItem(current_tree)
            qtreeitem.setText(0, item['prodid'] + item['prodname'])
            qtreeitem.setText(1, item['commonname'])
            qtreeitem.setText(2, item['spec'])
            qtreeitem.setText(3, item['package'])
            qtreeitem.setText(4, to_str(item['piamount']))
            qtreeitem.setText(5, to_str(item['stockamount']))
            qtreeitem.setText(6, item['spunit'])

    pyqtSlot(bool)

    def on_radioButton_batchno_toggled(self, p_bool):
        if p_bool:
            self.current_button = self.radioButton_batchno
            self.get_product_list()

    pyqtSlot(bool)
    def on_radioButton_kind_toggled(self, p_bool):
        if p_bool:
            self.current_button = self.radioButton_kind
            self.get_product_list()

    @pyqtSlot(QPoint)
    def on_treeWidget_productbatchnolist_customContextMenuRequested(self, pos):
        id = 0
        batchno = ''
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is None:
            return

        id = int(current_item.text(0))
        prodid, stuffname = current_item.text(2).split(' ')
        batchno = current_item.text(4)

        menu = QMenu()
        button1 = menu.addAction("查看检验报告")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:
            detail = FindCheckReportModule(prodid, batchno, self)
            detail.show()


VALUES_TUPLE_SUPPLYER = ('autoid',)
VALUES_TUPLE_SD = ('checkunit',)
VALUES_TUPLE_PRODUCINGPLAN = ('batchno',)

VALUES_TUPLE_BATCHNO = (
    'autoid', 'prodid', 'prodname', 'commonname', 'batchno',
    'spec', 'package', 'piamount', 'stockamount', 'pisource',
    'spunit', 'makedate', 'indate', 'expireddate', 'hxid', 'hxamount',
    'warehousemanid', 'warehousemanname', 'position', 'hxstockamount'
)
VALUES_TUPLE_KIND = (
    'prodid', 'prodname', 'commonname', 'spec', 'package', 'spunit'
)

SOURCE = ("普通", "零头", "合箱")
