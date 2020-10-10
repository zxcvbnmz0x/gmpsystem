# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from lib.utils.inputcode import Inputcode
from lib.utils.saveexcept import SaveExcept

from labrecord.controllers.checkitem import CheckItem
from labrecord.controllers.setcheckitem import SetCheckItem
from imageslib.controllers.image import Image
from supplyer.controllers.stuffsupplyer import StuffSupplyer
from product.controllers.productcontroller import ProductController
from productline.controllers.setproductline import SetProductLine
from product.views.productdetail import Ui_Dialog

# 检验结果的类型和入库类型
RESTYPE = ("文本", "数据")
PUTINTYPE = ("无", "含量", "水分", "效价", "相对密度", "杂质")


class ProductDetailModule(QtWidgets.QDialog, Ui_Dialog):
    check_item = CheckItem()
    flush_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None, autoid=None):
        super().__init__(parent)
        self.setupUi(self)
        self.autoid = 0
        # 添加右键菜单功能
        self.__add_menu()

        self.product = ProductController()
        medkind_list = self.product.get_all_medkind()
        self.set_medkind_list(medkind_list)
        self.oridetail = dict()
        self.new_detail = dict()
        self.prodcheckitem.itemDoubleClicked.connect(
            self.on_checkitem_itemDoubleClicked)
        self.precheckitem.itemDoubleClicked.connect(
            self.on_checkitem_itemDoubleClicked)
        self.samplecheckitem.itemDoubleClicked.connect(
            self.on_checkitem_itemDoubleClicked)
        self.prodname.textChanged.connect(self.on_QLineEdit_textChanged)
        self.commonname.textChanged.connect(self.on_QLineEdit_textChanged)
        self.allowno.textChanged.connect(self.on_QLineEdit_textChanged)
        self.spec.textChanged.connect(self.on_QLineEdit_textChanged)
        self.medkind.currentTextChanged.connect(self.on_QLineEdit_textChanged)
        self.checkunit.currentIndexChanged.connect(
            self.on_QComboBox_currentIndexChanged)
        self.expireddates.textChanged.connect(self.on_QLineEdit_textChanged)
        self.storage.textChanged.connect(self.on_QLineEdit_textChanged)

    def set_medkind_list(self, p_list: list):
        for item in p_list:
            self.medkind.addItem(item)

    def on_tab_tabBarClicked(self, p_int):
        tab_name = self.tab.tabText(p_int)
        # 原料检验项目
        if tab_name in ("中间产品检验项目", "成品检验项目", "留样检验项目"):
            try:
                # 原料检验项目itemtype=0
                if tab_name == "中间产品检验项目":
                    items = self.check_item.get_checkitems(self.prodid.text(),
                                                           2)
                    widget = self.precheckitem
                # 前处理检验项目itemtype=5
                elif tab_name == "成品检验项目":
                    items = self.check_item.get_checkitems(self.prodid.text(),
                                                           1)
                    widget = self.prodcheckitem
                elif tab_name == "留样检验项目":
                    items = self.check_item.get_checkitems(self.prodid.text(),
                                                           6)
                    widget = self.samplecheckitem
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
        elif tab_name == "产品配方":
            pass
        # 产品标签图
        elif tab_name == "产品标签图":
            self.labellist.clear()
            if self.labelvaildButton.isEnabled():
                flag = 1
            else:
                flag = 0
            product_labels = self.product.get_label(
                prodid=self.oridetail['prodid'], flag=flag)
            if product_labels:
                for item in product_labels:
                    treeitem = QtWidgets.QTreeWidgetItem(self.labellist)
                    treeitem.setText(0, str(item.autoid))
                    treeitem.setText(1, str(item.imagename))
                    treeitem.setText(2,
                                     item.modifierid + ' ' + item.modifiername)
                    treeitem.setText(3, str(item.modifytime))
                    treeitem.setText(4, str(item.imgid))
            self.labellist.hideColumn(0)
            self.labellist.hideColumn(4)
            self.labellist.resizeColumnToContents(1)
            self.labellist.resizeColumnToContents(2)
            self.labellist.resizeColumnToContents(3)
        else:
            pass

    # 中间产品/成品/留样检验项目，双击打开详细信息
    def on_checkitem_itemDoubleClicked(self, p_int):
        try:
            widget = self.sender()
            set_check_item = SetCheckItem(self, widget.currentItem().text(0))
            set_check_item.flush_signal.connect(
                lambda: self.on_tab_tabBarClicked(self.tab.currentIndex()))
            set_check_item.show()
        except AttributeError:
            pass
        except Exception as e:
            SaveExcept(e, "双击中间产品/成品/留样检验项目时报错")

    # 产品标签图双击功能
    def on_labellist_itemDoubleClicked(self, p_int):
        widget = self.sender()
        autoid = widget.currentItem().text(4)
        image = Image()
        image_detail = image.get_image(autoid)
        img = QtGui.QImage.fromData(image_detail[0].img)
        self.productimage.setPixmap(QtGui.QPixmap.fromImage(img))

    # 添加菜单功能
    def __add_menu(self):
        self.prodcheckitem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.labellist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.prodcheckitem.customContextMenuRequested.connect(
            self.generate_check_menu)
        self.labellist.customContextMenuRequested.connect(
            self.generate_label_menu)
        self.formula.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.precheckitem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.formula.customContextMenuRequested.connect(self.generate_menu)
        self.precheckitem.customContextMenuRequested.connect(
            self.generate_check_menu)
        self.samplecheckitem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.samplecheckitem.customContextMenuRequested.connect(
            self.generate_check_menu)

    # 产品标签图的右键菜单功能
    def generate_label_menu(self, pos):
        # 返回调用者的对象
        sender_widget = self.sender()
        menu = QtWidgets.QMenu()
        button1 = menu.addAction("增加")
        button2 = menu.addAction("修改")
        button3 = menu.addAction("删除")
        button4 = menu.addAction("设置为生效/失效")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        set_stuff_supplyer = StuffSupplyer(self)
        set_stuff_supplyer.set_variable('sdid', self.autoid)
        # 增加
        if action == button1:
            img_names, img_type = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                                         "打开图片",
                                                                         os.path.expanduser(
                                                                             "~") + "\Desktop",
                                                                         "*.jpg;;*.png;;All Files(*)")

            for item in img_names:
                imagename_no_ext = item.split("/")[-1]
                image_ext = item.split(".")[1]
                if image_ext.lower() not in ("jpg", "png", "bmp", "gif"):
                    continue
                fp = open(item, 'rb') 
                with fp:
                    image_byte = fp.read()
                    fp.close()
                imagedetail = dict()
                imagedetail['img'] = image_byte
                imagedetail['ext'] = image_ext
                res = self.product.save_productlabel(prodid=self.prodid.text(),
                                                     imagename=imagename_no_ext,
                                                     imagedetail=imagedetail)
                try:
                    if res[0] > 1:
                        self.on_tab_tabBarClicked(self.tab.currentIndex())
                except TypeError:
                    pass
        # 修改
        elif action == button2:
            label_no = self.labellist.currentItem().text(0)
            img_name, img_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                       "打开图片",
                                                                       os.path.expanduser(
                                                                           "~") + "\Desktop",
                                                                       "*.jpg;;*.png;;All Files(*)")
            imagename_no_ext = img_name.split("/")[-1]
            image_ext = img_name.split(".")[1]
            if image_ext.lower() in ("jpg", "png", "bmp", "gif"):
                fp = open(img_name, 'rb')
                with fp:
                    image_byte = fp.read()
                    fp.close()
                imagedetail = dict()
                imagedetail['img'] = image_byte
                imagedetail['ext'] = image_ext
                res = self.product.save_productlabel(autoid=label_no, prodid=self.prodid.text(),
                                                     imagename=imagename_no_ext,
                                                     imagedetail=imagedetail)
                try:
                    if res[0] > 1:
                        self.on_tab_tabBarClicked(self.tab.currentIndex())
                        new_image = QtGui.QImage.fromData(image_byte)
                        self.productimage.setPixmap(
                            QtGui.QPixmap.fromImage(new_image))
                except TypeError:
                    pass
        # 删除
        elif action == button3:
            select_item = sender_widget.selectedItems()
            item_autoid = []
            for item in select_item:
                item_autoid.append(item.text(0))
            res = self.product.delete_productlabel(item_autoid)
            try:
                if res[0] >= 1:
                    self.on_tab_tabBarClicked(self.tab.currentIndex())
            except TypeError:
                pass
        # 切换生效和失效的状态
        elif action == button4:
            product_label = self.labellist.currentItem().text(0)
            # 生效按键允许点击，则当前状态为失效
            if self.labelvaildButton.isEnabled():
                flag = 0
            else:
                flag = 1
            self.product.update_productlabel(autoid=product_label, flag=flag)
            self.on_tab_tabBarClicked(self.tab.currentIndex())
        else:
            pass

    # 检验项目的右键菜单功能
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
        set_check_item.set_variable('prodid', self.prodid.text())
        # 增加
        if action == button1:
            if sender_widget.objectName() == "precheckitem":
                set_check_item.set_variable('itemtype', 2)
            elif sender_widget.objectName() == "prodcheckitem":
                set_check_item.set_variable('itemtype', 1)
            elif sender_widget.objectName() == "samplecheckitem":
                set_check_item.set_variable('itemtype', 6)
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
                        detail["prodid"] = self.prodid.text()
                        if self.tab.tabText(
                                self.tab.currentIndex()) == "中间产品检验项目":
                            detail["itemtype"] = 2
                        elif self.tab.tabText(
                                self.tab.currentIndex()) == "成品检验项目":
                            detail["itemtype"] = 1
                        elif self.tab.tabText(
                                self.tab.currentIndex()) == "留样检验项目":
                            detail["itemtype"] = 6
                        check_item = CheckItem()
                        check_item.update_check_item(None, **detail)
                        count += 1
            except Exception as e:
                print("检验项目黏贴出错", repr(e))
        else:
            pass

    # 产品标签图生效按键点击
    @QtCore.pyqtSlot()
    def on_labelvaildButton_clicked(self):
        self.labelvaildButton.setEnabled(False)
        self.labelinvaildButton.setEnabled(True)
        self.on_tab_tabBarClicked(self.tab.currentIndex())

    # 产品标签图失效按键点击
    @QtCore.pyqtSlot()
    def on_labelinvaildButton_clicked(self):
        self.labelvaildButton.setEnabled(True)
        self.labelinvaildButton.setEnabled(False)
        self.on_tab_tabBarClicked(self.tab.currentIndex())

    # 修改编号时触发
    @QtCore.pyqtSlot(str)
    def on_prodid_textChanged(self, p_str):
        objname = self.sender().objectName()
        try:
            if p_str != self.oridetail[objname]:
                self.new_detail[objname] = p_str
            else:
                try:
                    del self.new_detail[objname]
                except KeyError:
                    pass
        except KeyError:
            self.new_detail[objname] = p_str

    # 修改名称时触发
    @QtCore.pyqtSlot(str)
    def on_prodname_textChanged(self, p_str):
        objname = self.sender().objectName()
        try:
            if p_str != self.oridetail[objname]:
                self.new_detail[objname] = p_str
                self.inputcode.setText(Inputcode.make_inputcode(p_str))
                self.kind.setText(p_str)
            else:
                try:
                    del self.new_detail[objname]
                except KeyError:
                    pass
        except KeyError:
            self.new_detail[objname] = p_str

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

    # 修改行元素时触发
    @QtCore.pyqtSlot(str)
    def on_QLineEdit_textChanged(self, p_str):
        objname = self.sender().objectName()
        try:
            if p_str != self.oridetail[objname]:
                self.new_detail[objname] = p_str
            else:
                try:
                    del self.new_detail[objname]
                except KeyError:
                    pass
        except KeyError:
            self.new_detail[objname] = p_str

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

    # 修改下拉框时触发
    @QtCore.pyqtSlot(int)
    def on_QComboBox_currentIndexChanged(self, p_int):
        objname = self.sender().objectName()
        try:
            if p_int != int(self.oridetail[objname]):
                self.new_detail[objname] = p_int
            else:
                try:
                    del self.new_detail[objname]
                except KeyError:
                    pass
        except KeyError:
            self.new_detail[objname] = p_int

    # 修改生产线和车间时触发
    @QtCore.pyqtSlot()
    def on_workshop_clicked(self):
        setpl = SetProductLine(parent=self, pltype=0)
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
            self.new_detail['plid'] = linedetail['autoid']

    # 修改退货线和车间时触发
    @QtCore.pyqtSlot()
    def on_bworkshop_clicked(self):
        setpl = SetProductLine(parent=self, pltype=2)
        setpl.select_line_signal.connect(self.setwpproductline)
        setpl.show()

    def setwpproductline(self, linedetail: dict):
        try:
            if linedetail['autoid'] != self.oridetail['wplid']:
                self.new_detail['wplid'] = linedetail['autoid']
                self.bworkshop.setText(linedetail['deptname'])
                self.bproductionline.setText(linedetail['linename'])
            else:
                try:
                    del self.new_detail['wplid']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['wplid'] = linedetail['autoid']

    # 确认
    @QtCore.pyqtSlot()
    def on_acceptButton_clicked(self):
        # 有修改过数据
        if self.new_detail:
            try:
                # autoid不为空，则为修改记录
                # 否则为插入记录
                if self.autoid:
                    res = self.product.update_product(self.autoid,
                                                      **self.new_detail)
                    if res == 1:
                        self.flush_signal.emit()
                        self.accept()
                else:
                    res = self.product.update_product(**self.new_detail)
                    if res.autoid > 0:
                        self.flush_signal.emit()
                        self.accept()
            except Exception as e:
                print(repr(e))

    # 取消
    @QtCore.pyqtSlot()
    def on_cancelButton_clicked(self):
        self.close()
