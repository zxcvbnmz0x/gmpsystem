# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem

from stuff.controllers.stuffcontroller import StuffController
from product.controllers.productcontroller import ProductController

from workshop.views.productioninstruction import Ui_Form

import datetime

class PorductionInstructionModule(QWidget, Ui_Form):

    def __init__(self, autoid, parent=None):
        super(PorductionInstructionModule, self).__init__(parent)
        self.autoid = autoid
        self.setupUi(self)
        self.SC = StuffController()
        self.PC = ProductController()
        self.ori_detail = dict()
        self.new_detail = dict()
        # 获取物料信息
        self.get_stufflist()
        # 获取生产指令信息
        self.get_detail()

    # 获取已经领取了的物料
    def get_stufflist(self):
        values_tupe = (
            "autoid", "lrid", "stuffid", "stuffname", "batchno", "spec",
            "package", "presamount", "content", "cunit", "water",
            "impurity", "rdensity", "presunit"
        )
        key_dict = {
            'ppid': self.autoid,
            'stufftype__in': (0, 1, 2)
        }
        res = self.SC.get_prodstuff(False, *values_tupe, **key_dict)
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_stufflist)
                qtreeitem.setText(0, str(item['autoid']))  # autoid
                qtreeitem.setText(1, str(item['lrid']))  # lrid
                qtreeitem.setText(2, item['stuffid'] + ' ' + item[
                    'stuffname'])  # 物料
                qtreeitem.setText(3, item['batchno'])  # 进厂批号
                qtreeitem.setText(4, item['spec'])  # 含量规格
                qtreeitem.setText(5, item['package'])  # 包装规格
                qtreeitem.setText(6, str(item['presamount']) + item[
                    'presunit'])  # 计划量
                qtreeitem.setText(7, str(item['content']) + item[
                    'cunit'])  # 含量/效价
                qtreeitem.setText(8, str(item['water']) + '%')  # 水分
                qtreeitem.setText(9, str(item['impurity']))  # 相对密度
                qtreeitem.setText(10, str(item['rdensity']))  # 杂质

            self.treeWidget_stufflist.hideColumn(0)
            self.treeWidget_stufflist.hideColumn(1)
            for i in range(2, 11):
                self.treeWidget_stufflist.resizeColumnToContents(i)



    def get_detail(self):
        values_list = (
            'instructorid', 'instructorname', 'warrantorid', 'warrantorname',
            'executorid', 'executorname', 'plandate', 'warrantdate',
            'executedate'
        )
        key_dict = {
            'autoid': self.autoid
        }
        res = self.PC.get_producingplan(False, *values_list, **key_dict)
        if len(res) == 0:
            return

        self.ori_detail = res[0]
        self.pushButton_instructor.setText(
            self.ori_detail['instructorid'] + ' ' +
            self.ori_detail['instructorname']
        )
        self.pushButton_warrantor.setText(
            self.ori_detail['warrantorid'] + ' ' +
            self.ori_detail['warrantorname']
        )
        self.pushButton_executor.setText(
            self.ori_detail['executorid'] + ' ' +
            self.ori_detail['executorname']
        )
        if type(self.ori_detail['plandate']) is datetime.date:
            self.dateEdit_plandate.setDate(self.ori_detail['plandate'])
        if type(self.ori_detail['warrantdate']) is datetime.date:
            self.dateEdit_warrantdate.setDate(self.ori_detail['warrantdate'])
        if type(self.ori_detail['executedate']) is datetime.date:
            self.dateEdit_executedate.setDate(self.ori_detail['executedate'])

