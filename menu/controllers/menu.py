import sys
from PyQt5 import QtCore, QtGui, QtWidgets


from db.models import Selfdefinedformat


from menu.views.mainmenu import Ui_MainWindow
from clerks.controllers.deptclerks import Clerks
from stuff.controllers.stuffdictionary import StuffDictionary

from supplyer.modules.purchasingplanmodule import PurchasingplanModule

from product.controllers.productdictionary import ProductDictionary
from product.controllers.producingplan import Producingplan

from labrecord.modules.labsamplelistmodule import LabsamplelistModule
from labrecord.modules.labreportlistmodule import LabreportlistModule

from warehouse.modules.stuffpickingmodule import StuffpickingModule
from warehouse.modules.oddmentputinnotemodule import OddmentputinnoteModule
from warehouse.modules.productputinlistmodule import ProductputinlistModule
from warehouse.modules.purchaseregistrationmodule import PurchaseRegistrationModule
from warehouse.modules.purstuffcheckinmodule import PurStuffCheckInModule

from workshop.modules.midproddetailmodule import MidproddetailModule
from workshop.modules.oddmentdetailmodule import OddmentdetailModule



class Menu(QtWidgets.QMainWindow, Ui_MainWindow):
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
        if item == "部门员工管理":
            if "clerkdept" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("clerkdept"))
            else:
                menu = Clerks(self)
                tab_no = self.tabWidget.addTab(menu, "部门员工")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("clerkdept")
        elif item == "物料字典":
            if "stuffdict" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("stuffdict"))
            else:
                menu = StuffDictionary(self)
                tab_no = self.tabWidget.addTab(menu, "物料字典")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("stuffdict")
        elif item == "产品字典":
            if "productdict" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("productdict"))
            else:
                menu = ProductDictionary(self)
                tab_no = self.tabWidget.addTab(menu, "产品字典")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("productdict")
        elif item == "请验取样":
            if "sampling" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("sampling"))
            else:
                menu = LabsamplelistModule(self)
                tab_no = self.tabWidget.addTab(menu, "请验取样")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("sampling")
        elif item == "检验报告":
            if "labreport" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("labreport"))
            else:
                menu = LabreportlistModule(self)
                tab_no = self.tabWidget.addTab(menu, "检验报告")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("labreport")
        elif item == "生产指令":
            if "producingplan" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("producingplan"))
            else:
                menu = Producingplan(self)
                tab_no = self.tabWidget.addTab(menu, "生产指令")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("producingplan")
        elif item == "生产车间":
            if "production" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("production"))
            else:
                menu = Producingplan(self, flag=1)
                tab_no = self.tabWidget.addTab(menu, "生产车间")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("production")
        elif item == "自定义文档":
            if "selfdefineformat" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("selfdefineformat"))
            else:
                menu = test.XMLRW(self)

                scroller = menu.scrollArea.horizontalScrollBar()
                scroller.setValue(200)
                res = Selfdefinedformat.objects.filter(autoid=2855)
                menu.__setattr__('autoid', 50)
                menu.openxml(res[0].format)
                menu.scrollAreaWidgetContents.adjustSize()
                menu.scrollAreaWidgetContents.setMinimumSize(menu.scrollAreaWidgetContents.size())

                tab_no = self.tabWidget.addTab(menu, "自定义文档")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("selfdefineformat")

        elif item == "半成品登记/发放":
            if "midproddraw" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("midproddraw"))
            else:
                menu = MidproddetailModule(self)
                tab_no = self.tabWidget.addTab(menu, "生产领料")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("midproddraw")
        elif item == "零头登记/发放":
            if "midproddraw" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("midproddraw"))
            else:
                menu = MidproddetailModule(self)
                tab_no = self.tabWidget.addTab(menu, "生产领料")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("midproddraw")
        elif item == "生产领料":
            if "stuffpicking" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("stuffpicking"))
            else:
                menu = StuffpickingModule(self)
                tab_no = self.tabWidget.addTab(menu, "生产领料")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("stuffpicking")
        elif item == "产品寄库":
            if "prodputin" in self.tablist:
                self.tabWidget.setCurrentIndex(self.tablist.index("prodputin"))
            else:
                menu = ProductputinlistModule(self)
                tab_no = self.tabWidget.addTab(menu, "产品寄库")
                self.tabWidget.setCurrentIndex(tab_no)
                self.tablist.append("prodputin")

    def on_close_requested(self, p_str):
        self.tabWidget.removeTab(p_str)
        del(self.tablist[p_str])
