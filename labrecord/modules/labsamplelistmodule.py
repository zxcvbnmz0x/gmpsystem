# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QMenu
from PyQt5.QtCore import Qt, pyqtSlot

from labrecord.controllers.labrecordscontroller import LabrecordsController

from labrecord.views.labsamplelist import Ui_Form
from labrecord.modules.samplingmodule import SamplingModule
from labrecord.modules.checkreportmodule import CheckreportModule


class LabsamplelistModule(QDialog, Ui_Form):
    def __init__(self, parent=None):
        super(LabsamplelistModule, self).__init__(parent)
        self.setupUi(self)
        # 数据库操作类
        self.LC = LabrecordsController()
        self.detail = ''

        # 显示物料列表
        self.show_records_list()
        # 添加右键菜单功能
        self.__add_menu()

    # 添加菜单功能
    def __add_menu(self):
        self.treeWidget_labrecords.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget_labrecords.customContextMenuRequested.connect(self.generate_menu)

    def generate_menu(self, pos):
        # 返回调用者的对象
        sender_widget = self.sender()
        menu = QMenu()
        button1 = menu.addAction("取消取样")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        # 取消取样
        if action == button1:
            autoid=sender_widget.currentItem().text(0)
            res = self.LC.update_labrecord(autoid=autoid, status=0)
            if res:
                self.show_records_list()

    # 显示列表内容
    def show_records_list(self):
        if not len(self.detail):
            values_list = (
                'autoid', 'chkid', 'chkname', 'spec', 'package', 'batchno',
                'mbatchno', 'checkamount', 'caunit', 'sampleamount',
                'sampleunit', 'samplesource', 'applyerid', 'applyername',
                'applydate', 'applyremark', 'samplerid', 'samplername',
                'sampledate', 'remark'
            )
            key_dict = {'status':1}
            self.detail = self.LC.get_labrecord(
                False, *values_list, **key_dict
            )

        self.treeWidget_labrecords.clear()
        tab_index = self.tabWidget.currentIndex()
        content = self.detail.filter(labtype=tab_index)
        # 把树控件移动到当前的页面
        self.gridLayout_2.setParent(getattr(self,'tab_'+str(tab_index)))
        self.gridLayout_2.addWidget(self.treeWidget_labrecords, 0, 0, 1, 1)
        if len(content):
            self.countlabel.setText("共%s条记录" % len(content))
            for item in content:
                qtreeitem = QTreeWidgetItem(self.treeWidget_labrecords)
                qtreeitem.setText(0, str(item['autoid']))
                qtreeitem.setText(1, item['chkid'])
                qtreeitem.setText(2, item['chkname'])
                qtreeitem.setText(3, item['spec'])
                qtreeitem.setText(4, item['package'])
                qtreeitem.setText(5, item['batchno'])
                qtreeitem.setText(6, item['mbatchno'])
                qtreeitem.setText(7, str(item['checkamount']) + item['caunit'])
                qtreeitem.setText(8, str(item['sampleamount']) + item['sampleunit'])
                qtreeitem.setText(9, item['samplesource'])
                qtreeitem.setText(10, item['applyerid'] + ' ' + item['applyername'])
                qtreeitem.setText(11, str(item['applydate']))
                qtreeitem.setText(12, item['applyremark'])
                qtreeitem.setText(13, item['samplerid'] + ' ' + item['samplername'])
                qtreeitem.setText(14, str(item['sampledate']))
                qtreeitem.setText(15, item['remark'])
            # 隐藏第一列的id
            self.treeWidget_labrecords.hideColumn(0)
            for i in range(1, 15):
                self.treeWidget_labrecords.resizeColumnToContents(i)
                if self.treeWidget_labrecords.columnWidth(i) > 200:
                    self.treeWidget_labrecords.setColumnWidth(i, 200)
        else:
            self.countlabel.setText("共0条记录")

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        self.show_records_list()

    # 刷新功能
    @pyqtSlot()
    def on_refreshButton_clicked(self):
        self.show_records_list()

    # 打开记录详情
    @pyqtSlot()
    def on_recordButton_clicked(self):
        qtreeitem = self.treeWidget_labrecords.currentItem()
        if qtreeitem is not None:
            self.on_treeWidget_labrecords_itemDoubleClicked(self.treeWidget_labrecords.currentItem(), 0)

    # 列表双击功能
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_labrecords_itemDoubleClicked(self, qtreeitem, p_int):
        autoid = qtreeitem.text(0)
        detail = SamplingModule(autoid, self)
        detail.accepted.connect(self.show_records_list)
        # 修改了记录，刷新列表
        detail.show()
