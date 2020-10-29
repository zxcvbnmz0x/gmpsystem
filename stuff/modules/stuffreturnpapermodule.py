# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot

from stuff.views.stuffreturnpaper import Ui_Form
from stuff.controllers.stuffcontroller import StuffController
from stuff.modules.editstuffreturndetailmodule import EditStuffReturnDetailModule

from lib.utils.util import to_str

import user


class StuffReturnPaperModule(QWidget, Ui_Form):
    def __init__(self, autoid, parent=None):
        # autoid：领料单在stuffdrawpaper中的autoid
        super(StuffReturnPaperModule, self).__init__(parent)
        self.autoid = autoid
        self.ori_detail = dict()
        self.new_detail = dict()
        self.SC = StuffController()
        self.setupUi(self)
        self.pushButton_apply.setVisible(False)
        self.pushButton_cancel.setVisible(False)

        self.get_stuffdrawpaper()
        self.get_stufflist()

    # 获取领料单的状态
    def get_stuffdrawpaper(self):
        key_dict = {'autoid': self.autoid}
        res = self.SC.get_stuffdrawpaper(False, *VALUES_TUPLE_pAPER, **key_dict)
        if len(res) == 1:
            self.ori_detail = res[0]

            self.label_dept.setText(
                self.ori_detail['deptid'] + ' ' + self.ori_detail['deptname'])
            if self.ori_detail['wdstatus'] == 0:
                self.label_status.setText("未提交")
                self.pushButton_apply.setVisible(True)
                self.pushButton_cancel.setVisible(False)
                self.label_charger.setText('')
                # self.label_provider.setText('')
                self.dateEdit_applytime.setVisible(False)
                self.dateEdit_receivetime.setVisible(False)
            elif self.ori_detail['wdstatus'] == 1:
                self.label_status.setText("已提交")
                self.pushButton_apply.setVisible(False)
                self.pushButton_cancel.setVisible(True)
                self.label_charger.setText(
                    self.ori_detail['wdchargerid'] + ' ' +
                    self.ori_detail['wdchargername']
                )
                self.label_receiver.setText('')
                self.dateEdit_applytime.setDate(
                    self.ori_detail['wddate'])
                self.dateEdit_applytime.setVisible(True)
                self.dateEdit_receivetime.setVisible(False)
            elif self.ori_detail['wdstatus'] == 2:
                self.pushButton_apply.setVisible(False)
                self.pushButton_cancel.setVisible(False)
                self.label_status.setText("已完成")
                self.label_charger.setText(
                    self.ori_detail['wdchargerid'] + ' ' +
                    self.ori_detail['wdchargername'])
                self.label_receiver.setText(
                    self.ori_detail['wddrawerid'] + ' ' +
                    self.ori_detail['wddrawername']
                )
                self.dateEdit_applytime.setDate(self.ori_detail['wddate'])
                self.dateEdit_receivetime.setDate(self.ori_detail['wddrawdate'])

    # 获取已经领取了的物料
    def get_stufflist(self):
        self.treeWidget_stufflist.clear()
        self.treeWidget_stufflist.hideColumn(0)
        key_dict = {'sdpid': self.autoid}
        if self.label_status.text() == "已完成":
            key_dict['backamount__gt'] = 0
        res = self.SC.get_prodstuff(False, *VALUES_TUPLE_STUFF, **key_dict)
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_stufflist)
                qtreeitem.setText(0, str(item['autoid']))  # autoid
                qtreeitem.setText(1, item['stuffid'] + ' ' + item['stuffname'])  # 物料
                qtreeitem.setText(2, item['batchno'])  # 进厂批号
                qtreeitem.setText(3, item['spec'])  # 含量规格
                qtreeitem.setText(4, item['package'])  # 包装规格
                qtreeitem.setText(5, to_str(item['presamount']) + item['presunit'])  # 计划量
                qtreeitem.setText(6, to_str(item['pracamount']) + item['pracunit'])  # 实际量
                qtreeitem.setText(7, to_str(item['drawamount']) + item['drawunit'])  # 领取量
                qtreeitem.setText(8, to_str(item['restamount']) + item['drawunit'])  # 剩余量
                qtreeitem.setText(9, to_str(item['backamount']) + item['drawunit'])  # 退库量量
                qtreeitem.setText(10, item['wdid'] + item['wdname'])

            for i in range(1, 11):
                self.treeWidget_stufflist.resizeColumnToContents(i)

    # 提交领料
    @pyqtSlot()
    def on_pushButton_apply_clicked(self):
        if self.ori_detail['wdstatus'] != 0:
            return
        self.new_detail['wdstatus'] = 1
        self.new_detail['wdchargerid'] = user.user_id
        self.new_detail['wdchargername'] = user.user_name
        self.new_detail['wddate'] = user.now_date
        # print(self.new_detail)
        self.SC.update_stuffdrawpaper(
            autoid=self.autoid, **self.new_detail
        )
        self.get_stuffdrawpaper()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        if self.ori_detail['wdstatus'] != 1:
            return
        self.new_detail['wdstatus'] = 0
        self.new_detail['wdchargerid'] = ''
        self.new_detail['wdchargername'] = ''
        self.new_detail['wddate'] = None
        self.SC.update_stuffdrawpaper(
            autoid=self.autoid, **self.new_detail
        )
        self.get_stuffdrawpaper()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_stufflist_itemDoubleClicked(self, q_treeitem, p_int):
        if self.label_status.text() != "未提交":
            return
        id = int(q_treeitem.text(0))
        detail = EditStuffReturnDetailModule(id, self)
        detail.accepted.connect(self.get_stufflist)
        detail.show()

VALUES_TUPLE_pAPER =(
    'wdchargerid', 'wdchargername', 'wddate', 'wdstatus', 'wddrawerid',
    'wddrawername', 'wddrawdate', 'deptid', 'deptname'
)

VALUES_TUPLE_STUFF = (
            "autoid", "stuffid", "stuffname", "batchno", "spec",
            "package", "presamount", "pracamount", "drawamount",
            "presunit", "pracunit", "drawunit", "restamount", "backamount",
            "wdid", "wdname"
        )