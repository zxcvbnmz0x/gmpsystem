# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import user
from django.forms.models import model_to_dict

from lib.utils.saveexcept import SaveExcept

from product.controllers.productcontroller import ProductController
from productline.controllers.productlineconroller import ProductLineConroller

from product.views.editproducingplan import Ui_Dialog

# 产品表字段(Productdictionary)
PRODUCT_VALUE_TUPLE = (
    'autoid', 'prodid', 'prodname', 'commonname', 'spec', 'package')
# 前处理表字段（Stuffdictionary）
STUFF_VALUE_TUPLE = (
    'autoid', 'stuffid', 'stuffname', 'kind', 'spec', 'package')
# 产品查询关键字
PRODUCT_KEY = set(['prodid', 'inputcode', 'prodname', 'commonname'])
# 前处理查询关键字
STUFF_KEY = set(['stuffid', 'inputcode', 'stuffname', 'kind'])
# 下拉表头名
VALUE_NAME = ("id", "编号", "商品名", "通用名", "含量规格", "包装规格")
# 要查询的数据库表名
DB_TABLE = ('Productdictionary', 'Stuffdictionary')


class EditProducingplan(QtWidgets.QDialog, Ui_Dialog):
    flush_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None, autoid=None):
        super().__init__(parent)
        self.product = ProductController()

        self.autoid = autoid
        self.setupUi(self)
        self.prodname.namelist.resize(650, 250)
        self.oridetail = dict()
        self.new_detail = dict()

        self.prodname.setup(DB_TABLE[0], PRODUCT_VALUE_TUPLE, PRODUCT_KEY,
                            VALUE_NAME)

        self.prodname.getItem.connect(self.setproduct)

        if autoid is not None:
            self.set_autoid(autoid)
        else:
            self.makedate.setDate(QtCore.QDate.currentDate())

    def setproduct(self, qtreeitem: QtWidgets.QTreeWidgetItem):
        autoid = qtreeitem.text(0)
        self.commonname.setText(qtreeitem.text(3))
        self.spec.setText(qtreeitem.text(4))
        self.package_2.setText(qtreeitem.text(5))
        if autoid:
            # flag：产品的类型，0成品，1半成品，2退货
            flag = self.productkind.currentIndex()
            res = self.product.get_product_or_stuff(flag, autoid)
            if res:
                self.unit.setText(res.spunit)
                lineid = res.plid
                if lineid:
                    productline = ProductLineConroller()
                    pline = productline.get_productline(lineid, flag)
                    if pline:
                        self.prodline.setText(pline[0].linename)
                        self.productworkshop.setText(
                            pline[0].deptid + ' ' + pline[0].deptname)

    def set_autoid(self, autoid: int):
        self.autoid = autoid
        # 查询autoid对应的记录，并关联到表格中
        self.flush_basedata(self.autoid)
        self.new_detail.clear()

    def flush_basedata(self, autoid):
        res = self.product.get_producingplan(autoid=autoid)
        if res:
            # 把生产指令的内容填入表格中
            self.set_data(res[0])
            self.oridetail = model_to_dict(res[0])
        else:
            errordialig = QtWidgets.QErrorMessage(self)
            errordialig.setWindowTitle("错误")

    # 初始化编辑生产指令的内容
    def set_data(self, detail):
        self.productkind.setCurrentIndex(detail.pltype)
        self.prodname.setText(detail.prodid + ' ' + detail.prodname)
        self.commonname.setText(detail.commonname)
        self.spec.setText(detail.spec)
        self.package_2.setText(detail.package)
        self.planamount.setText(str(detail.planamount))
        self.unit.setText(detail.spunit)
        self.batchno.setText(detail.batchno)
        self.makedate.setDate(
            QtCore.QDate.fromString(str(detail.makedate), QtCore.Qt.ISODate))
        self.remarks.setText(detail.remark)
        lineid = detail.lineid

        if lineid:
            productline = ProductLineConroller()
            pline = productline.get_productline(lineid, detail.pltype)
            if pline:
                self.prodline.setText(pline[0].linename)
                self.productworkshop.setText(
                    pline[0].deptid + ' ' + pline[0].deptname)
                self.new_detail['linename'] = pline[0].linename
                self.new_detail['workshopid'] = pline[0].deptid
                self.new_detail['workshopname'] = pline[0].deptname

    # 产品种类改变时
    @QtCore.pyqtSlot(int)
    def on_productkind_currentIndexChanged(self, p_int):
        if p_int in (0, 2):
            self.prodname.setup(DB_TABLE[0], PRODUCT_VALUE_TUPLE, PRODUCT_KEY,
                                VALUE_NAME)
        else:
            self.prodname.setup(DB_TABLE[1], STUFF_VALUE_TUPLE, STUFF_KEY,
                                VALUE_NAME)

    # 修改计划量时触发
    @QtCore.pyqtSlot(str)
    def on_planamount_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['planamount']:
                self.new_detail['planamount'] = p_str
            else:
                try:
                    del self.new_detail['planamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['planamount'] = p_str

    # 修改批号时触发
    @QtCore.pyqtSlot(str)
    def on_batchno_textEdited(self, p_str):
        try:
            if p_str != self.oridetail['batchno']:
                self.new_detail['batchno'] = p_str
            else:
                try:
                    del self.new_detail['batchno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['batchno'] = p_str

    # 修改生产日期时触发
    @QtCore.pyqtSlot(QtCore.QDate)
    def on_makedate_dateChanged(self, q_date):
        p_date = q_date.toPyDate()
        try:
            if p_date != self.oridetail['makedate']:
                self.new_detail['makedate'] = p_date
            else:
                try:
                    del self.new_detail['makedate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['makedate'] = p_date

    # 修改备注时触发
    @QtCore.pyqtSlot(str)
    def on_remarks_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['remark']:
                self.new_detail['remark'] = p_str
            else:
                try:
                    del self.new_detail['remark']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['remark'] = p_str

    @QtCore.pyqtSlot()
    def on_accept_button_clicked(self):
        if self.prodname.flat == 0:
            errordialig = QtWidgets.QMessageBox(self)
            errordialig.setWindowTitle("错误")
            errordialig.setIcon(QtWidgets.QMessageBox.Critical)
            errordialig.setText("没有找到对应的产品信息，请修改后重试！")
            errordialig.setInformativeText("选择好产品名称后请不要再修改，否则将导致系统无法找到正确的产品！")
            # 添加Yes和No2个按键

            errordialig.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            button_yes = errordialig.button(QtWidgets.QMessageBox.Yes)
            button_yes.setText("确认")
            button_no = errordialig.button(QtWidgets.QMessageBox.No)
            button_no.setText("取消")
            errordialig.exec()
            self.prodname.setFocus()
        # 有修改过数据
        if self.new_detail:
            try:
                # 修改过记录，把当前的人员和日期存入修改记录中
                self.new_detail['instructorid'] = user.user_id
                self.new_detail['instructorname'] = user.user_name
                self.new_detail['plandate'] = user.now_date
                self.new_detail['deptid'] = user.dept_id
                self.new_detail['deptname'] = user.dept_name
                self.new_detail['bpconstitutorid'] = user.user_id
                self.new_detail['bpconstitutorname'] = user.user_name
                self.new_detail['bpconsdate'] = user.now_date

                # autoid不为空，则为修改记录
                # 否则为插入记录
                if self.autoid:
                    res = self.product.update_producingplan(autoid=self.autoid,
                                                            **self.new_detail)
                    if res == 1:
                        self.flush_signal.emit()
                        self.accept()
                else:
                    prodtype = self.productkind.currentIndex()
                    prod_id = self.prodname.namelist.currentItem().text(0)
                    self.new_detail['id'] = prod_id
                    res = self.product.update_producingplan(
                        prodtype=prodtype, **self.new_detail
                    )
                    if res:
                        self.flush_signal.emit()
                        self.accept()
            except Exception as e:
                SaveExcept(e, "提交生产指令时出错", **self.new_detail)
        else:
            self.close()

    @QtCore.pyqtSlot()
    def on_cancel_button_clicked(self):
        self.close()
