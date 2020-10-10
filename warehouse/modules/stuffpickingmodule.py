from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot, QTimer

from warehouse.controllers.warehousecontroller import WarehouseController

from warehouse.modules.drawstuffmodule import DrawstuffModule

from warehouse.views.stuffpicking import Ui_Form

from lib.utils.saveexcept import SaveExcept
from lib.utils.messagebox import MessageBox


# 物料字典几个按键对应的值
STUFFTYPE = ("未提交", "已提交", "已领取")
PAPERTYPE = ("原辅材料领料单", "内包材领料单", "外包材领料单")


class StuffpickingModule(QDialog, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.current_stuff_kind_button = self.pushButton_apply
        # 数据库操作类
        self.WC = WarehouseController()
        self.pushButton_apply.clicked.connect(self.on_statusButton_clicked)
        self.pushButton_finish.clicked.connect(self.on_statusButton_clicked)

        # 显示物料列表
        self.show_stuffdrawpaper_list()

    # 显示领料单列表内容
    # stufftype默认为已提交的领料单
    def show_stuffdrawpaper_list(self):
        self.stuffdrawpaperlist.clear()
        if self.current_stuff_kind_button.text() in STUFFTYPE:
            paperstatus = STUFFTYPE.index(self.current_stuff_kind_button.text())
            self.stuffdrawpaper = self.WC.get_stuffdrawpaper(status=paperstatus)
            if len(self.stuffdrawpaper):
                self.countlabel.setText("共%s条记录" % len(self.stuffdrawpaper))
                for item in self.stuffdrawpaper:
                    try:
                        stufflist = QTreeWidgetItem(
                            self.stuffdrawpaperlist)
                        stufflist.setText(0, str(item.autoid))
                        stufflist.setText(1, str(item.ppid))
                        stufflist.setText(2, PAPERTYPE[item.papertype])
                        stufflist.setText(3,
                                          item.chargerid + ' ' + item.chargername)
                        stufflist.setText(4, str(item.applytime))
                        stufflist.setText(5,
                                          item.providerid + ' ' + item.providername)
                        stufflist.setText(6, str(item.drawtime))
                        stufflist.setText(7, item.prod)
                        stufflist.setText(8, item.spec)
                        stufflist.setText(9, item.package)
                        stufflist.setText(10, item.batchno)
                    except:
                        pass
                # 隐藏第一列的id
                self.stuffdrawpaperlist.hideColumn(0)
                self.stuffdrawpaperlist.hideColumn(1)
                for i in range(2, 9):
                    self.stuffdrawpaperlist.resizeColumnToContents(i)
                    if self.stuffdrawpaperlist.columnWidth(i) > 200:
                        self.stuffdrawpaperlist.setColumnWidth(i, 200)
            else:
                self.countlabel.setText("共0条记录")

    # 刷新功能
    @pyqtSlot()
    def on_pushButton_refresh_clicked(self):
        self.show_stuffdrawpaper_list()

    # 打开记录详情
    @pyqtSlot()
    def on_recordButton_clicked(self):
        if self.stufflist.currentItem():
            self.on_stufflist_itemDoubleClicked(self.stufflist.currentItem(), 0)

    # 物料列表双击功能
    @pyqtSlot(QTreeWidgetItem, int)
    def on_stuffdrawpaperlist_itemDoubleClicked(self, QTreeWidgetItem, p_int):
        try:
            sdpid = QTreeWidgetItem.text(0)
            ppid = QTreeWidgetItem.text(1)
            kind = PAPERTYPE.index(QTreeWidgetItem.text(2))
            # 物料详细列表
            detail = DrawstuffModule(ppid, sdpid, kind, self)
            detail.accepted.connect(self.show_stuffdrawpaper_list)
            detail.finished.connect(self.not_find_proddetail)
            # 修改了物料记录，刷新列表
            detail.showMaximized()
        except ValueError:
            SaveExcept(ValueError, "打开领料单时出错", (QTreeWidgetItem.text(1), QTreeWidgetItem.text(2)))

    def not_find_proddetail(self, p_int):
        if p_int == 6:
            msg = MessageBox(parent=self, title="错误", text="领料单异常!",
                         informative="没有找到对应的产品信息!")
            msg.show()
            timer = QTimer(self)
            timer.start(1000)
            timer.timeout.connect(msg.close)

    @pyqtSlot()
    def on_statusButton_clicked(self):
        button_name = self.sender()
        if self.current_stuff_kind_button == button_name:
            pass
        else:
            self.current_stuff_kind_button.setEnabled(True)
            self.current_stuff_kind_button = button_name
            button_name.setEnabled(False)
            self.show_stuffdrawpaper_list()
