# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QWidget, QTreeWidgetItem, QMenu, \
    QComboBox, QFileDialog, QGridLayout
from PyQt5.QtGui import QImage, QPixmap, QBrush, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QDate, QPoint

from labrecord.controllers.labrecordscontroller import LabrecordsController

from labrecord.modules.selectoricheckpaper import SelectoricheckpaperModule
from labrecord.modules.oricheckpapermodule import OricheckpaperModule
from labrecord.modules.editcheckitemmodule import EditcheckitemModule

from labrecord.views.checkreport import Ui_MainWindow

from lib.utils.messagebox import MessageBox
from lib.utils.pdf2pxmap import render_pdf_page

import user

import datetime
import fitz
import os

CHECK_RESULT = ("符合规定", "不符合规定")


class CheckreportModule(QMainWindow, Ui_MainWindow):
    accepted = pyqtSignal()

    def __init__(self, autoid, parent=None):
        super(CheckreportModule, self).__init__(parent)
        self.setupUi(self)
        self.autoid = autoid
        self.ori_detail = dict()
        self.new_detail = dict()
        self.ori_checkitem = []
        self.new_checkitem = []
        self.images_list = []
        self.current_img = object
        self.current_page = object
        self.LC = LabrecordsController()
        # 自动缩放
        self.label_image.setScaledContents(True)

        # 获取当前报告的信息
        has_find_report = self.get_report_detail(self.autoid)
        # 获取检验项目
        self.get_checkitem()
        if has_find_report:
            # 获取检验依据的下拉项目
            self.get_combobox_items(
                self.comboBox_checkgist, 'checkgist',
                chkid=self.ori_detail['chkid']
            )
            # 获取结论的下拉项目
            self.get_combobox_items(
                self.comboBox_result, 'result', chkid=self.ori_detail['chkid']
            )

        # 获取图片
        self.get_images(autoid)
        # 获取原始检验记录
        self.get_oricheckpaper(autoid)
        # 检验项目的右键菜单功能
        if len(self.ori_detail):
            if self.ori_detail['paperno'] == '':
                self.get_paperno()
            self.new_paperstatus = self.ori_detail['paperstatus']
            # 根据签名情况确定是否允许修改签名
            self.set_paperstatus()

    def set_paperstatus(self):
        paperstatus = self.ori_detail['paperstatus']
        if paperstatus == 1:
            # 检验人已经签名
            self.pushButton_reporter.setEnabled(True)
            self.pushButton_checker.setEnabled(True)
            self.pushButton_warrantor.setEnabled(True)
        elif paperstatus == 2:
            # 复核人已经签名
            self.pushButton_reporter.setEnabled(False)
            self.pushButton_checker.setEnabled(True)
            self.pushButton_warrantor.setEnabled(True)
        elif paperstatus == 3:
            # 审核人已经签名
            self.pushButton_reporter.setEnabled(False)
            self.pushButton_checker.setEnabled(False)
            self.pushButton_warrantor.setEnabled(True)

    def get_report_detail(self, autoid):
        values_list = [
            'chkid', 'chkname', 'spec', 'package', 'applydate', 'sampleamount',
            'sampleunit', 'sampledate', 'samplesource', 'checkamount', 'caunit',
            'batchno', 'mbatchno', 'supplyer', 'producer', 'paperno',
            'reportdate', 'checkgist', 'reporterid', 'reportername',
            'checkerid', 'checkername', 'warrantorid', 'warrantorname',
            'result', 'conclusion', 'labtype', 'paperstatus'
        ]
        key_dict = {'autoid': autoid}
        res = self.LC.get_labrecord(False, *values_list, **key_dict)
        if len(res) == 1:
            self.ori_detail = res[0]
            self.label_chkitem.setText(
                self.ori_detail['chkid'] + self.ori_detail['chkname'])
            self.label_spec.setText(self.ori_detail['spec'])
            self.label_package.setText(self.ori_detail['package'])
            self.label_applydate.setText(str(self.ori_detail['sampledate']))
            self.label_sampleamount.setText(
                str(self.ori_detail['sampleamount']) + self.ori_detail[
                    'sampleunit'])
            self.label_sampledate.setText(str(self.ori_detail['sampledate']))
            self.label_samplesource.setText(self.ori_detail['samplesource'])
            self.label_checkamount.setText(
                str(self.ori_detail['checkamount']) + self.ori_detail['caunit'])
            self.label_batchno.setText(self.ori_detail['batchno'])
            self.label_supplyer.setText(self.ori_detail['supplyer'])
            self.label_producer.setText(self.ori_detail['producer'])
            self.label_mbatchno.setText(self.ori_detail['mbatchno'])
            self.lineEdit_paperno.setText(self.ori_detail['paperno'])
            self.dateEdit_reportdate.setDate(
                self.ori_detail['reportdate'] if
                type(self.ori_detail[
                    'reportdate']) is datetime.date else user.now_date
            )
            self.comboBox_checkgist.addItem(self.ori_detail['checkgist'])
            self.comboBox_checkgist.setCurrentText(self.ori_detail['checkgist'])
            self.pushButton_reporter.setText(
                self.ori_detail['reporterid'] + ' ' + self.ori_detail[
                    'reportername'])
            self.pushButton_checker.setText(
                self.ori_detail['checkerid'] + ' ' + self.ori_detail[
                    'checkername'])
            self.pushButton_warrantor.setText(
                self.ori_detail['warrantorid'] + ' ' + self.ori_detail[
                    'warrantorname'])
            self.comboBox_result.addItem(self.ori_detail['result'])
            self.comboBox_result.setCurrentText(self.ori_detail['result'])
            self.checkBox_conclusion.setCheckState(
                self.ori_detail['conclusion'])
            return True
        else:
            return False

    def get_checkitem(self):
        values_list = [
            'autoid', 'kind', 'itemname', 'labvalue', 'referencevalue',
            'checked', 'startdate', 'enddate', 'checkerid', 'checkername',
            'result'
        ]
        key_dict = {'lrid': self.autoid}
        res = self.LC.get_labitem(False, *values_list, **key_dict)
        self.ori_checkitem = res.order_by('kind', 'seqid')

        self.treeWidget_checkitem.clear()
        if not len(self.ori_checkitem):
            return
        for item in self.ori_checkitem:
            qtreeitem = QTreeWidgetItem(self.treeWidget_checkitem)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['kind'])
            qtreeitem.setText(2, item['itemname'])
            qtreeitem.setText(
                3, str(item['startdate']) if type(item['startdate']) is
                                             datetime.date else ''
            )
            qtreeitem.setText(
                4, str(item['enddate']) if type(item['enddate'])
                                           is datetime.date else ''
            )
            qtreeitem.setText(5, item['referencevalue'])
            qtreeitem.setText(6, item['labvalue'])
            qtreeitem.setText(7, CHECK_RESULT[item['result']])
            qtreeitem.setText(8, item['checkerid'] + item['checkername'])
            qtreeitem.setCheckState(1, item['checked'])
            if item['result'] == 1:
                brush = QBrush(1)
                brush.setColor(QColor(255, 0, 0))
                for i in range(1, 9):
                    qtreeitem.setBackground(i, brush)

        self.treeWidget_checkitem.hideColumn(0)
        for i in range(1, 8):
            self.treeWidget_checkitem.resizeColumnToContents(i)
            if self.treeWidget_checkitem.columnWidth(i) > 200:
                self.treeWidget_checkitem.setColumnWidth(i, 200)

    # 检验依据和结论获取下拉内容
    def get_combobox_items(self, qcombobox: QComboBox, *args, **kwargs):
        if type(qcombobox) == QComboBox:
            text = qcombobox.currentText()
            res = self.LC.get_labrecord(True, *args, **kwargs)
            key = dict(zip(args, [text, ]))
            items = res.exclude(**key)
            qcombobox.addItems(set(items))

    def get_paperno(self):
        res = self.LC.get_paperno(self.autoid)
        self.lineEdit_paperno.setText(res[0])

    def get_images(self, lrid):
        self.treeWidget_imagenamelist.clear()
        res = self.LC.get_labimages(False, scid=lrid)
        self.images_list = res

        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_imagenamelist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, str(item['imageid']))
            qtreeitem.setText(2, item['title'])
            qtreeitem.setText(3, item['creatorid'] + item['creatorname'])
            qtreeitem.setText(4, str(item['createdate']))

    def get_oricheckpaper(self, lrid):
        values_list = ['autoid', 'formname']
        key_dict = {
            'lrid': lrid
        }
        res = self.LC.get_oricheckpaper(False, *values_list, **key_dict)
        for item in res:
            tabpage = QWidget()
            tabpage.setObjectName("oriid_" + str(item['autoid']))
            self.tabWidget.addTab(tabpage, item['formname'])

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_checkitem_itemDoubleClicked(self, qtreeitem, p_int):
        item_id = int(qtreeitem.text(0))
        detail = EditcheckitemModule(item_id, self)
        detail.accepted.connect(self.get_checkitem)
        detail.show()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_checkitem_itemClicked(self, qtreeitem, p_int):
        if p_int == 1:
            newstate = qtreeitem.checkState(1)
            for item in self.ori_checkitem:
                if int(qtreeitem.text(0)) == item['autoid']:
                    if newstate != item['checked']:
                        it = {'autoid': int(qtreeitem.text(0)),
                              'checked': newstate
                              }
                        self.new_checkitem.append(it)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_imagenamelist_itemDoubleClicked(self, qtreeitem, p_int):

        rela_id = int(qtreeitem.text(0))
        for item in self.images_list:
            if item['autoid'] == rela_id:

                if item['ext'].lower() == 'pdf':
                    self.comboBox_jumpto.setVisible(True)
                    self.pushButton_prepage.setVisible(True)
                    self.pushButton_nextpage.setVisible(True)
                    self.current_img = fitz.Document(stream=item['image'],
                                                     filetype='pdf')
                    page_count = self.current_img.pageCount
                    page_list = []
                    self.comboBox_jumpto.clear()
                    for i in range(1, page_count + 1):
                        page_list.append('第' + str(i) + '页')
                    self.comboBox_jumpto.addItems(page_list)
                    self.current_page = self.current_img.loadPage(0)

                else:
                    self.comboBox_jumpto.setVisible(False)
                    self.pushButton_prepage.setVisible(False)
                    self.pushButton_nextpage.setVisible(False)
                    img = QImage.fromData(item['image'])
                    self.current_img = QPixmap.fromImage(img)
                    self.label_image.setPixmap(self.current_img)
                break
        # 默认放大为3被，同时自动调用on_horizontalSlider_zoom_valueChanged
        self.horizontalSlider_zoom.setValue(30)

    @pyqtSlot(int)
    def on_horizontalSlider_zoom_valueChanged(self, p_int):

        try:
            self.label_zoom.setText(str(p_int * 10) + '%')
            # 把当前页面转为QPixmap,并缩放为p_int/10
            cover = render_pdf_page(self.current_page, p_int / 10, p_int / 10)
            self.label_image.setPixmap(cover)
        except AttributeError:
            size = self.current_img.size()
            new_pixmap = self.current_img.scaled(size.width() * p_int / 10,
                                                 size.height() * p_int / 10)
            self.label_image.setPixmap(new_pixmap)

    @pyqtSlot(QPoint)
    def on_treeWidget_imagenamelist_customContextMenuRequested(self, pos):
        # 返回调用者的对象
        sender_widget = self.sender()
        menu = QMenu()
        button1 = menu.addAction("新增图片")
        button2 = menu.addAction("修改图片")
        button3 = menu.addAction("删除图片")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        res = "rollback"
        # 增加
        if action == button1:
            img_names, img_type = QFileDialog.getOpenFileNames(
                self, "打开图片", os.path.expanduser("~") + "\Desktop",
                "*.jpg;;*.png;;*.bmp;;*.gif;;*.pdf;;All Files(*)"
            )
            for item in img_names:
                imagename_no_ext = item.split("/")[-1]
                image_ext = item.split(".")[1]
                if image_ext.lower() not in ("jpg", "png", "bmp", "gif", "pdf"):
                    continue
                fp = open(item, 'rb')
                with fp:
                    image_byte = fp.read()
                    fp.close()
                imagedetail = {
                    'img': image_byte,
                    'ext': image_ext
                }
                reladetail = {
                    'kind': 2,
                    'scid': self.autoid,
                    'title': imagename_no_ext,
                    'creatorid': user.user_id,
                    'creatorname': user.user_name,
                    'createdate': user.now_date
                }

                res = self.LC.update_labimages(reladetail, imagedetail)

        # 修改
        elif action == button2:
            rela_id = self.treeWidget_imagenamelist.currentItem().text(0)
            img_id = self.treeWidget_imagenamelist.currentItem().text(1)
            img_name, img_type = QFileDialog.getOpenFileName(
                self, "打开图片", os.path.expanduser("~") + "\Desktop",
                "*.jpg;;*.png;;*.bmp;;*.gif;;*.pdf;;All Files(*)"
            )
            imagename_no_ext = img_name.split("/")[-1]
            image_ext = img_name.split(".")[1]
            if image_ext.lower() in ("jpg", "png", "bmp", "gif", "pdf"):
                fp = open(img_name, 'rb')
                with fp:
                    image_byte = fp.read()
                    fp.close()
                imagedetail = {
                    'img': image_byte,
                    'ext': image_ext
                }
                reladetail = {
                    'title': imagename_no_ext,
                    'creatorid': user.user_id,
                    'creatorname': user.user_name,
                    'createdate': user.now_date
                }

                res = self.LC.update_labimages(reladetail, imagedetail, rela_id,
                                               img_id)

        # 删除
        elif action == button3:
            select_item = sender_widget.selectedItems()
            rela_id = []
            img_id = []
            for item in select_item:
                rela_id.append(item.text(0))
                img_id.append(item.text(1))
            res = self.LC.delete_labimages(rela_id, img_id)

        if res == "accept":
            self.get_images(self.autoid)

    @pyqtSlot(int)
    def on_comboBox_jumpto_currentIndexChanged(self, p_int):
        try:
            self.current_page = self.current_img.loadPage(p_int)
            self.on_horizontalSlider_zoom_valueChanged(
                self.horizontalSlider_zoom.value())
        except (AttributeError, ValueError):
            pass

    @pyqtSlot()
    def on_pushButton_prepage_clicked(self):
        index = self.comboBox_jumpto.currentIndex()
        if index - 1 >= 0:
            try:
                self.current_page = self.current_img.loadPage(index - 1)
                self.comboBox_jumpto.setCurrentIndex(index - 1)
            except (AttributeError, ValueError):
                pass

    @pyqtSlot()
    def on_pushButton_nextpage_clicked(self):
        index = self.comboBox_jumpto.currentIndex()
        if index + 1 < self.comboBox_jumpto.count():
            try:
                self.current_page = self.current_img.loadPage(index + 1)
                self.comboBox_jumpto.setCurrentIndex(index + 1)
            except (AttributeError, ValueError):
                pass

    @pyqtSlot()
    def on_pushButton_add_oripaper_clicked(self):
        dictid = self.ori_detail['chkid']
        itemtype = int(self.ori_detail['labtype'])
        detail = SelectoricheckpaperModule(dictid, itemtype, self)
        detail.selected.connect(self.selectoricheckpaper)
        detail.show()

    @pyqtSlot(list)
    def selectoricheckpaper(self, p_list):
        if not len(p_list):
            return
        detail = {
            'lrid': self.autoid,
            'creatorid': user.user_id,
            'creatorname': user.user_name,
            'createdate': user.now_date
        }
        res = self.LC.update_oricheckpaper(sdfid_list=p_list, **detail)
        for item in res:
            tabpage = QWidget()
            tabpage.setObjectName("oriid_" + str(item.autoid))
            self.tabWidget.addTab(tabpage, item.formname)

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        if p_int <= 1:
            return
        # 点击的是原始检验记录
        current_widget = self.tabWidget.currentWidget()
        if current_widget.children():
            return
        objname = current_widget.objectName()

        try:
            ori_id = int(objname.split('_')[1])
        except TypeError:
            # TypeError:objname的第二段不是数字
            return
        self.current_content = OricheckpaperModule(ori_id, self)
        gridlayout = QGridLayout(current_widget)
        gridlayout.addWidget(self.current_content)

    @pyqtSlot(str)
    def on_lineEdit_paperno_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['paperno']:
                self.new_detail['paperno'] = p_str
            else:
                try:
                    del self.new_detail['paperno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['paperno'] = p_str

    @pyqtSlot(QDate)
    def on_dateEdit_reportdate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['reportdate']) is str:
                self.new_detail['reportdate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['reportdate']):
                self.new_detail['reportdate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['reportdate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['reportdate'] = q_date.toPyDate()

    @pyqtSlot(str)
    def on_comboBox_checkgist_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['checkgist']:
                self.new_detail['checkgist'] = p_str
            else:
                try:
                    del self.new_detail['checkgist']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['checkgist'] = p_str

    @pyqtSlot(str)
    def on_comboBox_result_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['result']:
                self.new_detail['result'] = p_str
            else:
                try:
                    del self.new_detail['result']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['result'] = p_str

    @pyqtSlot(int)
    def on_checkBox_conclusion_stateChanged(self, p_int):
        try:
            if p_int != self.ori_detail['conclusion']:
                self.new_detail['conclusion'] = p_int
            else:
                try:
                    del self.new_detail['conclusion']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['conclusion'] = p_int

    @pyqtSlot(str)
    def on_pushButton_reporter_signChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['reporterid'] or name != self.ori_detail[
                'opertername']:
                self.new_detail['reporterid'] = id
                self.new_detail['reportername'] = name
                if id != '':
                    self.new_paperstatus = 1
                else:
                    self.new_paperstatus = 0
            else:
                try:
                    del self.new_detail['reporterid']
                    del self.new_detail['reportername']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['reporterid'] = id
            self.new_detail['reportername'] = name

    @pyqtSlot(str)
    def on_pushButton_checker_signChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['checkerid'] or name != self.ori_detail[
                'checkername']:
                self.new_detail['checkerid'] = id
                self.new_detail['checkername'] = name
                if id != '':
                    self.new_paperstatus = 2
                else:
                    self.new_paperstatus = 1
            else:
                try:
                    del self.new_detail['checkerid']
                    del self.new_detail['checkername']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['checkerid'] = id
            self.new_detail['checkername'] = name

    @pyqtSlot(str)
    def on_pushButton_warrantor_signChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['warrantorid'] or name != self.ori_detail[
                'warrantorname']:
                self.new_detail['warrantorid'] = id
                self.new_detail['warrantorname'] = name
                if id != '':
                    self.new_paperstatus = 3
                else:
                    self.new_paperstatus = 2
            else:
                try:
                    del self.new_detail['warrantorid']
                    del self.new_detail['warrantorname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['warrantorid'] = id
            self.new_detail['warrantorname'] = name

    @pyqtSlot()
    def on_pushButton_save_clicked(self):
        if self.new_paperstatus != self.ori_detail['paperstatus']:
            self.new_detail['paperstatus'] = self.new_paperstatus
        if len(self.new_detail):
            res = self.LC.update_labrecord(self.autoid, **self.new_detail)
            if res:
                self.new_detail = {}
            if len(self.new_checkitem):
                for item in self.new_checkitem:
                    res = self.LC.update_labitem(**item)
                    if res:
                        self.new_checkitem = {}
            self.accepted.emit()
            # self.close()

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if self.new_paperstatus != self.ori_detail['paperstatus']:
            self.new_detail['paperstatus'] = self.new_paperstatus
        if self.checkBox_conclusion.checkState() == 0:
            self.new_detail['status'] = 4
        else:
            self.new_detail['status'] = 3
        res = self.LC.update_labrecord(self.autoid, **self.new_detail)
        if res:
            self.new_detail = {}
        if len(self.new_checkitem):
            for item in self.new_checkitem:
                res = self.LC.update_labitem(**item)
                if res:
                    self.new_checkitem = {}
        self.accepted.emit()
        self.close()

    def closeEvent(self, qcloseevent):
        if len(self.new_detail):
            qdialog = MessageBox(
                self, title="提醒", text="检验报告书",
                informative="是否保存修改？"
            )
            res = qdialog.exec()
            if res == 16384:
                self.on_pushButton_save_clicked()

        for i in range(2, self.tabWidget.count() + 1):
            widgets = self.tabWidget.widget(i)

            try:
                for item in widgets.children():
                    try:
                        if item.current_content.flat == 1:
                            qdialog = MessageBox(
                                self, title="提醒",
                                text=self.tabWidget.tabText(i),
                                informative="是否保存修改？"
                            )
                            res = qdialog.exec()
                            if res == 16384:
                                item.on_pushButton_accept_clicked()
                    except AttributeError:
                        pass
            except AttributeError:
                pass
