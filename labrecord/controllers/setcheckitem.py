# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from django.forms.models import model_to_dict
from lib.utils.saveexcept import SaveExcept
from labrecord.models.checkitem import CheckItem

from labrecord.views.checkitem import Ui_Dialog




# 检验项目详细资料页面，
# 如果没有传入autoid，则默认为新建界面
# 若传入autoid，则查询后返回找到的内容，
# 若无对应的autoid则返回错误信息
class SetCheckItem(QtWidgets.QDialog, Ui_Dialog):
    flush_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None, autoid=None):
        super().__init__(parent)
        self.autoid = autoid
        # 存放当前数据
        self.detail = dict()
        self.oridetail = dict()
        self.setupUi(self)
        # 数据库操作类
        self.check_item = CheckItem()
        if self.autoid:
            self.flush_basedata(self.autoid)
        # 把所有预定义好的信号连接到槽
        self.signal_connect_slit()

    # 设置要保存的参数名和值
    # 先判断self.detail里有没有这个变量
    # 若不存在则加入，否则跳过操作
    def set_variable(self, var_name, var_value):
        self.detail[var_name] = var_value

    def set_autoid(self, autoid):
        self.autoid = autoid
        # 若autoid不为空，则查询对应的记录，并关联到表格中
        if self.autoid:
            self.flush_basedata(self.autoid)
        else:
            raise TypeError

    # 若传入了autoid，则刷新传入的数据
    def flush_basedata(self, autoid):
        item = self.check_item.get_checkitem(autoid)
        self.oridetail = model_to_dict(item)
        if item:
            self.seqid.setText(str(item.seqid))
            self.kind.setText(item.kind)
            self.itemname.setText(item.itemname)
            self.referencevalue.setText(item.referencevalue)
            self.restype.setCurrentIndex(item.restype)
            self.putintype .setCurrentIndex(item.putintype)
        else:
            raise KeyError

    def signal_connect_slit(self):
        object_tuple = (
            'seqid', 'kind', 'itemname', 'referencevalue', 'restype',
            'putintype')

        for item in object_tuple:

            try:
                if item == 'referencevalue':
                    raise TypeError
                getattr(self, item).textChanged.connect(self.on_textChanged)
            except AttributeError:
                getattr(self, item).currentIndexChanged.connect(
                    self.on_indexChanged)
            except TypeError:
                getattr(self, item).textChanged.connect(
                    self.on_textChanged)
        self.acceptbutton.clicked.connect(self.on_accept_clicked)
        self.cancelbutton.clicked.connect(self.on_cancel_clicked)

    def on_text2Changed(self):
        obj = self.sender()
    # 修改内容时触发
    def on_textChanged(self, p_str=None):
        obj = self.sender()
        obj_name = self.sender().objectName()
        if p_str == None:
            p_str = obj.toPlainText()
        try:
            if p_str != str(self.oridetail[obj_name]):
                self.detail[obj_name] = p_str
            else:
                try:
                    del self.detail[obj_name]
                except KeyError:
                    pass
        except KeyError:
            self.detail[obj_name] = p_str

    def on_indexChanged(self, p_int):
        obj_name = self.sender().objectName()
        try:
            if p_int != self.oridetail[obj_name]:
                self.detail[obj_name] = p_int
            else:
                try:
                    del self.data[obj_name]
                except KeyError:
                    pass
        except KeyError:
            self.detail[obj_name] = p_int

    # 修改种类时触发
    def on_no_textChanged(self, p_str):
        try:
            if p_str != self.detail['seqid']:
                self.detail['seqid'] = p_str
            else:
                try:
                    del self.data['seqid']
                except KeyError:
                    pass
        except KeyError:
            self.detail['seqid'] = p_str

    # 确认
    def on_accept_clicked(self):
        # 有修改过数据
        try:
            # autoid不为空，则为修改记录
            # 否则为插入记录
            if self.autoid:
                res = self.check_item.update_check_item(self.autoid,
                                                        **self.detail)
                if res == 1:
                    self.flush_signal.emit()
                    self.accept()
            else:
                print(self.detail)
                res = self.check_item.update_check_item(**self.detail)
                if res.autoid > 0:
                    self.flush_signal.emit()
                    self.accept()
        except Exception as e:
            SaveExcept(e, "保存检验项目出错", self.detail)


    # 取消
    def on_cancel_clicked(self):
        self.close()
