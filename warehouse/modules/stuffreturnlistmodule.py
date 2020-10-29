from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot, QTimer

from warehouse.controllers.warehousecontroller import WarehouseController

from warehouse.modules.stuffreturninmodule import StuffReturnInModule

from warehouse.views.stuffreturnlist import Ui_Form

import datetime


# 物料字典几个按键对应的值
PAPERTYPE = ("原辅材料领料单", "内包材领料单", "外包材领料单")


class StuffReturnListModule(QDialog, Ui_Form):
    def __init__(self, parent=None):
        super(StuffReturnListModule, self).__init__(parent)
        self.setupUi(self)
        # 数据库操作类
        self.WC = WarehouseController()

        # 显示物料列表
        self.show_stuffdrawpaper_list()
        # 隐藏第一列的id
        self.stuffdrawpaperlist.hideColumn(0)

    # 显示领料单列表内容
    # stufftype默认为已提交的领料单
    def show_stuffdrawpaper_list(self):
        self.stuffdrawpaperlist.clear()

        paperstatus = self.tabWidget.currentIndex() + 1
        key_dict = {'status': paperstatus}
        self.stuffdrawpaper = self.WC.get_stuffdrawpaper(False, **key_dict).\
            extra(
            select={
                'prodid': 'producingplan.prodid',
                'prodname': 'producingplan.prodname',
                'spec': 'producingplan.spec',
                'package': 'producingplan.package',
                'batchno': 'producingplan.batchno'
            },
            tables=['producingplan'],
            where=['stuffdrawpaper.ppid=producingplan.autoid']
        ).values(*VALUES_TUPLE)
        if not len(self.stuffdrawpaper):
            self.countlabel.setText("共0条记录")
            return
        self.countlabel.setText("共%s条记录" % len(self.stuffdrawpaper))
        for item in self.stuffdrawpaper:

            stufflist = QTreeWidgetItem(self.stuffdrawpaperlist)
            stufflist.setText(0, str(item['autoid']))
            stufflist.setText(1, PAPERTYPE[item['papertype']])
            stufflist.setText(
                2, item['wdchargerid'] + ' ' + item['wdchargername']
            )
            stufflist.setText(3, str(item['wddate']))
            stufflist.setText(
                4, item['wddrawerid'] + ' ' + item['wddrawername']
            )
            stufflist.setText(
                5, str(item['wddrawdate']) if type(item['wddrawdate']) is
                                              datetime.date else ''
            )
            stufflist.setText(6, item['prodid'] + ' ' + item['prodname'])
            stufflist.setText(7, item['spec'])
            stufflist.setText(8, item['package'])
            stufflist.setText(9, item['batchno'])

        for i in range(1, 10):
            self.stuffdrawpaperlist.resizeColumnToContents(i)

    # 刷新功能
    @pyqtSlot()
    def on_pushButton_refresh_clicked(self):
        self.show_stuffdrawpaper_list()

    # 物料列表双击功能
    @pyqtSlot(QTreeWidgetItem, int)
    def on_stuffdrawpaperlist_itemDoubleClicked(self, QTreeWidgetItem, p_int):
        sdpid = QTreeWidgetItem.text(0)
        # 物料详细列表
        detail = StuffReturnInModule(sdpid, self)
        detail.accepted.connect(self.show_stuffdrawpaper_list)
        # 修改了物料记录，刷新列表
        detail.show()

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        tab = getattr(self, 'tab_' + str(p_int))
        tab.setLayout(self.gridLayout_2)
        self.show_stuffdrawpaper_list()


VALUES_TUPLE = (
    'autoid', 'papertype', 'wdchargerid', 'wdchargername', 'wddate',
    'wddrawerid', 'wddrawername', 'wddrawdate', 'prodid', 'prodname', 'spec',
    'package', 'batchno'
)
