# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QKeyEvent, QFocusEvent
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from product.controllers.productcontroller import ProductController
from workshop.controllers.workshopcontroller import WorkshopController

from workshop.views.scanqrcode import Ui_Dialog

from lib.utils.messagebox import MessageBox, msgdialog
from lib.utils.tts import Tts


class ScanqrcodeModule(QDialog, Ui_Dialog):
    applyed = pyqtSignal(list, str)

    def __init__(self, ppid, parent=None):
        # b,m,s分别对应大、中、小包装
        # num 为已经扫描的个数
        # amount 为包装比例
        super(ScanqrcodeModule, self).__init__(parent)
        self.PC = ProductController()
        self.WC = WorkshopController()
        self.msg = msgdialog(parent=self)
        self.tts = Tts()
        self.tts.start()
        self.ppid = ppid

        self.batchno = '0'

        self.lpid = None
        self.bpid = None
        self.mpid = None

        self.lpnum = 0
        self.bpnum = 0
        self.mpnum = 0
        self.spnum = 0

        self.bpamount = 0
        self.mpamount = 0
        self.spamount = 0
        self.use_lv_qrcode = []

        self.setupUi(self)
        qrtype = self.get_prod_packagelv()
        self.qrcode = AboxQrcode(
            qrtype, self.bpamount, self.mpamount, self.spamount
        )
        if qrtype == 7:
            # 00111
            self.lineEdit_spqrcode.setEnabled(False)
            self.spamount = 0
            self.use_lv_qrcode = ['lp', 'bp', 'mp']
        elif qrtype == 10:
            # 01010
            self.lineEdit_lpqrcode.setEnabled(False)
            self.lineEdit_mpqrcode.setEnabled(False)
            self.mpamount = 0
            self.use_lv_qrcode = ['bp', 'sp']
            self.lineEdit_bpqrcode.setFocus()
        elif qrtype == 11:
            # 01011
            self.lineEdit_mpqrcode.setEnabled(False)
            self.mpamount = 0
            self.use_lv_qrcode = ['lp', 'bp', 'sp']
        elif qrtype == 13:
            # 01101
            self.lineEdit_bpqrcode.setEnabled(False)
            self.bpamount = 0
            self.use_lv_qrcode = ['lp', 'mp', 'sp']
        elif qrtype == 14:
            # 01110
            self.lineEdit_bpqrcode.setFocus()
            self.lineEdit_lpqrcode.setEnabled(False)
            self.use_lv_qrcode = ['bp', 'mp', 'sp']
        elif qrtype == 16:
            self.lineEdit_bpqrcode.setEnabled(False)
            self.lineEdit_lpqrcode.setEnabled(False)
            self.bpamount = 0
            self.use_lv_qrcode = ['mp', 'sp']
            self.lineEdit_mpqrcode.setFocus()

    def get_prod_packagelv(self):
        key_dict_prod = {
            'autoid': self.ppid
        }
        res = self.PC.get_producingplan(
            False, *value_list_prod, **key_dict_prod
        )
        if len(res) != 1:
            return
        self.batchno = res[0]['batchno']
        self.bpamount = res[0]['bpamount']
        self.mpamount = res[0]['mpamount']
        self.spamount = res[0]['spamount']
        return res[0]['qrtype']

    @pyqtSlot()
    def on_lineEdit_spqrcode_focused(self):
        self.tts.say("请扫描小包装二维码")

    @pyqtSlot()
    def on_lineEdit_mpqrcode_focused(self):
        if self.mpnum >= self.mpamount:
            self.focusPreviousChild()
            return
        self.tts.say("请扫描中包装二维码")

    @pyqtSlot()
    def on_lineEdit_bpqrcode_focused(self):
        if self.bpnum >= self.bpamount:
            self.focusPreviousChild()
            return
        self.tts.say("请扫描大包装二维码")

    @pyqtSlot()
    def on_lineEdit_lpqrcode_focused(self):
        self.tts.say("请扫描巨包装二维码")

    @pyqtSlot()
    def on_lineEdit_spqrcode_returnPressed(self):
        p_str = self.lineEdit_spqrcode.text()
        self.plainTextEdit_spqrcode.appendPlainText(p_str)
        data = p_str.replace('，', ',')
        qrcode = data.split(',')[0]
        self.lineEdit_spqrcode.clear()
        # if len(qrcode0) != 24:
        #     # 二维码长度不对
        #     text = qrcode0 + ":二维码格式错误\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     self.tts.say("错码")
        #     return
        # key_dict_qrcode_rep['qrcode'] = qrcode0
        # res = self.WC.get_qrcoderep(
        #     True, *value_list_qrcode_rep, **key_dict_qrcode_rep
        # )
        # if len(res) == 0:
        #     # 二维码库中无此二维码
        #     text = qrcode0 + ":二维码库中无此二维码\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     self.tts.say("错码")
        #     return
        # elif res[0] == 1:
        #     # 此二维码已经被使用
        #     text = qrcode0 + ":此二维码已被使用\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     return

        self.qrcode.set_qrcode(0, self.mpid, qrcode)
        self.spnum += 1
        self.tts.say(str(self.spnum) + "个")
        if self.spnum >= self.spamount:
            self.spnum = 0
            if self.qrcode.is_enough_qrcode():
                self.lpnum = 0
                self.bpnum = 0
                self.mpnum = 0
                qrcode_list = self.qrcode.get_qrcode_list()
                self.applyed.emit(qrcode_list, self.batchno)
                self.qrcode.reset()

                if self.lineEdit_lpqrcode.isEnabled():
                    self.lineEdit_lpqrcode.setFocus()
                elif self.lineEdit_bpqrcode.isEnabled():
                    self.lineEdit_bpqrcode.setFocus()
                elif self.lineEdit_mpqrcode.isEnabled():
                    self.lineEdit_mpqrcode.setFocus()
                return


            if self.lineEdit_mpqrcode.isEnabled():
                if self.mpnum < self.mpamount:
                    self.lineEdit_mpqrcode.setFocus()
            elif self.lineEdit_bpqrcode.isEnabled():
                if self.bpnum < self.bpamount:
                    self.lineEdit_bpqrcode.setFocus()
            elif self.lineEdit_lpqrcode.isEnabled():
                self.lineEdit_lpqrcode.setFocus()

    @pyqtSlot()
    def on_lineEdit_mpqrcode_returnPressed(self):
        p_str = self.lineEdit_mpqrcode.text()
        self.plainTextEdit_mpqrcode.appendPlainText(p_str)
        data = p_str.replace('，', ',')
        qrcode = data.split(',')[0]
        self.lineEdit_mpqrcode.clear()
        # if len(qrcode0) != 24:
        #     # 二维码长度不对
        #     text = qrcode0 + ":二维码格式错误\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     self.tts.say("错码")
        #     return
        # key_dict_qrcode_rep['qrcode'] = qrcode0
        # res = self.WC.get_qrcoderep(
        #     True, *value_list_qrcode_rep, **key_dict_qrcode_rep
        # )
        # if len(res) == 0:
        #     # 二维码库中无此二维码
        #     text = qrcode0 + ":二维码库中无此二维码\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     self.tts.say("错码")
        #     return
        # elif res[0] == 1:
        #     # 此二维码已经被使用
        #     text = qrcode0 + ":此二维码已被使用\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     return

        self.mpid = self.qrcode.set_qrcode(1, self.bpid, qrcode)
        index = self.use_lv_qrcode.index('mp')
        if index <= len(self.use_lv_qrcode) - 1:
            spnum = self.qrcode.set_parent_id(0, self.mpid)
        self.mpnum += 1
        # self.tts.say(str(self.mpnum) + "个")

        if spnum < self.spamount:
            # 小包装没有扫够
            self.lineEdit_spqrcode.setFocus()
        # 扫完一箱里的中包装码,且大包装没扫满
        elif spnum >= self.spamount and self.mpnum >= self.mpamount and \
                self.bpnum < self.bpamount:
            # 小包装扫够了且中包装也扫够了
            self.mpid = None
            if self.lineEdit_bpqrcode.isEnabled():
                self.lineEdit_bpqrcode.setFocus()
            elif self.lineEdit_lpqrcode.isEnabled():
                self.lineEdit_lpqrcode.setFocus()
            else:
                self.mpnum = 0

    @pyqtSlot()
    def on_lineEdit_bpqrcode_returnPressed(self):
        p_str = self.lineEdit_bpqrcode.text()
        self.plainTextEdit_bpqrcode.appendPlainText(p_str)
        data = p_str.replace('，', ',')
        qrcode = data.split(',')[0]
        self.lineEdit_bpqrcode.clear()
        # if len(qrcode0) != 24:
        #     # 二维码长度不对
        #     text = qrcode0 + ":二维码格式错误\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     self.tts.say("错码")
        #     return
        # key_dict_qrcode_rep['qrcode'] = qrcode0
        # res = self.WC.get_qrcoderep(
        #     True, *value_list_qrcode_rep, **key_dict_qrcode_rep
        # )
        # if len(res) == 0:
        #     # 二维码库中无此二维码
        #     text = qrcode0 + ":二维码库中无此二维码\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     self.tts.say("错码")
        #     return
        # elif res[0] == 1:
        #     # 此二维码已经被使用
        #     text = qrcode0 + ":此二维码已被使用\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     return

        self.bpid = self.qrcode.set_qrcode(2, self.lpid, qrcode)
        index = self.use_lv_qrcode.index('bp')
        if index <= len(self.use_lv_qrcode) - 1:
            child = self.use_lv_qrcode[index+1]
            flag = 0 if child=='sp' else 1
            self.qrcode.set_parent_id(flag, self.bpid)
        self.bpnum += 1
        # self.tts.say(str(self.spnum) + "个")
        if self.lineEdit_mpqrcode.isEnabled():
            # 中包装允许扫码且没有扫够
            if self.mpnum < self.mpamount:
                self.lineEdit_mpqrcode.setFocus()
            elif self.lineEdit_lpqrcode.isEnabled():
                if self.bpnum < self.bpamount:
                    self.bpnum = 0
                    self.bpid = None
                else:
                    self.lineEdit_lpqrcode.setFocus()


    @pyqtSlot()
    def on_lineEdit_lpqrcode_returnPressed(self):
        p_str = self.lineEdit_mpqrcode.text()
        self.plainTextEdit_mpqrcode.appendPlainText(p_str)
        data = p_str.replace('，', ',')
        qrcode = data.split(',')[0]
        self.lineEdit_lpqrcode.clear()
        # if len(qrcode0) != 24:
        #     # 二维码长度不对
        #     text = qrcode0 + ":二维码格式错误\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     self.tts.say("错码")
        #     return
        # key_dict_qrcode_rep['qrcode'] = qrcode0
        # res = self.WC.get_qrcoderep(
        #     True, *value_list_qrcode_rep, **key_dict_qrcode_rep
        # )
        # if len(res) == 0:
        #     # 二维码库中无此二维码
        #     text = qrcode0 + ":二维码库中无此二维码\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     self.tts.say("错码")
        #     return
        # elif res[0] == 1:
        #     # 此二维码已经被使用
        #     text = qrcode0 + ":此二维码已被使用\n"
        #     self.textEdit_errorlist.insertPlainText(text)
        #     return

        self.lpid = self.qrcode.set_qrcode(3, None, qrcode)
        index = self.use_lv_qrcode.index('lp')
        if index <= len(self.use_lv_qrcode) - 1:
            child = self.use_lv_qrcodep[index + 1]
            flag = 0 if child == 'sp' else 1 if child == 'mp' else 2
            self.qrcode.set_parent_id(flag, self.lpid)
        self.mpnum += 1
        self.tts.say(str(self.mpnum) + "个")
        if self.mpnum >= self.mpamount:
            self.groupBox_bpqrcode.setFocus()
            self.mpnum = 0
            self.bpid = None

    @pyqtSlot()
    def on_pushButton_nextbox_clicked(self):
        qrcode_list = self.qrcode.get_qrcode_list()
        self.applyed.emit(qrcode_list, self.batchno)
        self.qrcode.reset()
        if self.lineEdit_lpqrcode.isEnabled():
            self.lineEdit_lpqrcode.setFocus()
        elif self.lineEdit_bpqrcode.isEnabled():
            self.lineEdit_lpqrcode.setFocus()
        elif self.lineEdit_mpqrcode.isEnabled():
            self.lineEdit_lpqrcode.setFocus()
        else:
            self.lineEdit_spqrcode.setFocus()

    def closeEvent(self, e):
        print(e)
        qrcode_list = self.qrcode.get_qrcode_list()
        print(qrcode_list)
        self.applyed.emit(qrcode_list, self.batchno)


class AboxQrcode(object):
    def __init__(self, qrtype, bpamount, mpamount, spamount):

        self.bpamount = bpamount if bpamount != 0 else 1
        self.mpamount = mpamount if mpamount != 0 else 1
        self.spamount = spamount if spamount != 0 else 1
        # 00110
        b_qrtype = bin(qrtype)
        if len(b_qrtype[2:]) < 5:
            b_qrtype = '0'*(5-len(b_qrtype[2:])) + b_qrtype[2:]
        self.lpcount = 1 if b_qrtype[4] == '1' else 0
        self.bpcount = bpamount if b_qrtype[3] else 0
        self.mpcount = mpamount * bpamount if b_qrtype[2] == '1' else 0
        self.spcount = spamount * mpamount * bpamount if b_qrtype[1] == '1' else 0
        if b_qrtype[0] == 1:
            self.lpcount = 0
            self.bpcount = 0
            self.mpcount = 0

        self.lpqrcode = []
        self.bpqrcode = []
        self.mpqrcode = []
        self.spqrcode = []
        self.lpid = 0
        self.bpid = 0
        self.mpid = 0
        self.spid = 0

    def is_enough_qrcode(self):
        if len(self.lpqrcode)>= self.lpcount and len(self.bpqrcode) >= \
                self.bpamount and len(self.mpqrcode) >= self.mpamount and \
                len(self.spqrcode) >= self.spamount:
            return True
        else:
            return False

    def set_qrcode(self, flag, parent_id, qrcode):
        if flag == 0:
            self.spqrcode.append([0, parent_id, qrcode])
        elif flag == 1:
            self.mpid += 1
            self.mpqrcode.append([self.mpid, parent_id, qrcode])
            return self.mpid
        elif flag == 2:
            self.bpid += 1
            self.bpqrcode.append([self.bpid, parent_id, qrcode])
            return self.bpid
        elif flag == 3:
            self.lpid += 1
            self.lpqrcode = (self.lpid, 0, [qrcode])
            return self.lpid

    def set_parent_id(self, flag, id):
        change_num = 0
        if flag == 0:
            for item in self.spqrcode:
                if item[1] == None:
                    item[1] = id
                    change_num += 1
        elif flag == 1:
            for item in self.mpqrcode:
                if item[1] == None:
                    item[1] = id
                    change_num += 1
        elif flag == 2:
            for item in self.bpqrcode:
                if item[1] == None:
                    item[1] = id
                    change_num += 1
        return change_num

    def get_qrcode_list(self):
        if len(self.lpqrcode) == 0:
            self.lpqrcode.append([None, None, ''])
        if len(self.bpqrcode) == 0:
            self.bpqrcode.append([None, None, ''])
        if len(self.mpqrcode) == 0:
            self.mpqrcode.append([None, None, ''])
        if len(self.spqrcode) == 0:
            self.spqrcode.append([None, None, ''])
        qrcode_list = []
        for lpitem in self.lpqrcode:
            lpid = lpitem[0]
            for bpitem in self.bpqrcode:
                bpid = bpitem[0]
                if bpitem[1] != lpid:
                    continue
                for mpitem in self.mpqrcode:
                    mpid = mpitem[0]
                    if mpitem[1] != bpid:
                        continue
                    for spitem in self.spqrcode:
                        if spitem[1] != mpid:
                            continue
                        qrcode_list.append(
                            (spitem[2], mpitem[2], bpitem[2], lpitem[2])
                        )
        return qrcode_list

    def reset(self):
        self.lpqrcode = []
        self.bpqrcode = []
        self.mpqrcode = []
        self.spqrcode = []
        self.lpid = 0
        self.bpid = 0
        self.mpid = 0
        self.spid = 0


value_list_prod = ('batchno', 'bpamount', 'mpamount', 'spamount', 'qrtype')

value_list_qrcode_rep = ('used',)
key_dict_qrcode_rep = {
    'qrcode': ''
}
value_list_qrcode_prod = ('used',)
key_dict_qrcode_prod = {
    'qrcode': ''
}