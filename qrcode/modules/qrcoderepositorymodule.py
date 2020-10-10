# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QFileDialog, QTreeWidgetItem, QMenu, \
    QApplication

from PyQt5.QtCore import pyqtSlot, QPoint

from qrcode.controlllers.qrcodecontroller import QrcodeController

from qrcode.views.qrcoderepository import Ui_Form

from lib.utils.messagebox import MessageBox

import datetime
import re

import user


class QrcoderepositoryModule(QWidget, Ui_Form):
    """ 二维码库模块，可以查看到所有已经上传了的二维码的使用记录。
    提供了右键上传二维码的功能。
    """

    def __init__(self, parent=None):
        super(QrcoderepositoryModule, self).__init__(parent)
        self.setupUi(self)
        self.QC = QrcodeController()
        # 获取二维码信息
        self.get_qrcoderepository()

    def get_qrcoderepository(self):
        self.treeWidget_qrcode.clear()
        self.treeWidget_qrcode.hideColumn(0)
        res = self.QC.get_qrcoderep(False, *VALUES_LIST)
        if not len(res):
            return
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_qrcode)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['qrcode'])
            qtreeitem.setText(2, item['prodname'])
            qtreeitem.setText(3, item['allowno'])
            qtreeitem.setText(4, item['companyname'])
            qtreeitem.setText(5, item['telno'])
            qtreeitem.setText(6, str(item['createdate']))
            qtreeitem.setText(7, str(item['useddate']) if type(
                item['useddate']) is datetime.date else '')
            qtreeitem.setText(8, USED_STATUS[item['used']])
        for i in range(1, 9):
            self.treeWidget_qrcode.resizeColumnToContents(i)

    @pyqtSlot(QPoint)
    def on_treeWidget_qrcode_customContextMenuRequested(self, pos):
        menu = QMenu()
        button1 = menu.addAction("上传二维码文件")
        g_pos = self.treeWidget_qrcode.mapToGlobal(pos)
        action = menu.exec(g_pos)
        if action == button1:
            clipboard = QApplication.clipboard()
            dir = clipboard.property("fileurl")
            if not dir:
                dir = "c:\\"
            files_route, file_types = QFileDialog.getOpenFileNames(
                self, "选择文件", dir, "*.txt;;All Files(*)"
            )
            if not files_route:
                return
            informative = ''
            selected_dir = re.split(r'\w+.txt', files_route[0])[0]
            clipboard.setProperty("fileurl", selected_dir)
            for file_route in files_route:
                if not file_route.endswith(".txt"):
                    informative += file_route + "文件后缀错误\n"
                    continue
                filename = re.findall(r'\w+.txt', file_route)[0].split(".")[0]
                with open(file_route) as f:
                    try:
                        lines = f.readlines()
                    except UnicodeDecodeError:
                        informative += filename + "：编码格式错误\n"
                        continue
                    qrcode_list = []
                    for i in range(1, len(lines)):
                        content = lines[i].strip()
                        text = re.split(r',|，', content)
                        if len(text) != 5:
                            continue
                        text.append(user.now_date)
                        qrcode_list.append(text)
                    if not len(qrcode_list):
                        informative += filename + "：文件格式错误\n"
                        continue
                    res = self.QC.update_qrcoderep(None, *qrcode_list)
                    if res == 1062:
                        informative += filename + "：二维码重复\n"
            if informative:
                msg = MessageBox(
                    text="以下文件上传失败：", informative=informative
                )
                msg.exec()
            self.get_qrcoderepository()


VALUES_LIST = (
    'autoid', 'qrcode', 'prodname', 'allowno', 'companyname', 'telno',
    'createdate', 'useddate', 'used'
)
USED_STATUS = ("未使用", "已使用")
