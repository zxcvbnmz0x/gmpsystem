# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot

from stuff.views.stuffdrawpaper import Ui_Form
from stuff.controllers.stuffcontroller import StuffController

import user


class StuffdrawpaperModule(QWidget, Ui_Form):
    def __init__(self, autoid, parent=None):
        # autoid：领料单在stuffdrawpaper中的autoid
        # kind: 领料单的类型与原料对应
        super(StuffdrawpaperModule, self).__init__(parent)
        self.autoid = autoid
        self.ori_detail = object
        self.new_detail = {}
        self.SC = StuffController()
        self.setupUi(self)
        self.pushButton_apply.setVisible(False)
        self.get_stuffdrawpaper()

    # 获取领料单的状态
    def get_stuffdrawpaper(self):
        res = self.SC.get_stuffdrawpaper(autoid=self.autoid)
        if len(res) == 1:
            self.ori_detail = res[0]

            self.label_dept.setText(
                self.ori_detail.deptid + ' ' + self.ori_detail.deptname)
            if self.ori_detail.status == 0:
                self.label_status.setText("未提交")
                self.pushButton_apply.setVisible(True)
                self.pushButton_apply.setText("提交领料")
                self.label_charger.setText('')
                self.label_provider.setText('')
                self.dateEdit_applytime.setVisible(False)
                self.dateEdit_drawtime.setVisible(False)
            elif self.ori_detail.status == 1:
                self.label_status.setText("已提交")
                self.pushButton_apply.setText("取消领料")
                self.label_charger.setText(
                    self.ori_detail.chargerid + ' ' + self.ori_detail.chargername)
                self.label_provider.setText('')
                self.dateEdit_applytime.setDate(
                    self.ori_detail.applydate)
                self.dateEdit_applytime.setVisible(True)
                self.dateEdit_drawtime.setVisible(False)
            elif self.ori_detail.status == 2:
                self.label_status.setText("已完成")
                self.label_charger.setText(
                    self.ori_detail.chargerid + ' ' + self.ori_detail.chargername)
                self.label_provider.setText(
                    self.ori_detail.providerid + ' ' + self.ori_detail.providername)
                self.dateEdit_applytime.setDate(
                    self.ori_detail.applydate)
                self.dateEdit_drawtime.setDate(self.ori_detail.drawdate)
                self.get_stufflist()

    # 获取已经领取了的物料
    def get_stufflist(self):
        values_tupe = (
            "autoid", "lrid", "stuffid", "stuffname", "batchno", "spec",
            "package", "presamount", "pracamount", "drawamount", "content",
            "cunit", "water", "impurity", "rdensity", "presunit", "pracunit",
            "drawunit"
        )
        key_dict = {'sdpid': self.autoid}
        res = self.SC.get_prodstuff(0, *values_tupe, **key_dict)
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_stufflist)
                qtreeitem.setText(0, str(item['autoid']))  # autoid
                qtreeitem.setText(1, str(item['lrid']))  # lrid
                qtreeitem.setText(2, item['stuffid'] + ' ' + item['stuffname'])  # 物料
                qtreeitem.setText(3, item['batchno'])  # 进厂批号
                qtreeitem.setText(4, item['spec'])  # 含量规格
                qtreeitem.setText(5, item['package'])  # 包装规格
                qtreeitem.setText(6, str(item['presamount']) + item['presunit'])  # 计划量
                qtreeitem.setText(7, str(item['pracamount']) + item['pracunit'])  # 实际量
                qtreeitem.setText(8, str(item['drawamount']) + item['drawunit'])  # 领取量
                qtreeitem.setText(9, str(item['content']) + item['cunit'])  # 含量/效价
                qtreeitem.setText(10, str(item['water']) + '%')  # 水分
                qtreeitem.setText(11, str(item['impurity']))  # 相对密度
                qtreeitem.setText(12, str(item['rdensity']))  # 杂质

            self.treeWidget_stufflist.hideColumn(0)
            self.treeWidget_stufflist.hideColumn(1)
            for i in range(2, 11):
                self.treeWidget_stufflist.resizeColumnToContents(i)

    # 提交领料
    @pyqtSlot()
    def on_pushButton_apply_clicked(self):
        if self.ori_detail.status == 0:
            self.new_detail['status'] = 1
            self.new_detail['chargerid'] = user.user_id
            self.new_detail['chargername'] = user.user_name
            self.new_detail['applydate'] = user.now_date
            # print(self.new_detail)
            res = self.SC.update_stuffdrawpaper(autoid=self.autoid,
                                                **self.new_detail)
            print("res1=", res)

        elif self.ori_detail.status == 1:
            self.new_detail['status'] = 0
            self.new_detail['chargerid'] = ''
            self.new_detail['chargername'] = ''
            self.new_detail['applydate'] = None
            res = self.SC.update_stuffdrawpaper(autoid=self.autoid,
                                                **self.new_detail)
        if res:
            self.get_stuffdrawpaper()
