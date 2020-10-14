from PyQt5 import QtCore, QtGui, QtWidgets

from stuff.controllers.stuffdetail import StuffDetail

from stuff.models.stuffmodel import StuffModel

from stuff.views.stuffdictionary import Ui_Form

# 物料字典几个按键对应的值
STUFFTYPE = ("主材料", "前处理", "辅材料", "内包材", "外包材")


class StuffDictionaryModule(QtWidgets.QDialog, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 数据库操作类
        self.sd = StuffModel()
        self.detail = ''
        self.all_stuff = []

        # 当前的物料种类，默认为“全部按键”
        self.current_stuff_kind_button = self.ALLButton
        self.ALLButton.clicked.connect(self.on_stufftypeButton_clicked)
        self.ZCButton.clicked.connect(self.on_stufftypeButton_clicked)
        self.QCLButton.clicked.connect(self.on_stufftypeButton_clicked)
        self.FCButton.clicked.connect(self.on_stufftypeButton_clicked)
        self.NBButton.clicked.connect(self.on_stufftypeButton_clicked)
        self.WBButton.clicked.connect(self.on_stufftypeButton_clicked)
        # 显示物料列表
        self.show_stuff_list()
        # 添加右键菜单功能
        self.__add_menu()

    # 添加菜单功能
    def __add_menu(self):
        self.stufflist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.stufflist.customContextMenuRequested.connect(self.generate_menu)

    def generate_menu(self, pos):
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
        #model = StuffSupplyer(self)
        #set_stuff_supplyer.set_variable('sdid', self.autoid)
        # 增加
        if action == button1:
            self.on_addButton_clicked()
        # 修改
        elif action == button2:
            self.on_recordButton_clicked()
        # 删除
        elif action == button3:
            self.on_deleteButton_clicked()
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
                        print(tree_item)
                        if tree_item is None:
                            raise AttributeError
                        detail = dict()
                        detail["supid"] = tree_item.text(1)
                        detail["supname"] = tree_item.text(2)
                        detail["producer"] = tree_item.text(3)
                        detail["sdid_id"] = self.autoid
                        #set_stuff_supplyer.update_stuff_supplyer_item(None,
                        #                                              **detail)
                        count += 1
                    self.on_tab_tabBarClicked(self.tab.currentIndex())
            except Exception as e:
                print("供应商黏贴出错", repr(e))
        else:
            pass

    # 显示物料列表内容
    # stufftype默认为-1，即为全部物料
    def show_stuff_list(self):
        if self.current_stuff_kind_button.text() in STUFFTYPE:
            stufftype = STUFFTYPE.index(self.current_stuff_kind_button.text())
        else:
            stufftype = -1
        self.stufflist.clear()
        self.all_stuff = self.sd.get_all_stuff(stufftype)
        if self.all_stuff:
            self.countlabel.setText("共%s条记录" % len(self.all_stuff))
            for item in self.all_stuff:
                stufflist = QtWidgets.QTreeWidgetItem(self.stufflist)
                stufflist.setText(0, str(item["autoid"]))
                stufflist.setText(1, item["stuffid"])
                stufflist.setText(2, item["stuffname"])
                stufflist.setText(3, item["kind"])
                stufflist.setText(4, item["spec"])
                stufflist.setText(5, item["package"])
                stufflist.setText(6, item["allowno"])
                stufflist.setText(7, item["storage"])
            # 隐藏第一列的id
            self.stufflist.hideColumn(0)
            for i in range(1, 8):
                self.stufflist.resizeColumnToContents(i)
                if self.stufflist.columnWidth(i) > 200:
                    self.stufflist.setColumnWidth(i, 200)
                elif self.stufflist.columnWidth(i) < 120:
                    self.stufflist.setColumnWidth(i, 120)
        else:
            self.countlabel.setText("共0条记录")
    # 刷新功能
    @QtCore.pyqtSlot()
    def on_refreshButton_clicked(self):
        self.show_stuff_list()

    # 新建功能
    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        detail = StuffDetail(self)
        detail.flush_signal.connect(self.show_stuff_list)
        detail.show()

    # 删除功能
    @QtCore.pyqtSlot()
    def on_deleteButton_clicked(self):
        items = self.stufflist.selectedItems()
        autoid_list = []
        for item in items:
            autoid_list.append(item.text(0))
        res = self.sd.delete_stuff(None, *autoid_list)
        if res[0] >= 1:
            self.show_stuff_list()

    # 打开记录详情
    @QtCore.pyqtSlot()
    def on_recordButton_clicked(self):
        if self.stufflist.currentItem():
            self.on_stufflist_itemDoubleClicked(self.stufflist.currentItem(), 0)

    # 物料列表双击功能
    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def on_stufflist_itemDoubleClicked(self, QTreeWidgetItem, p_int):
        autoid = int(QTreeWidgetItem.text(0))
        # 物料详细列表
        detail = StuffDetail(autoid, self)
        detail.flush_signal.connect(self.show_stuff_list)
        # 修改了物料记录，刷新列表
        detail.show()

    # 物料类型的选择，6个按键共用一个方法
    @QtCore.pyqtSlot()
    def on_stufftypeButton_clicked(self):
        button_name = self.sender()
        if self.current_stuff_kind_button == button_name:
            pass
        else:
            self.current_stuff_kind_button.setEnabled(True)
            self.current_stuff_kind_button = button_name
            button_name.setEnabled(False)
            self.show_stuff_list()