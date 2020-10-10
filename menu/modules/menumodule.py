import sys
from PyQt5 import QtCore, QtWidgets


from db.models import Selfdefinedformat


from menu.views.mainmenu import Ui_MainWindow
from clerks.controllers.deptclerks import Clerks
from stuff.controllers.stuffdictionary import StuffDictionary

from product.controllers.productdictionary import ProductDictionary
from product.controllers.producingplan import Producingplan

from labrecord.modules.labsamplelistmodule import LabsamplelistModule
from labrecord.modules.labreportlistmodule import LabreportlistModule

from warehouse.modules.stuffpickingmodule import StuffpickingModule
from warehouse.modules.oddmentputinnotemodule import OddmentputinnoteModule
from warehouse.modules.productputinlistmodule import ProductputinlistModule

from workshop.modules.midproddetailmodule import MidproddetailModule
from workshop.modules.oddmentdetailmodule import OddmentdetailModule


class MenuModule(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = ''
        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.showtime)
        self.setupUi(self)

        self._signalAndslot()
        screen = QtWidgets.QApplication.desktop().screenGeometry(0)
        width = screen.width() / 12
        hegiht = screen.height() / 12
        size = QtCore.QRect(10, 20, 30, 30)
        self.centralwidget.resize(width * 12, hegiht * 12)
        # 用于存放已经打开了的选项卡
        self.tablist = []

    def showtime(self):
        time = QtCore.QDateTime.currentDateTime()
        time_display = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.datetime.setText(time_display)

    def _signalAndslot(self):
        self.menulist.itemDoubleClicked.connect(self.display)
        self.tabWidget.tabCloseRequested.connect(self.on_close_requested)

    def display(self, qtreeitem):
        item = qtreeitem.text(0)
        if not item in MODULE_NAME:
            return
        tabname = MODULE_NAME[item][0]
        module = MODULE_NAME[item][1]
        if tabname in self.tablist:
            self.tabWidget.setCurrentIndex(self.tablist.index(tabname))
        else:
            menu = module(self)
            tab_no = self.tabWidget.addTab(menu, item)
            self.tabWidget.setCurrentIndex(tab_no)
            self.tablist.append(tabname)

    def on_close_requested(self, p_str):
        self.tabWidget.removeTab(p_str)
        del(self.tablist[p_str])

MODULE_NAME = {
    "部门员工管理": ("clerkdept", Clerks),
    "物料字典": ("stuffdict", StuffDictionary),
    "产品字典": ("productdict", ProductDictionary),
    "请验取样": ("sampling", LabsamplelistModule),
    "检验报告": ("labreport", LabreportlistModule),
    "生产指令": ("producingplan", Producingplan),
    "生产车间": ("production", Producingplan),
    "半成品登记/发放": ("midproddraw", MidproddetailModule),
    "零头登记/发放": ("oddmentdetail", OddmentdetailModule),
    "零头寄库": ("oddmentputin", OddmentputinnoteModule),
    "产品寄库": ("prodputin", ProductputinlistModule),
    "生产领料": ("stuffpicking", StuffpickingModule)
}