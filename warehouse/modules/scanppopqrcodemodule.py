# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from warehouse.views.scanppopqrcode import Ui_Dialog
from warehouse.controllers.warehousecontroller import WarehouseController

from lib.utils.tts import Tts


class ScanPpopQrcodeMudule(QDialog, Ui_Dialog):
    qrcodeAdded = pyqtSignal()

    def __init__(self, ppopid, parent=None):
        super(ScanPpopQrcodeMudule, self).__init__(parent)
        self.setupUi(self)
        self.ppopid = ppopid
        self.WC = WarehouseController()
        self.kind = 0
        self.tts = Tts()
        self.tts.start()
        self.lineEdit_qrcode.setFocus()

    @pyqtSlot()
    def on_lineEdit_qrcode_returnPressed(self):
        p_str = self.lineEdit_qrcode.text()
        self.plainTextEdit_qrcode.appendPlainText(p_str)
        # 把中文的逗号替换为英文的逗号，防止后续分割字符串时出错
        data = p_str.replace('，', ',')
        qrcode = data.split(',')[0]
        self.lineEdit_qrcode.clear()
        if len(qrcode) != 2:
            # 二维码长度不是24位
            text = qrcode + ":二维码格式错误\n"
            self.plainTextEdit_errormsg.insertPlainText(text)
            self.tts.say("错码")
            return
        status, flag, amount, ppid, batchno = self.WC.find_prodqrcode(qrcode)

        if status == 0:
            detail = {
                'ppopid': self.ppopid,
                'ppid': ppid,
                'batchno': batchno,
                'qr0': qrcode,
                'flag': flag,
                'kind': self.kind,
                'amount': amount
            }
            self.WC.add_ppopqrocde(flag, qrcode, detail)
            self.qrcodeAdded.emit()
        elif status == 1:
            # 此二维码已经被使用
            text = qrcode + ":此二维码已被使用\n"
            self.plainTextEdit_errormsg.insertPlainText(text)
            self.tts.say("虫码")

        elif status == 2:
            # 此二维码已经被使用
            text = qrcode + ":此二维码/部分下级码已被使用\n"
            self.plainTextEdit_errormsg.insertPlainText(text)
            self.tts.say("虫码")

        elif status == 3:
            # 此二维码已经被使用
            text = qrcode + ":产品库中无此二维码\n"
            self.plainTextEdit_errormsg.insertPlainText(text)
            self.tts.say("错码")
        else:
            # 没有匹配到符合的情况，查询结果异常
            text = qrcode + ":二维码异常\n"
            self.plainTextEdit_errormsg.insertPlainText(text)
            self.tts.say("错码")

    @pyqtSlot(bool)
    def on_radioButton_0_toggled(self, p_bool):
        if p_bool:
            self.kind = 0

    @pyqtSlot(bool)
    def on_radioButton_1_toggled(self, p_bool):
        if p_bool:
            self.kind = 1

    @pyqtSlot(bool)
    def on_radioButton_2_toggled(self, p_bool):
        if p_bool:
            self.kind = 2

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

