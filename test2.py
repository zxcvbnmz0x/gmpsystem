import decimal
from db.models import Productstuff,Workflow, Linepost,Eqrunnotes
from django.db import connection,transaction
import sys,datetime
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication  ,QWidget,QLineEdit, QDialog
from PyQt5.QtGui import   QPainter ,QPixmap, QPen
from PyQt5.QtCore import Qt , QPoint, QDate,QFile, QUrl,QTextStream,QIODevice,QByteArray, pyqtSlot
from PyQt5.QtXmlPatterns import QXmlQuery
from PyQt5.QtXml import QDomDocument,QDomNode,QDomElement
from equipment.controllers.equipmentcontroller import EquipmentController

from django.forms import model_to_dict
import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, \
    QLabel, QPushButton
from PyQt5.QtCore import QDateTime
from lib.sign.signbutton import SignButton
from equipment.modules.eqrunnotedodule import EqrunnoteModule
from stuff.modules.stuffdrawpapermodule import StuffdrawpaperModule
from warehouse.modules.drawstuffmodule import DrawstuffModule
from warehouse.modules.stuffpickingmodule import StuffpickingModule

class Winform(QWidget):
    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)
        self.setWindowTitle("窗体布局管理例子")
        self.resize(400, 100)

        fromlayout = QFormLayout()
        labl1 = QLabel("标签1")
        lineEdit1 = QPushButton()
        labl2 = QLabel("标签2")
        lineEdit2 = QLineEdit()
        labl3 = QLabel("标签3")
        lineEdit3 = QLineEdit()

        fromlayout.addRow(labl1, lineEdit1)
        fromlayout.addRow(labl2, lineEdit2)
        fromlayout.addRow(labl3, lineEdit3)

        self.setLayout(fromlayout)
        lineEdit1.clicked.connect(self.a)
    def a(self):
        s = StuffdrawpaperModule(6781, 0, parent=self)
        res = s.show()
        print(res)

from django.db.models import Aggregate, CharField
from django.db.models.expressions import Func
class Concat(Func):
    """ORM用来分组显示其他字段 相当于group_concat"""
    function = 'CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)
        print(expression)
        print(distinct)
        print(extra)


from PyQt5.QtWidgets import QTreeWidgetItem
from db.models import Productstuff
from lib.utils.inputcode import Inputcode
from labrecord.modules.applycheckmodule import ApplycheckModule
from labrecord.modules.labsamplelistmodule import LabsamplelistModule
from labrecord.modules.labreportlistmodule import LabreportlistModule
from labrecord.modules.checkreportmodule import CheckreportModule
from workshop.modules.productioninstructionmodule import PorductionInstructionModule
from workshop.modules.packageinstructionmodule import PackageInstructionModule
from workshop.modules.midproddrawnotemodule import MidproddrawnoteModule
from workshop.modules.midproddetailmodule import MidproddetailModule
from workshop.modules.oddmentregisternotemodule import OddmentregisternoteModule
from workshop.modules.oddmentdrawnotemodule import OddmentdrawnoteModule
from workshop.modules.oddmentdetailmodule import OddmentdetailModule
from warehouse.modules.oddmentputinnotemodule import OddmentputinnoteModule
from workshop.modules.productputinnotemodule import ProductputinModule
from warehouse.modules.productputinlistmodule import ProductputinlistModule
from workshop.modules.qrcodelistmodule import QrcodelistModule
from workshop.modules.scanqrcodemodule import ScanqrcodeModule
from qrcode.modules.qrcodeinputmodule import QrcodeinputModule
from qrcode.modules.qrcodeoutputmodule import QrcodeoutputModule
from qrcode.modules.qrcodereturnmodule import QrcodereturnModule
from supplyer.modules.purchasingplanmodule import PurchasingplanModule

import re
from db.models import Relativepictures, Imagelib

class a():
    b = 0

    @pyqtSlot(QDate)
    def on_dateEdit_bpdate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['bpdate']) is str:
                self.new_detail['bpdate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['bpdate']):
                self.new_detail['bpdate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['bpdate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['bpdate'] = q_date.toPyDate()

# 修改备注时触发
@pyqtSlot(str)
def on_lineEdit_remark_textChanged(self, p_str):
    try:
        if p_str != self.ori_detail['remark']:
            self.new_detail['remark'] = p_str
        else:
            try:
                del self.new_detail['remark']
            except KeyError:
                pass
    except KeyError:
        self.new_detail['remark'] = p_str


    @pyqtSlot(str)
    def on_pushButton_warrantor_signChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['warrantorid'] or name != self.ori_detail[
                'warrantorname']:
                self.new_detail['warrantorid'] = id
                self.new_detail['warrantorname'] = name
            else:
                try:
                    del self.new_detail['warrantorid']
                    del self.new_detail['warrantorname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['warrantorid'] = id
            self.new_detail['warrantorname'] = name
import datetime

datetime.date.today()
from supplyer.modules.purchasingplanmodule import PurchasingplanModule
from warehouse.modules.editregstuffmodule import EditRegStuffModule
from warehouse.modules.purchaseregistrationmodule import PurchaseRegistrationModule
from warehouse.modules.purstuffcheckinmodule import PurStuffCheckInModule
from warehouse.modules.editstuffcheckin import EditStuffCheckInModule
if __name__ == "__main__":

    app = QApplication(sys.argv)

    form = PurStuffCheckInModule()
    form.show()
    sys.exit(app.exec_())



