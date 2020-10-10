# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QFileDialog, QTreeWidgetItem, QMenu, \
    QApplication

from PyQt5.QtCore import pyqtSlot, QPoint, QUrl, QXmlStreamWriter, QIODevice, \
    QFile

from warehouse.controllers.warehousecontroller import WarehouseController
from product.controllers.productcontroller import ProductController
from system.controllers.systemcontroller import SystemController
from sale.controllers.salecontroller import SaleController

from qrcode.views.qrcodeoutput import Ui_Form

from lib.utils.messagebox import MessageBox

import datetime
import re

import user


class QrcodeoutputModule(QWidget, Ui_Form):
    """ 二维码出库文件模块，可以查看到所有订单的二维码记录。
    提供了右键下载二维码。
    """

    def __init__(self, parent=None):
        super(QrcodeoutputModule, self).__init__(parent)
        self.setupUi(self)
        self.WC = WarehouseController()
        self.PC = ProductController()
        self.SC = SystemController()
        self.SLC = SaleController()
        self.orderlist = dict()
        # 获取二维码信息
        self.get_order_list()

    def get_order_list(self):
        self.treeWidget_orderlist.clear()
        self.treeWidget_prodlist.hideColumn(0)
        key_dict = dict()
        index = self.tabWidget.currentIndex()
        if index in (0, 1):
            key_dict['status'] = index + 1
        else:
            key_dict['status__gte'] = 1
        self.orderlist = self.WC.get_prodputoutpaper(False, *VALUES_LIST,
                                                  **key_dict)
        if not len(self.orderlist):
            return
        for item in self.orderlist:
            qtreeitem = QTreeWidgetItem(self.treeWidget_orderlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, str(item['putoutdate']))
            qtreeitem.setText(2, item['pokind'])
            qtreeitem.setText(3, item['clientid'] + ' ' + item['clientname'])
            qtreeitem.setText(4, item['auditorid'] + ' ' + item['auditorname'])
            qtreeitem.setText(5, str(item['remark']))
        for i in range(1, 6):
            self.treeWidget_orderlist.resizeColumnToContents(i)

    @pyqtSlot(QPoint)
    def on_treeWidget_orderlist_customContextMenuRequested(self, pos):
        qtreeitem = self.treeWidget_orderlist.selectedItems()
        if not len(qtreeitem):
            return
        select_id = int(qtreeitem[0].text(0))
        menu = QMenu()
        button1 = menu.addAction("生成出库数据文件")
        # button2 = menu.addAction("导入入库二维码数据")
        # button3 = menu.addAction("覆盖入库二维码数据")
        g_pos = self.treeWidget_orderlist.mapToGlobal(pos)
        action = menu.exec(g_pos)
        if action == button1:
            clipboard = QApplication.clipboard()
            dir = clipboard.property("qrcodeoutputurl")
            filename = "出库数据" + str(user.now_date).replace("-", "") + ".xml"
            if not dir:
                dir = "C:\\"
            file_route, ext = QFileDialog.getSaveFileName(
                self, "请选择出库文件输出路径", dir + filename, "*.xml;;All Files(*)"
            )

            if not file_route:
                return
            selected_dir = re.findall(r'^(.+/|.+\\)', file_route)[0]
            clipboard.setProperty("qrcodeoutputurl", selected_dir)

            self.makeqrcodeoutputfile(select_id, file_route)
            self.WC.update_prodputoutpaper(select_id, status=2)
            self.get_order_list()

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        getattr(self, 'tab_' + str(index)).setLayout(self.gridLayout_2)
        self.get_order_list()

    def makeqrcodeoutputfile(self, id, file_route):
        for item in self.orderlist:
            if item['autoid'] == id:
                proddetail = item
                break
        clientid = proddetail['clientid']
        key_dict_client = {'clientid': clientid}
        clients_detail = self.SLC.get_client(
            False, *VALUES_LIST_CLIENT, **key_dict_client
        )
        if len(clients_detail) != 1:
            return
        client = clients_detail[0]

        key_dict = {
            'ppopid': id
        }
        res = self.WC.get_ppopqrcode(False, *VALUES_LIST_QRCODE, **key_dict)
        if not len(res):
            return
        # 把二维码按比例分组
        q_list, ppid_list, batchno_list = self.sort_qrcode(res.order_by('batchno'))

        xml = QXmlStreamWriter()
        qfile=QFile(file_route)
        if qfile.open(QIODevice.WriteOnly):
            xml.setDevice(qfile)
        else:
            return
        xml.setAutoFormatting(True)
        xml.writeStartDocument()
        # 添加头文件信息
        self.addxmlheader(xml, client['kind'])
        self.addxmlproddetail(xml, proddetail)
        temp_ppid = ''
        for i in range(0, len(ppid_list)):
            if temp_ppid != ppid_list[i]:
                if temp_ppid != '':
                    # 把上一个Batch结束了
                    xml.writeEndElement()
                temp_ppid = ppid_list[i]
                xml.writeStartElement("Batch")
                xml.writeAttribute('batchNo', batchno_list[i])
                xml.writeAttribute('operator', proddetail['auditorname'])
                xml.writeAttribute('oprDate', str(proddetail['putoutdate']))

                xml.writeAttribute(' toUnit', client['clientname'])
                xml.writeAttribute('toProvince', client['province'])
                xml.writeAttribute('toCity', client['city'])
                xml.writeAttribute('toCounty', client['county'])
                xml.writeAttribute('toUnitcode', client['unitcode'])

            xml.writeStartElement("Data")
            xml.writeAttribute('code', q_list[i])
            xml.writeEndElement()

        xml.writeEndElement()
        xml.writeEndElement()
        xml.writeEndDocument()

    def sort_qrcode(self, qrcode_list):
        q_list = []
        ppid_list = []
        batchno_list = []
        try:
            for item in qrcode_list:
                q_list.append(item['qr0'])
                ppid_list.append(item['ppid'])
                batchno_list.append(item['batchno'])
        except KeyError:
            pass
        return q_list, ppid_list, batchno_list

    def addxmlheader(self, xml, toUnitType):
        company = "智普飞扬"
        mancode = "19060310"
        key_dict_sys = {'varname__in': ("company", "mancode")}
        res = self.SC.get_syssetting(False, *VALUES_LIST_SYS, **key_dict_sys)
        if len(res):
            for item in res:
                if item['varname'] == "company":
                    company = item['varvalue']
                elif item ['varname'] == "mancode":
                    mancode = item['varvalue']
        xml.writeStartElement("DataList")
        xml.writeAttribute("corpName", company)
        xml.writeAttribute("toUnitType", str(toUnitType))
        xml.writeAttribute("manCode", mancode)
        xml.writeAttribute("dataType", "wareHouseOut")
        xml.writeAttribute("version", "1.1")
        xml.writeAttribute("xmlns: xsi", "http://www.w3.org/2001/XMLSchema-instance")
        xml.writeAttribute("xsi: noNamespaceSchemaLocation", "兽药产品出库数据1.1.xsd")

    def addxmlproddetail(self, xml, proddetail):
        xml.writeStartElement("Product")


VALUES_LIST = (
    'autoid', 'createdate', 'pokind', 'creatorid', 'creatorname', 'clientid',
    'clientname', 'putoutdate', 'remark', 'auditorid', 'auditorname'
)
VALUES_LIST_SYS = ('varname', 'varvalue')
VALUES_LIST_CLIENT = (
    'clientname', 'kind', 'unitcode', 'province', 'city', 'county'
)
VALUES_LIST_QRCODE = ('ppid', 'batchno', 'qr0')
