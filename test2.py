from PyQt5.QtCore import QDate, pyqtSlot

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, \
    QLabel, QPushButton
from stuff.modules.stuffdrawpapermodule import StuffdrawpaperModule


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

from django.db.models import CharField
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
from sale.modules.saleordermodule import SaleOrderModule
from sale.modules.editsaleprodmodule import EditSaleProdMudule
from warehouse.modules.productputoutpaperlistmodule import ProductPutOutPaperListModule
from warehouse.modules.editproductputoutpapermodule import EditProductPutOutPaperModule
from warehouse.modules.scanppopqrcodemodule import ScanPpopQrcodeMudule
from workshop.modules.homepagemodule import HomePageModule
from stuff.modules.stuffreturnpapermodule import StuffReturnPaperModule
from warehouse.modules.stuffreturnlistmodule import StuffReturnListModule
from warehouse.modules.preprodputinlistmodule import PreProdputinlistModule
if __name__ == "__main__":

    app = QApplication(sys.argv)

    # form = StuffReturnPaperModule(1360)
    form = PreProdputinlistModule()
    # form = StuffReturnListModule()
    form.show()
    sys.exit(app.exec_())



