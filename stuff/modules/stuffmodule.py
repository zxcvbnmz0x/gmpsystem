# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from lib.utils.inputcode import Inputcode

from labrecord.controllers.checkitem import CheckItem
from labrecord.controllers.setcheckitem import SetCheckItem
from supplyer.controllers.supplyercontroller import SupplyerController
from supplyer.controllers.stuffsupplyer import StuffSupplyer
from stuff.controllers.setstuff import setStuff
from productline.controllers.setproductline import SetProductLine

from stuff.views.stuffdetail import Ui_Dialog

# 检验结果的类型和入库类型
RESTYPE = ("文本", "数据")
PUTINTYPE = ("无", "含量", "水分", "效价", "相对密度", "杂质")


class StuffModule(QtWidgets.QDialog, Ui_Dialog):
    check_item = CheckItem()
    flush_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None, autoid=None):
        super().__init__(parent)
        self.setupUi(self)
        self.autoid = 0
        # 添加右键菜单功能
        self.__add_menu()
        self.oridetail = dict()
        self.new_detail = dict()

    def on_tab_tabBarClicked(self, p_int):
        tab_name = self.tab.tabText(p_int)
        # 原料检验项目
        if tab_name == "原料检验项目" or tab_name == "前处理检验项目":
            try:
                # 原料检验项目itemtype=0
                if tab_name == "原料检验项目":
                    items = self.check_item.get_checkitems(
                        False, stuffid=self.stuffid.text(), itemtype=0
                    )
                    widget = self.checkitem
                # 前处理检验项目itemtype=5
                else:
                    items = self.check_item.get_checkitems(
                        False, stuffid=self.prodid.text(), itemtype=5
                    )
                    widget = self.precheckitem
                widget.clear()
                for item in items:
                    checkitemlist = QtWidgets.QTreeWidgetItem(widget)
                    checkitemlist.setText(0, str(item.autoid))
                    checkitemlist.setText(1, str(item.seqid))
                    checkitemlist.setText(2, item.kind)
                    checkitemlist.setText(3, item.itemname)
                    checkitemlist.setText(4, item.referencevalue)
                    checkitemlist.setText(5, RESTYPE[item.restype])
                    checkitemlist.setText(6, PUTINTYPE[item.putintype])
                widget.hideColumn(0)
                widget.resizeColumnToContents(1)
                widget.resizeColumnToContents(2)
                widget.resizeColumnToContents(3)
                widget.resizeColumnToContents(5)
                widget.resizeColumnToContents(6)
                del items
            except Exception as e:
                print(repr(e))
        # 前处理配方
        elif tab_name == "前处理配方":
            pass
        # 供应商和生产厂家
        elif tab_name == "供应商和生产厂家":
            self.pdandsp.clear()
            kwargs = {"sdid": self.autoid}
            self.SM = SupplyerController()
            supplyers = self.SM.get_supply(**kwargs)
            if supplyers:
                for item in supplyers:
                    treeitem = QtWidgets.QTreeWidgetItem(self.pdandsp)
                    treeitem.setText(0, str(item.autoid))
                    treeitem.setText(1, str(item.spid.supid))
                    treeitem.setText(2, item.spid.supname)
                    treeitem.setText(3, item.producer)
            self.pdandsp.hideColumn(0)
            self.pdandsp.resizeColumnToContents(1)
            self.pdandsp.resizeColumnToContents(2)
            self.pdandsp.resizeColumnToContents(3)
        else:
            pass

    def on_precheckitem_itemDoubleClicked(self, p_int):
        self.on_checkitem_itemDoubleClicked(p_int)

    # 原料检验项目，双击打开详细信息
    def on_checkitem_itemDoubleClicked(self, p_int):
        widget = self.sender()
        set_check_item = SetCheckItem(self, widget.currentItem().text(0))
        set_check_item.flush_signal.connect(
            lambda: self.on_tab_tabBarClicked(self.tab.currentIndex()))
        set_check_item.show()

    def on_pdandsp_itemDoubleClicked(self, p_int):
        widget = self.sender()
        autoid = widget.currentItem().text(0)
        sfsp = StuffSupplyer(self)
        sfsp.set_variable("autoid", autoid)
        sfsp.set_stuff_supplyer()
        sfsp.flush_signal.connect(
            lambda: self.on_tab_tabBarClicked(self.tab.currentIndex()))
        sfsp.show()

    # 添加菜单功能
    def __add_menu(self):
        self.checkitem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pdandsp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.checkitem.customContextMenuRequested.connect(
            self.generate_check_menu)
        self.pdandsp.customContextMenuRequested.connect(self.generate_pdsp_menu)
        self.formula.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.precheckitem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.formula.customContextMenuRequested.connect(self.generate_menu)
        self.precheckitem.customContextMenuRequested.connect(
            self.generate_check_menu)

    # 物料供应商和生产厂家的右键菜单功能
    def generate_pdsp_menu(self, pos):
        # 返回调用者的对象
        sender_widget = self.sender()
        menu = QtWidgets.QMenu()
        button1 = menu.addAction("增加")
        button2 = menu.addAction("修改")
        button3 = menu.addAction("删除")
        button4 = menu.addAction("复制")
        button5 = menu.addAction("黏贴")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        set_stuff_supplyer = StuffSupplyer(self)
        set_stuff_supplyer.set_variable('sdid', self.autoid)
        # 增加
        if action == button1:

            set_stuff_supplyer.flush_signal.connect(
                lambda: self.on_tab_tabBarClicked(self.tab.currentIndex()))
            set_stuff_supplyer.show()
        # 修改
        elif action == button2:
            try:
                self.on_pdandsp_itemDoubleClicked(sender_widget.currentIndex())
            except Exception as e:
                print(repr(e))
        # 删除
        elif action == button3:
            select_item = sender_widget.selectedItems()
            item_autoid = []
            for item in select_item:
                item_autoid.append(item.text(0))
            res = set_stuff_supplyer.delete_stuff_supplyer(item_autoid)
            if res[0] >= 1:
                self.on_tab_tabBarClicked(self.tab.currentIndex())
        # 复制
        elif action == button4:
            clipboard = QtWidgets.QApplication.clipboard()
            # 当前选择的项目
            items = sender_widget.selectedItems()
            # 把项目转为Mime对象
            select_item = sender_widget.mimeData(items)
            # 把Mime对象存入剪切板
            clipboard.setMimeData(select_item)
        # 黏贴
        elif action == button5:
            try:
                clipboard = QtWidgets.QApplication.clipboard()
                # 获取剪切板里的内容
                data = clipboard.mimeData()
                # 获取当前行数,加1即为新的行号
                count = sender_widget.topLevelItemCount()
                # dropMineData，把Mime对象转回Qtreeitem
                # 第一个参数：要添加到的父节点
                # 第二个参数：行号
                # 第三个参数：Mime数据
                res = sender_widget.dropMimeData(
                    sender_widget.invisibleRootItem(), count + 1, data,
                    QtCore.Qt.CopyAction)
                # 黏贴完成后的行数
                finnal_index = sender_widget.topLevelItemCount()
                if res:
                    # 把黏贴的数据加入数据库中
                    # 数据从count到finnal_index即为黏贴的行号
                    while count < finnal_index:
                        tree_item = sender_widget.topLevelItem(count)
                        if tree_item is None:
                            raise AttributeError
                        detail = dict()
                        detail["supid"] = tree_item.text(1)
                        detail["supname"] = tree_item.text(2)
                        detail["producer"] = tree_item.text(3)
                        detail["sdid_id"] = self.autoid
                        set_stuff_supplyer.update_stuff_supplyer_item(None,
                                                                      **detail)
                        count += 1
                    self.on_tab_tabBarClicked(self.tab.currentIndex())
            except Exception as e:
                print("供应商黏贴出错", repr(e))
        else:
            pass

    # 物料检验项目和前处理检验项目的右键菜单功能
    def generate_check_menu(self, pos):
        # 返回调用者的对象
        sender_widget = self.sender()
        menu = QtWidgets.QMenu()
        button1 = menu.addAction("增加")
        button2 = menu.addAction("修改")
        button3 = menu.addAction("删除")
        button4 = menu.addAction("复制")
        button5 = menu.addAction("黏贴")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        set_check_item = SetCheckItem(self)
        set_check_item.set_variable('stuffid', self.stuffid.text())
        # 增加
        if action == button1:

            if sender_widget.objectName() == "checkitem":
                set_check_item.set_variable('itemtype', 0)
            else:
                set_check_item.set_variable('itemtype', 5)
            set_check_item.flush_signal.connect(
                lambda: self.on_tab_tabBarClicked(self.tab.currentIndex()))
            set_check_item.show()
        # 修改
        elif action == button2:
            self.on_checkitem_itemDoubleClicked(sender_widget.currentIndex())
        # 删除
        elif action == button3:
            checkitems = CheckItem()
            select_item = sender_widget.selectedItems()
            checkitem_autoid = []
            for item in select_item:
                checkitem_autoid.append(item.text(0))
            res = checkitems.delete_check_item(checkitem_autoid)
            if res[0] >= 1:
                self.on_tab_tabBarClicked(self.tab.currentIndex())
        # 复制
        elif action == button4:
            clipboard = QtWidgets.QApplication.clipboard()
            items = sender_widget.selectedItems()
            select_item = sender_widget.mimeData(items)
            clipboard.setMimeData(select_item)
        # 黏贴
        elif action == button5:
            try:
                clipboard = QtWidgets.QApplication.clipboard()
                data = clipboard.mimeData()
                # 获取当前行数,加1即为新的行号
                count = sender_widget.topLevelItemCount()
                res = sender_widget.dropMimeData(
                    sender_widget.invisibleRootItem(), count + 1, data,
                    QtCore.Qt.CopyAction)
                finnal_index = sender_widget.topLevelItemCount()
                if res:
                    while count < finnal_index:
                        tree_item = sender_widget.topLevelItem(count)
                        if tree_item is None:
                            raise AttributeError
                        detail = dict()
                        detail["seqid"] = tree_item.text(1)
                        detail["kind"] = tree_item.text(2)
                        detail["itemname"] = tree_item.text(3)
                        detail["referencevalue"] = tree_item.text(4)
                        detail["restype"] = RESTYPE.index(tree_item.text(5))
                        detail["putintype"] = PUTINTYPE.index(tree_item.text(6))
                        detail["stuffid"] = self.stuffid.text()
                        if self.stufftype.currentIndex() <= 3:
                            detail["itemtype"] = 0
                        else:
                            detail["itemtype"] = 5
                        check_item = CheckItem()
                        check_item.update_check_item(None, **detail)
                        count += 1
            except Exception as e:
                print("检验项目黏贴出错", repr(e))
        else:
            pass

    # 修改种类时触发
    @QtCore.pyqtSlot(int)
    def on_stufftype_currentIndexChanged(self, p_int):
        try:
            if p_int != int(self.oridetail['stufftype']):
                self.new_detail['stufftype'] = p_int
            else:
                try:
                    del self.new_detail['stufftype']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['stufftype'] = p_int

    # 修改编号时触发
    @QtCore.pyqtSlot(str)
    def on_stuffid_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['stuffid']:
                self.new_detail['stuffid'] = p_str
            else:
                try:
                    del self.new_detail['stuffid']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['stuffid'] = p_str

    # 修改名称时触发
    @QtCore.pyqtSlot(str)
    def on_stuffname_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['stuffname']:
                self.new_detail['stuffname'] = p_str
                self.inputcode.setText(Inputcode.make_inputcode(p_str))
                self.kind.setText(p_str)
            else:
                try:
                    del self.new_detail['stuffname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['stuffname'] = p_str

    # 修改外部编码时触发
    @QtCore.pyqtSlot(str)
    def on_externalno_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['externalno']:
                self.new_detail['externalno'] = p_str
            else:
                try:
                    del self.new_detail['externalno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['externalno'] = p_str

    # 修改种类时触发
    @QtCore.pyqtSlot(str)
    def on_kind_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['kind']:
                self.new_detail['kind'] = p_str
            else:
                try:
                    del self.new_detail['kind']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['kind'] = p_str

    # 修改批准文号时触发
    @QtCore.pyqtSlot(str)
    def on_allowno_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['allowno']:
                self.new_detail['allowno'] = p_str
            else:
                try:
                    del self.new_detail['allowno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['allowno'] = p_str

    # 修改输入码时触发
    @QtCore.pyqtSlot(str)
    def on_inputcode_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['inputcode']:
                self.new_detail['inputcode'] = p_str
            else:
                try:
                    del self.new_detail['inputcode']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['inputcode'] = p_str

    # 修改含量规格时触发
    @QtCore.pyqtSlot(str)
    def on_spec_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['spec']:
                self.new_detail['spec'] = p_str
            else:
                try:
                    del self.new_detail['spec']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['spec'] = p_str

    # 修改包装级别时触发
    @QtCore.pyqtSlot(int)
    def on_packageLv_currentIndexChanged(self, p_int):
        try:
            if p_int != int(self.oridetail['packagelv']):
                self.new_detail['packagelv'] = p_int
            else:
                try:
                    del self.new_detail['packagelv']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['packagelv'] = p_int

    # 修改包装情况时触发
    @QtCore.pyqtSlot(str)
    def on_package_2_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['package']:
                self.new_detail['package'] = p_str
            else:
                try:
                    del self.new_detail['package']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['package'] = p_str

    # 修改入库单位时触发
    @QtCore.pyqtSlot(int)
    def on_purchasingunit_currentIndexChanged(self, p_int):
        try:
            if p_int != int(self.oridetail['unit']):
                self.new_detail['unit'] = p_int
            else:
                try:
                    del self.new_detail['unit']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['unit'] = p_int

    # 修改取样单位时触发
    @QtCore.pyqtSlot(int)
    def on_checkunit_currentIndexChanged(self, p_int):
        try:
            if p_int != int(self.oridetail['checkunit']):
                self.new_detail['checkunit'] = p_int
            else:
                try:
                    del self.new_detail['checkunit']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['stufftype'] = p_int

    # 修改库存上限时触发
    @QtCore.pyqtSlot(str)
    def on_upperlimit_textChanged(self, p_int):
        try:
            if p_int != self.oridetail['upperlimit']:
                self.new_detail['upperlimit'] = p_int
            else:
                try:
                    del self.new_detail['upperlimit']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['upperlimit'] = p_int

    # 修改库存下限时触发
    @QtCore.pyqtSlot(str)
    def on_lowlimit_textChanged(self, p_int):
        try:
            if p_int != self.oridetail['lowlimit']:
                self.new_detail['lowlimit'] = p_int
            else:
                try:
                    del self.new_detail['lowlimit']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['lowlimit'] = p_int

    # 修改复检天数时触发
    @QtCore.pyqtSlot(str)
    def on_recheck_textChanged(self, p_int):
        try:
            if p_int != self.oridetail['countercheckdays']:
                self.new_detail['countercheckdays'] = p_int
            else:
                try:
                    del self.new_detail['countercheckdays']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['countercheckdays'] = p_int

    # 修改有效期时触发
    @QtCore.pyqtSlot(str)
    def on_expired_textChanged(self, p_int):
        try:
            if p_int != self.oridetail['expireddays']:
                self.new_detail['expireddays'] = p_int
            else:
                try:
                    del self.new_detail['expireddays']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['expireddays'] = p_int

    # 修改效价单位时触发
    @QtCore.pyqtSlot(str)
    def on_ceffectunit_textChanged(self, p_int):
        try:
            if p_int != self.oridetail['cunit']:
                self.new_detail['cunit'] = p_int
            else:
                try:
                    del self.new_detail['cunit']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['cunit'] = p_int

    # 修改储存条件时触发
    @QtCore.pyqtSlot(str)
    def on_storage_textChanged(self, p_int):
        try:
            if p_int != self.oridetail['storage']:
                self.new_detail['storage'] = p_int
            else:
                try:
                    del self.new_detail['storage']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['storage'] = p_int

    # 修改生产线和车间时触发
    @QtCore.pyqtSlot()
    def on_workshop_clicked(self):
        setpl = SetProductLine(parent=self, pltype=1)
        setpl.select_line_signal.connect(self.setproductline)
        setpl.show()

    def setproductline(self, linedetail: dict):
        try:
            if linedetail['autoid'] != self.oridetail['plid']:
                self.new_detail['plid'] = linedetail['autoid']
                self.workshop.setText(linedetail['deptname'])
                self.productionline.setText(linedetail['linename'])
            else:
                try:
                    del self.new_detail['plid']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['plid'] = p_int

    # 确认
    @QtCore.pyqtSlot()
    def on_acceptButton_clicked(self):
        # 有修改过数据
        if self.new_detail:
            try:
                # autoid不为空，则为修改记录
                # 否则为插入记录
                setstuff = setStuff()
                if self.autoid:
                    res = setstuff.update_stuff(self.autoid, **self.new_detail)
                    if res == 1:
                        self.flush_signal.emit()
                        self.accept()
                else:
                    res = setstuff.update_stuff(**self.new_detail)
                    if res.autoid > 0:
                        self.flush_signal.emit()
                        self.accept()
            except Exception as e:
                print(repr(e))

    # 取消
    @QtCore.pyqtSlot()
    def on_cancelButton_clicked(self):
        self.close()
