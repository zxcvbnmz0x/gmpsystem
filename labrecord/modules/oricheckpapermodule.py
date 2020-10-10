# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from equipment.controllers.equipmentcontroller import EquipmentController

from equipment.modules.eqrunnotedodule import EqrunnoteModule

from labrecord.controllers.labrecordscontroller import LabrecordsController

from labrecord.views.oricheckpaper import Ui_Form

from lib.xmlwidget.xmlreadwrite import XMLReadWrite

import user

RUN_STATUS = ("正常运行", "停用待修", "故障抢修", "日常小修", "计划大修")


class OricheckpaperModule(QWidget, Ui_Form):
    edited = pyqtSignal(int)

    def __init__(self, autoid, parent=None):
        super(OricheckpaperModule, self).__init__(parent)
        self.ori_detail = dict()
        self.autoid = autoid
        self.LC = LabrecordsController()
        self.current_content = object
        self.setupUi(self)
        # 获取记录内容
        self.get_oricheckpaper()
        # 获取设备运行记录
        self.get_equiprunnote()
        self.treeWidget_equipment.setContextMenuPolicy(3)
        self.treeWidget_equipment.customContextMenuRequested.connect(
            self.eqrun_menu)

    def get_oricheckpaper(self):
        values_list = ('formcontent',)
        key_dict = {
            'autoid': self.autoid
        }
        res = self.LC.get_oricheckpaper(True, *values_list, **key_dict)
        if len(res):
            ori_paper = res[0]
            self.current_content = XMLReadWrite(self)
            self.current_content.openxml(ori_paper)
            self.gridLayout_6.addWidget(self.current_content)
            self.current_content.__setattr__('autoid', self.autoid)

    def get_equiprunnote(self):
        self.treeWidget_equipment.clear()
        EC = EquipmentController()
        '''
        values_list = (
            'autoid', 'eqno', 'eqname', 'fillerid', 'fillername',
            'runstarttime', 'runendtime', 'runtime', 'runstatus'
        )
        key_dict = {
            'pid': self.autoid,
            'rtype': 1
        }
        '''
        eqrunnotes = EC.get_equip_run_note(pid=self.autoid, rtype=1)
        if len(eqrunnotes):
            for item in eqrunnotes:
                qtreeitem = QTreeWidgetItem(self.treeWidget_equipment)
                qtreeitem.setText(0, str(item.autoid))
                qtreeitem.setText(1, item.eqno + ' ' + item.eqname)
                qtreeitem.setText(2, item.fillerid + ' ' + item.fillername)
                qtreeitem.setText(3, str(item.runstarttime))
                qtreeitem.setText(4, str(item.runendtime))
                qtreeitem.setText(5, str(item.runtime) + ' ' + '分钟')
                qtreeitem.setText(6, RUN_STATUS[item.runstatus])
            self.treeWidget_equipment.hideColumn(0)
            for i in range(1, 7):
                self.treeWidget_equipment.resizeColumnToContents(i)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_equipment_itemDoubleClicked(self, qitem, p_int):
        eqrun_detail = EqrunnoteModule(qitem.text(0), parent=self)
        eqrun_detail.flush_signal.connect(self.get_equiprunnote)
        eqrun_detail.show()

    # 设备运行记录右键菜单功能
    def eqrun_menu(self, pos):
        # 返回调用者的对象
        sender_widget = self.sender()
        menu = QMenu()
        button1 = menu.addAction("编辑运行记录")
        button2 = menu.addAction("复制运行记录")
        button3 = menu.addAction("删除运行记录")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        select_items = sender_widget.selectedItems()
        autoid_list = []
        for item in select_items:
            autoid_list.append(int(item.text(0)))
        if len(select_items):
            EC = EquipmentController()
            # 编辑运行记录
            if action == button1:
                eqrun_detail = EqrunnoteModule(sender_widget.currentItem().text(0))
                res = eqrun_detail.exec()
            # 复制运行记录
            elif action == button2:
                res = EC.insert_equip_run_note(autoid_list)
            # 删除运行记录
            elif action == button3:
                res = EC.delete_equip_run_note(autoid_list)
            if res:
                self.get_equiprunnote()

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        res = self.LC.update_oricheckpaper(
            autoid=self.autoid, formcontent=self.current_content.get_content()
        )
        if res:
            self.current_content.flat = 0

    # 运行记录双击功能
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_equipment_itemDoubleClicked(self, qitem, p_int):
        eqrun_detail = EqrunnoteModule(qitem.text(0), parent=self)
        eqrun_detail.flush_signal.connect(self.get_equiprunnote)
        eqrun_detail.show()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.current_content.flat=0

    @pyqtSlot()
    def on_pushButton_delete_clicked(self):
        res = self.LC.delete_oricheckpaper([self.autoid,])
        if res:
            print(self.objectName())
