# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSlot

from workshop.views.homepage import Ui_Form
from product.controllers.productcontroller import ProductController
from workshop.controllers.workshopcontroller import WorkshopController
from imageslib.controllers.imagecontroller import ImageController

from lib.utils.pdf2pxmap import render_pdf_page
from lib.utils.util import to_str

import fitz


class HomePageModule(QWidget, Ui_Form):

    def __init__(self, autoid, parent=None):
        super(HomePageModule, self).__init__(parent)
        self.setupUi(self)
        self.autoid=autoid
        self.current_img = object
        self.current_page = object
        self.PC = ProductController()
        self.WC = WorkshopController()
        self.IC = ImageController()
        # 自动缩放
        self.label_image.setScaledContents(True)
        self.get_detail()
        self.get_images()
        self.scrollArea.setVisible(False)
        self.groupBox.setVisible(False)

    def get_detail(self):
        key_dict = {'autoid': self.autoid}
        res = self.PC.get_producingplan(False, *VALUES_TUPLE_PP, **key_dict)
        if not len(res):
            return
        pp_detail = res[0]
        self.label_product.setText(pp_detail['prodid'] + pp_detail['prodname'])
        self.label_commonname.setText(pp_detail['commonname'])
        self.label_spec.setText(pp_detail['spec'])
        self.label_package.setText(pp_detail['package'])
        self.label_batchno.setText(pp_detail['batchno'])
        self.label_realamout.setText(
            to_str(pp_detail['realamount']) + pp_detail['spunit']
        )
        self.label_makedate.setText(str(pp_detail['makedate']))

    def get_images(self):
        self.treeWidget_imagenamelist.clear()
        self.treeWidget_imagenamelist.hideColumn(0)
        key_dict = {'ppid': self.autoid}
        imgid_list = self.WC.get_plids(True,*VALUES_TUPLE_PLIB, **key_dict)
        if not len(imgid_list):
            return

        for item in imgid_list:
            qtreeitem = QTreeWidgetItem(self.treeWidget_imagenamelist)
            qtreeitem.setText(0, str(item['imgid']))
            qtreeitem.setText(1, str(item['title']))
            qtreeitem.setText(2, str(item['ext']))
        self.treeWidget_imagenamelist.resizeColumnToContents(1)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_imagenamelist_itemDoubleClicked(self, qtreeitem, p_int):
        self.scrollArea.setVisible(True)
        self.groupBox.setVisible(True)
        img_id = int(qtreeitem.text(0))
        ext = qtreeitem.text(2).lower()
        key_dict = {
            'autoid': img_id
        }
        img_list = self.IC.get_image(False, *VALUES_TUPLE_IMG, **key_dict)
        if not len(img_list):
            return
        image = img_list[0]
        if ext == 'pdf':
            self.comboBox_jumpto.setVisible(True)
            self.pushButton_prepage.setVisible(True)
            self.pushButton_nextpage.setVisible(True)
            self.current_img = fitz.Document(stream=image['img'],
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
            img = QImage.fromData(image['img'])
            self.current_img = QPixmap.fromImage(img)
            self.label_image.setPixmap(self.current_img)

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




VALUES_TUPLE_PLIB = ('title', 'imgid', 'ext')
VALUES_TUPLE_IMG = ('img',)
VALUES_TUPLE_PP = (
    'prodid', 'prodname', 'commonname', 'spec', 'package', 'batchno',
    'makedate', 'realamount', 'spunit'
)
