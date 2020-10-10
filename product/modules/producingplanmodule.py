# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import user
import datetime

from product.controllers.productcontroller import ProductController
from product.controllers.editproducingplan import EditProducingplan
from workshop.controllers.workshopcontroller import WorkshopController

from product.models.productmodel import ProductModel
from workshop.modules.producingmodule import ProducingModule

from product.views.producingplan import Ui_Form

BUTTON_KIND = ('editButton', 'releaseButton', 'produceButton', 'examineButton',
               'finishedpushButton')


class ProducingplanModule(QtWidgets.QDialog, Ui_Form):
    current_kind = 'editButton'

    def __init__(self, parent=None, flag=0):
        super().__init__(parent)
        self.setupUi(self)
        self.flag = flag
        if self.flag:
            self.addButton.setVisible(False)
            self.deleteButton.setVisible(False)
        # 数据库操作类
        self.sd = ProductModel()
        self.product = ProductController()
        self.detail = ''
        # 未下达/已下达/正在生产/审核/生产结束 五个状态按键的功能
        self.editButton.clicked.connect(self.on_statusButton_clikcked)
        self.releaseButton.clicked.connect(self.on_statusButton_clikcked)
        self.produceButton.clicked.connect(self.on_statusButton_clikcked)
        self.examineButton.clicked.connect(self.on_statusButton_clikcked)
        self.finishedpushButton.clicked.connect(self.on_statusButton_clikcked)
        # 显示产品列表
        self.show_production_list()
        # 添加右键菜单功能
        self.__add_menu()

    # 显示生产记录列表
    def show_production_list(self):
        status = BUTTON_KIND.index(self.current_kind)
        vlst = ('autoid', 'prodid', 'prodname', 'commonname', 'batchno',
                'spec', 'package', 'medkind', 'planamount', 'mpunit',
                'instructorid', 'instructorname', 'plandate', 'realamount',
                'makedate', 'qaauditorid', 'qaauditorname', 'qadate',
                'executorid', 'executorname', 'executedate', 'linename',
                'workshopid', 'workshopname')
        production_records = self.product.get_producingplan(False, status=status,
                                                            *vlst)
        production_records.reverse()
        if production_records:
            count = len(production_records)
            self.countlabel.setText("共%s条记录" % count)
            self.productionrecords.clear()
            for item in production_records.order_by('-autoid'):
                tree_item = QtWidgets.QTreeWidgetItem(self.productionrecords)
                tree_item.setText(0, str(item['autoid']))
                tree_item.setText(1, item['prodid'])
                tree_item.setText(2, item['prodname'])
                tree_item.setText(3, item['commonname'])
                tree_item.setText(4, item['batchno'])
                tree_item.setText(5, item['spec'])
                tree_item.setText(6, item['package'])
                tree_item.setText(7, item['medkind'])
                tree_item.setText(8, str(item['planamount']) + item['mpunit'])
                tree_item.setText(9, item['instructorid'] + " " + item[
                    'instructorname'])
                tree_item.setText(10, str(item['plandate']) if type(
                    item['plandate']) is datetime.date else '')
                tree_item.setText(11, str(item['makedate']) if type(
                    item['makedate']) is datetime.date else '')
                tree_item.setText(12, item['qaauditorid'] + " " + item[
                    'qaauditorname'])
                tree_item.setText(13, str(item['qadate']))
                tree_item.setText(14, item['executorid'] + " " + item[
                    'executorname'])
                tree_item.setText(15, str(item['executedate']) if type(
                    item['executedate']) is datetime.date else '')
                tree_item.setText(16, item['linename'])
                tree_item.setText(17, item['workshopid'] + " " + item[
                    'workshopname'])
            # 隐藏第一列的id
            self.productionrecords.hideColumn(0)
            for i in range(1, 18):
                self.productionrecords.resizeColumnToContents(i)
                if self.productionrecords.columnWidth(i) > 200:
                    self.productionrecords.setColumnWidth(i, 180)
                elif self.productionrecords.columnWidth(i) < 80:
                    self.productionrecords.setColumnWidth(i, 100)
        else:
            self.productionrecords.clear()
            self.productionrecords.hideColumn(0)
            self.countlabel.setText("共0条记录")

    def __add_menu(self):
        if self.flag == 0:
            self.productionrecords.setContextMenuPolicy(
                QtCore.Qt.CustomContextMenu)
            self.productionrecords.customContextMenuRequested.connect(
                self.generate_menu)
        else:
            pass

    def generate_menu(self, pos):
        sender_widget = self.sender()
        menu = QtWidgets.QMenu()
        if BUTTON_KIND.index(self.current_kind) == 0:
            button1 = menu.addAction("增加")
            button2 = menu.addAction("修改")
            button3 = menu.addAction("删除")
            button5 = menu.addAction("审核下达")
        elif BUTTON_KIND.index(self.current_kind) == 1:
            button6 = menu.addAction("取消下达")
            button7 = menu.addAction("开始生产")
        elif BUTTON_KIND.index(self.current_kind) == 2:
            button4 = menu.addAction("显示批生产记录")
            button8 = menu.addAction("删除生产记录")
        else:
            button4 = menu.addAction("显示批生产记录")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        try:
            if BUTTON_KIND.index(self.current_kind) == 0:
                # 增加
                if action == button1:
                    self.on_addButton_clicked()
                # 修改
                elif action == button2:
                    self.on_recordButton_clicked()
                # 删除
                elif action == button3:
                    self.on_deleteButton_clicked()
                # 审核下达
                elif action == button5:
                    self.on_status_changed(1)
            elif BUTTON_KIND.index(self.current_kind) == 1:
                # 取消下达
                if action == button6:
                    self.on_status_changed(0)
                # 开始生产生产记录
                elif action == button7:
                    self.on_status_changed(1)
            elif BUTTON_KIND.index(self.current_kind) == 2:
                # 显示批生产记录
                if action == button4:
                    pass
                # 删除生产记录
                elif action == button8:
                    self.on_deleteButton_clicked()
            else:
                # 显示批生产记录
                if action == button4:
                    pass
        # 按键没有定义
        except UnboundLocalError:
            pass

    # 批生产状态更新
    # current_status：int    当前的状态
    # flat:bool 更新的状态方向，0为减少1，1为加1
    def on_status_changed(self, flat: bool):
        current_status = BUTTON_KIND.index(self.current_kind)
        print(flat, current_status)
        items = self.productionrecords.selectedItems()
        autoid_list = []
        if items is not None:
            for item in items:
                autoid_list.append(item.text(0))
        data = dict()
        data['status'] = current_status + 1 if flat else current_status - 1
        data['statustime'] = user.time if flat else datetime.datetime(1000, 1,
                                                                      1, 0, 0,
                                                                      0)
        # 未下达
        if current_status == 0:
            data['warrantorid'] = user.user_id if flat else ''
            data['warrantorname'] = user.user_name if flat else ''
            data['warrantdate'] = user.now_date if flat else datetime.date(1000,
                                                                           1, 1)
            data['qadate'] = user.now_date if flat else datetime.date
            data['bpwarrantorid'] = user.user_id if flat else ''
            data['bpwarrantorname'] = user.user_name if flat else ''
            data['bpwarrantdate'] = user.now_date if flat else datetime.date(
                1000, 1, 1)
            res = self.product.update_producingplan_status(autoid_list, **data)
            self.show_production_list()
        # 已下达
        elif current_status == 1:
            data['executorid'] = user.user_id if flat else ''
            data['executorname'] = user.user_name if flat else ''
            data['executedate'] = user.now_date if flat else ''
            data['qadate'] = user.now_date if flat else ''
            data['bpwarrantorid'] = user.user_id if flat else ''
            data['bpwarrantorname'] = user.user_name if flat else ''
            data['bpwarrantdate'] = user.now_date if flat else ''
            res = self.product.update_producingplan_status(autoid_list, **data)
            if res:
                self.show_production_list()

    # 增加按键功能
    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        detail = EditProducingplan(self)
        detail.flush_signal.connect(self.show_production_list)
        detail.show()

    # 打开记录详情
    @QtCore.pyqtSlot()
    def on_recordButton_clicked(self):
        if self.productionrecords.currentItem():
            self.on_productionrecords_itemDoubleClicked(
                self.productionrecords.currentItem(), 0)

    # 刷新生产指令列表
    @QtCore.pyqtSlot()
    def on_refreshButton_clicked(self):
        self.show_production_list()

    # 删除按键功能
    @QtCore.pyqtSlot()
    def on_deleteButton_clicked(self):
        items = self.productionrecords.selectedItems()
        autoid_list = []
        if items is not None:
            current_status = BUTTON_KIND.index(self.current_kind)
            if current_status < 2:
                # 还没有开始生产，只需要删除producingplan里的记录
                flat = 0
            else:
                # 已经生产了，需要删除全部记录
                flat = 1
            for item in items:
                autoid_list.append(item.text(0))
            print(autoid_list)
            res = self.product.delete_producingplan(None, flat, *autoid_list)
            try:
                if res[0] >= 1:
                    self.show_production_list()
            except TypeError:
                if res >= 1:
                    self.show_production_list()

    # 生产指令列表双击功能
    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def on_productionrecords_itemDoubleClicked(self, QTreeWidgetItem, p_int):
        autoid = QTreeWidgetItem.text(0)
        if BUTTON_KIND.index(self.current_kind) < 2:
            # 生产指令详细列表
            detail = EditProducingplan(self)
            detail.set_autoid(autoid)
            detail.flush_signal.connect(self.show_production_list)
            # 修改了物料记录，刷新列表
            detail.show()
        else:
            detail = ProducingModule(autoid, self)
            detail.showMaximized()

    # 状态按键功能，5个按键共用一个方法
    @QtCore.pyqtSlot()
    def on_statusButton_clikcked(self):
        clicked_button = self.sender()
        current_button = getattr(self, self.current_kind)
        clicked_button.setEnabled(False)
        current_button.setEnabled(True)
        self.current_kind = clicked_button.objectName()
        self.show_production_list()
