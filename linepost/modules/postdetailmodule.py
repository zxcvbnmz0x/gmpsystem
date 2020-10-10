# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QDateTime, pyqtSlot

from linepost.views.postdetail import Ui_Form
from linepost.controllers.linepostconroller import LinepostController
from clerks.controllers.clerks import Clerks
from equipment.controllers.equipmentcontroller import EquipmentController
from equipment.modules.eqrunnotedodule import EqrunnoteModule

import json
import user

RUN_STATUS = ("正常运行", "停用待修", "故障抢修", "日常小修", "计划大修")


class PostdetailModule(QWidget, Ui_Form):
    def __init__(self, autoid, plid, seqid, postname, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.autoid = autoid
        self.flat = False
        self.ori_detail = object
        self.new_detail = {}
        # 人员id列表，用于判断操作人员是否有权限操作该岗位
        self.clerkid_list = list()
        self.LP = LinepostController()
        self.get_postdetail()
        # 设置温湿度的输入范围
        self.set_temp_hum_valid()
        self.setroomnamelist(plid, seqid, postname)
        self.get_workers(plid, seqid, postname)
        self.get_gmpfile(plid, seqid, postname)
        self.get_equiprunnote()
        self.treeWidget_equipment.setContextMenuPolicy(3)
        self.treeWidget_equipment.customContextMenuRequested.connect(self.eqrun_menu)

    # 设置温湿度的输入范围
    def set_temp_hum_valid(self):
        double_valitor = QDoubleValidator()
        double_valitor.setRange(-50, 100)
        self.lineEdit_temperature.setValidator(double_valitor)
        double_valitor.setRange(0, 100)
        self.lineEdit_humidity.setValidator(double_valitor)

    # 设置岗位的状态
    def get_postdetail(self):
        res = self.LP.get_linepost(self.autoid)
        if len(res) == 1:
            self.ori_detail = res[0]
            self.label_postname.setText(self.ori_detail.postname)
            self.comboBox_roomname.setCurrentText(self.ori_detail.roomname)
            self.lineEdit_temperature.setText(str(self.ori_detail.temp))
            self.lineEdit_humidity.setText(str(self.ori_detail.humidity))
            if self.ori_detail.status == 0:
                self.comboBox_roomname.setEnabled(True)
                self.dateTimeEdit_starttime.setDateTime(QDateTime(user.time))
                self.dateTimeEdit_endtime.setDateTime(QDateTime(user.time))
            elif self.ori_detail.status == 1:
                self.comboBox_roomname.setEnabled(False)
                self.comboBox_roomname.setStyleSheet('QComboBox{border:none;}QComboBox::drop-down{border-style: none;width:0;}')
                self.pushButton_startpost.setEnabled(False)
                self.dateTimeEdit_starttime.setDateTime(QDateTime(self.ori_detail.starttime))
                self.dateTimeEdit_endtime.setDateTime(QDateTime(user.time))
            else:
                self.toolButton.setVisible(False)
                self.comboBox_roomname.setStyleSheet(
                    'QComboBox::drop-down{border-style: none;}')
                self.pushButton_startpost.setEnabled(False)
                self.pushButton_endpost.setEnabled(False)
                self.dateTimeEdit_starttime.setDateTime(
                    QDateTime(self.ori_detail.starttime))
                self.dateTimeEdit_endtime.setDateTime(QDateTime(self.ori_detail.endtime))

    # 设置岗位工人列表
    def get_workers(self, plid, seqid, postname):

        res = self.LP.get_worker(plid, seqid, postname, 'clerkid')
        self.clerkid_list = list()
        CL = Clerks()
        if len(res) > 0:
            for item in res:
                self.clerkid_list.append(item)
            clerk_list = CL.get_clerks(self.clerkid_list, 'pid', 'clerkname')
            for clerk in clerk_list:
                self.listWidget_postworker.addItem(clerk[0] + ' '+ clerk[1])

    # 设置岗位文档
    def get_gmpfile(self, plid, seqid, postname):
        res = self.LP.get_gmpfile(plid, seqid, postname, 'autoid', 'docno', 'title')
        if len(res):
            for item in res:
                treeitem = QTreeWidgetItem(self.treeWidget_document)
                treeitem.setText(0, str(item[0]))
                treeitem.setText(1, item[1])
                treeitem.setText(2, item[2])
            self.treeWidget_document.hideColumn(0)
            self.treeWidget_document.resizeColumnToContents(1)
            self.treeWidget_document.resizeColumnToContents(2)

    # 获取岗位设备的运行情况
    def get_equiprunnote(self):
        self.treeWidget_equipment.clear()
        EC = EquipmentController()
        eqrunnotes = EC.get_equip_run_note(lpid=self.autoid)
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

    # 运行记录双击功能
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_equipment_itemDoubleClicked(self, qitem, p_int):
        eqrun_detail = EqrunnoteModule(qitem.text(0), parent=self)
        eqrun_detail.flush_signal.connect(self.get_equiprunnote)
        eqrun_detail.show()

    # 查询以前当前岗位使用过的房间名
    def setroomnamelist(self, plid, seqid, postname):
        spareroomstr = self.LP.get_spareroomlist(plid, seqid, postname)
        if len(spareroomstr):
            spareroomlist = json.loads(spareroomstr)
            self.comboBox_roomname.addItems(spareroomlist)

    # 更换房间按键功能
    @pyqtSlot(str)
    def on_comboBox_roomname_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail.roomname:
                self.new_detail['roomname'] = p_str
            else:
                try:
                    del self.new_detail['roomname']
                except KeyError:
                    pass
        except ValueError:
            pass

    # 开始岗位
    @pyqtSlot()
    def on_pushButton_startpost_clicked(self):
        try:
            if self.ori_detail.status == 0:
                roomname = self.new_detail['roomname'] if 'roomname' in self.new_detail else self.ori_detail.roomname

                self.new_detail['status'] = 1

                self.new_detail['starttime'] = user.time
                res = self.LP.start_linepost(self.autoid, roomname,
                                             **self.new_detail)
                if res:
                    self.dateTimeEdit_starttime.setDateTime(user.time)
                    self.dateTimeEdit_starttime.setEnabled(False)
                    self.pushButton_startpost.setEnabled(False)
        except ValueError:
            pass

    # 结束岗位
    @pyqtSlot()
    def on_pushButton_endpost_clicked(self):
        try:
            if self.ori_detail.status == 1:
                self.new_detail['status'] = 2
                self.new_detail['endtime'] = user.time
                res = self.LP.end_linepost(self.autoid, **self.new_detail)
                if res:
                    self.dateTimeEdit_endtime.setDateTime(user.time)
                    self.dateTimeEdit_endtime.setEnabled(False)
                    self.pushButton_endpost.setEnabled(False)
        except ValueError:
            pass

    # 修改温度
    @pyqtSlot(str)
    def on_lineEdit_temperature_textEdited(self, p_str):
        try:
            if p_str != self.ori_detail.temp:
                self.new_detail['temp'] = p_str
            else:
                try:
                    del self.new_detail['temp']
                except KeyError:
                    pass
        except ValueError:
            pass

    # 修改湿度
    @pyqtSlot(str)
    def on_lineEdit_humidity_textEdited(self, p_str):
        try:
            if p_str != self.ori_detail.humidity:
                self.new_detail['humidity'] = p_str
            else:
                try:
                    del self.new_detail['humidity']
                except KeyError:
                    pass
        except ValueError:
            pass

    def save(self):
        pass
