# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from django.forms.models import model_to_dict

from stuff.modules.stuffmodule import StuffModule
from productline.controllers.productlineconroller import ProductLineConroller

from stuff.models.stuffmodel import StuffModel


# 检验结果的类型和入库类型
RESTYPE = ("文本", "数据")
PUTINTYPE = ("无", "含量", "水分", "效价", "相对密度", "杂质")


# 物料详细资料页面，
# 如果没有传入autoid，则默认为新建界面
# 若传入autoid，则查询后返回找到的内容，
# 若无对应的autoid则返回错误信息
class StuffDetail(StuffModule):
    def __init__(self, parent=None):
        super(StuffDetail, self).__init__(parent)
        # 数据库操作类
        self.sd = StuffModel()


    def set_autoid(self, autoid):
        self.autoid = autoid
        # 若autoid不为空，则查询对应的记录，并关联到表格中
        if self.autoid:
            self.flush_basedata(self.autoid)
            self.new_detail.clear()
        else:
            raise TypeError

    def flush_basedata(self, autoid):
        stuff_detail = self.sd.get_stuff(self.autoid)
        if stuff_detail:
            self.set_data(stuff_detail)
            self.oridetail = model_to_dict(stuff_detail)
        else:
            errordialig = QtWidgets.QErrorMessage(self)
            errordialig.setWindowTitle("错误")
            # errordialig.setIcon(QtWidgets.QMessageBox.Warning)
            # errordialig.setText("没有找到对应的记录，请刷新后重试！")
            # 添加Yes和No2个按键
            # errordialig.setStandardButtons(
            ##button_yes = errordialig.button(QtWidgets.QMessageBox.Yes)
            # button_yes.setText("确认")
            # button_no = errordialig.button(QtWidgets.QMessageBox.No)
            # button_no.setText("取消")

    def set_data(self, detail):
        self.stufftype.setCurrentIndex(int(detail.stufftype))
        self.stuffid.setText(detail.stuffid)
        self.stuffname.setText(detail.stuffname)
        self.kind.setText(detail.kind)
        self.externalno.setText(detail.externalno)
        self.allowno.setText(detail.allowno)
        self.inputcode.setText(detail.inputcode)
        self.spec.setText(detail.spec)
        self.packageLv.setCurrentIndex(int(detail.packagelv))
        self.package_2.setText(detail.package)
        self.purchasingunit.setCurrentIndex(detail.unit)
        self.checkunit.setCurrentIndex(detail.checkunit)
        self.lowlimit.setText(str(detail.lowlimit))
        self.upperlimit.setText(str(detail.upperlimit))
        self.recheck.setText(str(detail.countercheckdays))
        self.expired.setText(str(detail.expireddays))
        self.ceffectunit.setText(detail.cunit)
        if detail.cstandard != 0:
            self.ceffect.setText(str(detail.cstandard))
        self.storage.setText(detail.storage)
        # 若为前处理，则不显示原料检验项目和供应商和生产厂家
        if detail.stufftype == 1:
            # 删除原料检验项目
            self.tab.removeTab(1)
            # 删除供应商和生产厂家
            # 由于前面删除了一个，所以序号往前了
            self.tab.removeTab(3)
        else:
            # 删除前处理配方和前处理检验项目
            self.tab.removeTab(2)
            self.tab.removeTab(2)
            self.workshoplabel.setVisible(False)
            self.workshop.setVisible(False)
            self.productionlinelabel.setVisible(False)
            self.productionline.setVisible(False)
        if detail.plid:
            productline = ProductLineConroller()
            productlinedetail = productline.get_productline(autoid=detail.plid)
            if productlinedetail:
                self.workshop.setText(productlinedetail[0].deptname)
                self.productionline.setText(productlinedetail[0].linename)
