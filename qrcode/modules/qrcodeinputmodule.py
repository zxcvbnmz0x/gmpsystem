# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QFileDialog, QTreeWidgetItem, QMenu, \
    QApplication

from PyQt5.QtCore import pyqtSlot, QPoint, QUrl, QXmlStreamWriter, QIODevice, \
    QFile

from workshop.controllers.workshopcontroller import WorkshopController
from product.controllers.productcontroller import ProductController
from system.controllers.systemcontroller import SystemController

from qrcode.views.qrcodeinput import Ui_Form

import re

import user


class QrcodeinputModule(QWidget, Ui_Form):
    """ 二维码入库文件模块，可以查看到所有产品批次的二维码记录。
    提供了右键下载二维码和导入二维码的功能。

    导入二维码和覆盖二维码功能尚未实现。
    导入二维码只把文件里的数据导入，不会覆盖旧有的数据
    覆盖二维码会先把旧的二维码删除了，同时需要把二维码库中的使用状态used改未0
    导入和覆盖进行的同时还需要把新二维码在二维码库中的状态改为used=1
    """

    def __init__(self, parent=None):
        super(QrcodeinputModule, self).__init__(parent)
        self.setupUi(self)
        self.WC = WorkshopController()
        self.PC = ProductController()
        self.SC = SystemController()
        self.prodlist = dict()
        # 获取二维码信息
        self.get_product_list()

    def get_product_list(self):
        self.treeWidget_prodlist.clear()
        self.treeWidget_prodlist.hideColumn(0)
        key_dict = {
            'pltype': 0
        }
        index = self.tabWidget.currentIndex()
        if index in (0, 1):
            key_dict['qrflag'] = index

        self.prodlist = self.PC.get_producingplan(False, *VALUES_LIST,
                                                  **key_dict)
        if not len(self.prodlist):
            return
        for item in self.prodlist:
            qtreeitem = QTreeWidgetItem(self.treeWidget_prodlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['prodid'] + item['prodname'])
            qtreeitem.setText(2, item['batchno'])
            qtreeitem.setText(3, item['spec'])
            qtreeitem.setText(4, item['package'])
            qtreeitem.setText(5, str(item['makedate']))
        for i in range(1, 6):
            self.treeWidget_prodlist.resizeColumnToContents(i)

    @pyqtSlot(QPoint)
    def on_treeWidget_prodlist_customContextMenuRequested(self, pos):
        qtreeitem = self.treeWidget_prodlist.selectedItems()
        if not len(qtreeitem):
            return
        select_ppid = int(qtreeitem[0].text(0))


        menu = QMenu()
        button1 = menu.addAction("生成入库数据文件")
        # button2 = menu.addAction("导入入库二维码数据")
        # button3 = menu.addAction("覆盖入库二维码数据")
        g_pos = self.treeWidget_prodlist.mapToGlobal(pos)
        action = menu.exec(g_pos)
        if action == button1:
            clipboard = QApplication.clipboard()
            dir = clipboard.property("qrcodeinputurl")
            filename = "入库数据" + str(user.now_date).replace("-", "") + ".xml"
            if not dir:
                dir = "C:\\"
            file_route, ext = QFileDialog.getSaveFileName(
                self, "请选择入库文件输出路径", dir + filename, "*.xml;;All Files(*)"
            )

            if not file_route:
                return
            selected_dir = re.findall(r'^(.+/|.+\\)', file_route)[0]
            clipboard.setProperty("qrcodeinputurl", selected_dir)

            self.makeqrcodeinputfile(select_ppid, file_route)
            self.PC.update_producingplan(select_ppid, qrflag=1)
            self.get_product_list()

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        getattr(self, 'tab_' + str(index)).setLayout(self.gridLayout_2)
        self.get_product_list()

    def makeqrcodeinputfile(self, ppid, file_route):
        for item in self.prodlist:
            if item['autoid'] == ppid:
                proddetail = item
                break
        key_dict = {
            'ppid': ppid
        }
        res = self.WC.get_qrcoderep(False, *VALUES_LIST_QRCODE, **key_dict)
        if not len(res):
            return
        # 把二维码按比例分组
        q_list, proportion_list = self.sort_qrcode(res)
        # 把比例相同的合并成一个同一个项目
        q_list_merge, proportion_list_merge = self.merge_qrcode(
            q_list, proportion_list
        )
        xml = QXmlStreamWriter()
        qfile=QFile(file_route)
        if qfile.open(QIODevice.WriteOnly):
            xml.setDevice(qfile)
        else:
            return

        xml.setAutoFormatting(True)
        xml.writeStartDocument()
        # 添加头文件信息
        self.addxmlheader(xml)
        self.addxmlproddetail(xml, proddetail)
        for i in range(0, len(proportion_list_merge)):
            spnum = proportion_list[i][0]
            mpnum = proportion_list[i][1]
            bpnum = proportion_list[i][2]
            lpnum = proportion_list[i][3]
            xml.writeStartElement("Batch")
            xml.writeAttribute('batchNo', proddetail['batchno'])
            xml.writeAttribute('specification', proddetail['spec'])
            xml.writeAttribute('minPackUnit', proddetail['spunit'])
            if spnum != 0:
                minTagUnit = proddetail['spunit']
            elif mpnum != 0:
                minTagUnit = proddetail['mpunit']
            else:
                minTagUnit = proddetail['bpunit']
            tagPackRatio = ''
            for num in (lpnum, bpnum, mpnum, spnum):
                if num != 0:
                    if tagPackRatio == '':
                        tagPackRatio = str(num)
                    else:
                        tagPackRatio += ':' + str(num)
            xml.writeAttribute('minTagUnit', minTagUnit)
            xml.writeAttribute('tagPackRatio', tagPackRatio)
            xml.writeAttribute('produceDate', str(proddetail['makedate']))
            xml.writeAttribute('operator', user.user_name)
            xml.writeAttribute('oprDate', str(user.now_date))
            xml.writeAttribute('count', str(len(q_list_merge[i])))
            xml.writeAttribute(
                'countUnit', '1' if minTagUnit == tagPackRatio else '2'
            )
            qrcode = q_list_merge[i]
            for code in qrcode:
                xml.writeStartElement("Data")
                xml.writeAttribute('code', code)
                xml.writeEndElement()


            xml.writeEndElement()
        xml.writeEndElement()
        xml.writeEndElement()
        xml.writeEndDocument()

    def sort_qrcode(self, qrcode_list):
        q_list = []
        temp_q_list = []
        next_box = False
        # 比例
        proportion_list = []
        temp_proportion_list = []
        spnum = 0
        mpnum = 0
        bpnum = 0
        lpnum = 0

        # qrcode_s = ''
        qrcode_m = ''
        qrcode_b = ''
        qrcode_l = ''
        max_lv = 'lp'
        first_qrcode = qrcode_list[0]
        # qrcode0 = first_qrcode['qrcode0']
        # qrcode1 = first_qrcode['qrcode1']
        qrcode2 = first_qrcode['qrcode2']
        qrcode3 = first_qrcode['qrcode3']
        if qrcode3 == '' and qrcode2 == '':
            max_lv = 'mp'
        elif qrcode3 == '' and qrcode2 != '':
            max_lv = 'bp'

        for item in qrcode_list:

            if qrcode_m == '' and item['qrcode1'] != '':
                qrcode_m = item['qrcode1']
            elif qrcode_m != item['qrcode1']:
                temp_q_list.append(qrcode_m)
                qrcode_m = item['qrcode1']
                mpnum += 1
                if max_lv == 'mp':
                    next_box = True

            if qrcode_b == '' and item['qrcode2'] != '':
                qrcode_b = item['qrcode2']
            elif qrcode_b != item['qrcode2']:
                temp_q_list.append(qrcode_b)
                qrcode_b = item['qrcode2']
                bpnum += 1
                if max_lv == 'bp':
                    next_box = True
            if qrcode_l == '' and item['qrcode3'] != '':
                qrcode_l = item['qrcode3']
            elif qrcode_l != item['qrcode3']:
                temp_q_list.append(qrcode_l)
                qrcode_l = item['qrcode3']
                lpnum += 1
                if max_lv == 'lp':
                    next_box = True

            if next_box:
                q_list.append(temp_q_list)
                temp_q_list = []
                for num in (spnum, mpnum, bpnum, lpnum):
                    temp_proportion_list.append(num)
                spnum = 0
                mpnum = 0
                bpnum = 0
                lpnum = 0
                proportion_list.append(temp_proportion_list)
                temp_proportion_list = []
                next_box = False

            if item['qrcode0'] != '':
                temp_q_list.append(item['qrcode0'])
                spnum += 1
        if len(temp_q_list):
            if qrcode_m != '':
                temp_q_list.append(qrcode_m)
                mpnum += 1
            if qrcode_b != '':
                temp_q_list.append(qrcode_b)
                bpnum += 1
            if qrcode_l != '':
                temp_q_list.append(qrcode_l)
                lpnum += 1

            q_list.append(temp_q_list)
            for item in (spnum, mpnum, bpnum, lpnum):
                temp_proportion_list.append(item)
            proportion_list.append(temp_proportion_list)
        return q_list, proportion_list

    def merge_qrcode(self, q_list, proportion_list):
        q_list_merge = []
        proportion_list_merge = []
        for i in range(0, len(proportion_list)):
            proprotion = proportion_list[i]
            if proprotion in proportion_list_merge:
                index = proportion_list_merge.index(proprotion)
                q_list_merge[index] += q_list[i]
            else:
                proportion_list_merge.append(proprotion)
                q_list_merge.append(q_list[i])
        return q_list_merge, proportion_list_merge

    def addxmlheader(self, xml):
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
        xml.writeAttribute("manCode", mancode)
        xml.writeAttribute("dataType", "wareHouseIn")
        xml.writeAttribute("version", "1.0")
        xml.writeAttribute("xmlns: xsi", "http://www.w3.org/2001/XMLSchema-instance")
        xml.writeAttribute("xsi: noNamespaceSchemaLocation", "兽药产品入库数据_生产企业.xsd")

    def addxmlproddetail(self, xml, proddetail):
        xml.writeStartElement("Product")
        xml.writeAttribute("productName", proddetail['commonname'])
        xml.writeAttribute("pzwh", proddetail['allowno'])
        xml.writeAttribute(
            "packing", str(proddetail['basicamount']) + proddetail['basicunit']
        )


VALUES_LIST = (
    'autoid', 'prodid', 'prodname', 'commonname', 'batchno', 'spec', 'package',
    'makedate', 'lpunit', 'bpunit', 'mpunit', 'spunit', 'basicamount',
    'basicunit', 'allowno'
)
VALUES_LIST_SYS = ('varname', 'varvalue')
VALUES_LIST_QRCODE = ('qrcode0', 'qrcode1', 'qrcode2', 'qrcode3')
