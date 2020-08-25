# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from django.forms.models import model_to_dict

from product.modules.productdetailmodule import ProductDetailModule
from productline.controllers.productlineconroller import ProductLineConroller

from product.models.productmodel import ProductModel


# 检验结果的类型和入库类型
RESTYPE = ("文本", "数据")
PUTINTYPE = ("无", "含量", "水分", "效价", "相对密度", "杂质")


# 物料详细资料页面，
# 如果没有传入autoid，则默认为新建界面
# 若传入autoid，则查询后返回找到的内容，
# 若无对应的autoid则返回错误信息
class ProductDetail(ProductDetailModule):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 数据库操作类
        self.sd = ProductModel()

    def set_autoid(self, autoid: int):
        self.autoid = autoid
        # 查询autoid对应的记录，并关联到表格中
        self.flush_basedata(self.autoid)
        self.new_detail.clear()

    def flush_basedata(self, autoid):
        stuff_detail = self.sd.get_product(self.autoid)
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
        self.prodid.setText(detail.prodid)
        self.prodname.setText(detail.prodname)
        self.commonname.setText(detail.commonname)
        self.medkind.setCurrentText(detail.medkind)
        self.externalno.setText(detail.externalno)
        self.allowno.setText(detail.allowno)
        self.inputcode.setText(detail.inputcode)
        self.spec.setText(detail.spec)
        self.packageLv.setCurrentIndex(int(detail.packagelv))
        self.package_2.setText(detail.package)
        self.checkunit.setCurrentIndex(detail.checkunit)
        self.expireddates.setText(str(detail.expireddates))
        self.storage.setText(detail.storage)

        if detail.plid:
            productline = ProductLineConroller()
            productlinedetail = productline.get_productline(autoid=detail.plid)
            if productlinedetail:
                self.workshop.setText(productlinedetail[0].deptname)
                self.productionline.setText(productlinedetail[0].linename)

        if detail.wplid:
            productline = ProductLineConroller()
            productlinedetail = productline.get_productline(autoid=detail.wplid)
            if productlinedetail:
                self.bworkshop.setText(productlinedetail[0].deptname)
                self.bproductionline.setText(productlinedetail[0].linename)