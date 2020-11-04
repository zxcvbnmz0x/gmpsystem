# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from equipment.views.equipmentlist import Ui_Form
from equipment.controllers.equipmentcontroller import EquipmentController
from equipment.modules.editequipdetailmodule import EditEquipDetailModule



class EquipmentListModule(QDialog, Ui_Form):
    def __init__(self, parent=None):
        super(EquipmentListModule, self).__init__(parent)
        self.setupUi(self)
        self.EC = EquipmentController()
        self.ori_detail = dict()
        self.new_detail = dict()
        self.deptid = ''
        self.get_dept_detail()
        self.get_eq_detail()

    def get_eq_detail(self):
        self.treeWidget_equuiplist.clear()
        self.treeWidget_equuiplist.hideColumn(0)
        key_dict = dict()
        if self.deptid != '':
            key_dict['deptid'] = self.deptid
        res = self.EC.get_data(0, False, *VALUES_TUPLE_EQ, **key_dict)
        if not len(res):
            return
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_equuiplist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, EQTYPE[item['eqtype']])
            qtreeitem.setText(2, STATUS[item['status']])
            qtreeitem.setText(3, item['eqno'])
            qtreeitem.setText(4, item['eqname'])
            qtreeitem.setText(5, item['serialno'])
            qtreeitem.setText(6, item['spec'])
            qtreeitem.setText(7, item['manufacturer'])
            qtreeitem.setText(8, item['makedate'])
            qtreeitem.setText(9, item['indate'])
            qtreeitem.setText(10, item['instposition'])
            qtreeitem.setText(11, item['parameter'])
            qtreeitem.setText(12, item['performance'])
        for i in range(1, 13):
            self.treeWidget_equuiplist.resizeColumnToContents(i)

    def get_dept_detail(self):
        self.treeWidget_deptlist.clear()
        self.treeWidget_deptlist.hideColumn(1)
        all_dept = QTreeWidgetItem(self.treeWidget_deptlist)
        all_dept.setText(0, "全部部门")
        all_dept.setText(1, "")
        self.treeWidget_deptlist.expandAll()
        res = self.EC.get_data(0, False, *VALUES_TUPLE_DP).distinct()
        if not len(res):
            return
        for item in res:
            qtreeitem = QTreeWidgetItem(all_dept)
            qtreeitem.setText(0, item['deptname'])
            qtreeitem.setText(1, item['deptid'])
        self.treeWidget_deptlist.resizeColumnToContents(0)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_equuiplist_itemDoubleClicked(self, qtreeitem, p_int):
        autoid = int(qtreeitem.text(0))
        detail = EditEquipDetailModule(autoid, self)
        detail.accepted.connect(self.get_eq_detail)
        detail.accepted.connect(self.get_dept_detail)
        detail.show()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_deptlist_itemDoubleClicked(self, qtreeitem, p_int):
        self.deptid = qtreeitem.text(1)
        self.get_eq_detail()

    @pyqtSlot(QPoint)
    def on_treeWidget_equuiplist_customContextMenuRequested(self, pos):
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        menu = QMenu()
        button1 = menu.addAction("增加设备")
        button2 = menu.addAction("修改设备")
        button3 = menu.addAction("删除设备")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        if action == button1:
            detail = EditEquipDetailModule(parent=self)
            detail.accepted.connect(self.get_eq_detail)
            detail.accepted.connect(self.get_dept_detail)
            detail.show()
        elif action == button2:
            if current_item is not None:
                id = int(current_item.text(0))
                detail = EditEquipDetailModule(id, self)
                detail.accepted.connect(self.get_eq_detail)
                detail.accepted.connect(self.get_dept_detail)
                detail.show()
        elif action == button3:
            if current_item is not None:
                id = int(current_item.text(0))
                condition = {'autoid': id}
                self.EC.delete_data(0, condition)
                self.get_eq_detail()
                self.get_dept_detail()

EQTYPE = (
    "一般设备", "计量器", "空调系统", "纯化水系统", "注射用水系统", "检验分析仪器",
    "办公设备", "公用设备")
STATUS = ("正常", "检修", "清洁", "报废")

VALUES_TUPLE_EQ = (
    'autoid', 'eqno', 'eqname', 'eqtype', 'serialno', 'spec', 'indate','status',
    'manufacturer', 'instposition', 'makedate', 'parameter', 'performance'
)
VALUES_TUPLE_DP = ('deptid', 'deptname')
