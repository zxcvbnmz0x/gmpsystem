# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

from workshop.models.workshopmodels import WorkshopModels
from workshop.views.producing import Ui_MainWindow
from product.controllers.productcontroller import ProductController

from stuff.modules.stuffdrawpapermodule import StuffdrawpaperModule

from lib.xmlwidget.xmlreadwrite import XMLReadWrite
from lib.utils.messagebox import MessageBox
from linepost.modules.postdetailmodule import PostdetailModule
from cleanfirmity.modules.cleanconfirmitycopymodule import CleanconfirmityCopyModule
from cleanfirmity.modules.cleanconfirmityoriginalmodule import CleanconfirmityOriginalModule


class ProducingModule(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, autoid, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.product = ProductController()
        self.autoid = autoid
        # 当前的文档内容
        self.current_docid = 0
        self.current_content = object
        self.wsmodels = WorkshopModels()
        self.detail = self.product.get_producingplan(autoid=autoid)
        if len(self.detail) != 1:
            raise ValueError
        self.linepost = self.wsmodels.get_linepost(autoid)
        linepost_list = []
        if len(self.linepost):
            for item in self.linepost:
                linepost_list.append(item.autoid)
        self.linepostdocuments = self.wsmodels.get_linepostdocuments(linepost_list)
        #if len(self.linepostdocuments):
        # 初始化标题和基本信息
        self.setup_title(self.detail[0])
        # 初始化文档目录
        self.setup_filetree(list(self.linepost), list(self.linepostdocuments))

    # 初始化标题和基本信息
    def setup_title(self, detail_list):
        self.label_prodname.setText(detail_list.prodid + ' ' +detail_list.prodname)
        self.label_batchno.setText(detail_list.batchno)
        self.label_package.setText(detail_list.package)
        self.label_medkind.setText(detail_list.medkind)
        self.label_spec.setText(detail_list.spec)
        self.label_planamount.setText(str(detail_list.planamount) + detail_list.spunit)
        self.label_basicamount.setText(str(detail_list.planamount * detail_list.basicamount) + detail_list.basicunit)

    # 初始化文档目录
    # post_list:岗位列表
    # document_list:文档列表
    # 数节点分3行，第一行为岗位/文档的id，第2行为岗位：0，
    # 文档：负数->内建文档，整数->自定义文档
    def setup_filetree(self, post_list, document_list):
        # 把岗位列表和文档列表合并为一个新的字典
        post_to_doucument = dict()
        for item in post_list:
            post_to_doucument[item] = []
            for it in document_list[:]:
                if item.autoid == it.lpid:
                    post_to_doucument[item].append(it)
                    document_list.remove(it)

        treeitem_root = QtWidgets.QTreeWidgetItem(self.treewidget_filetree)
        treeitem_root.setText(0, "批生产记录封面")
        treeitem_root.setText(1, '0')

        for item in post_to_doucument:
            qtreeitem = QtWidgets.QTreeWidgetItem(treeitem_root)

            qtreeitem.setText(0, item.postname)
            qtreeitem.setText(1, '1')
            qtreeitem.setText(2, str(item.autoid))
            qtreeitem.setText(3, str(item.seqid))
            qtreeitem.setText(4, str(item.expireddays))
            for it in post_to_doucument[item]:
                qtreechilditem = QtWidgets.QTreeWidgetItem(qtreeitem)
                #0 :文档名称，1：autoid,2:docid,3:aid
                if it.docid < 0:
                    # 内建文档
                    qtreechilditem.setText(0, GENERAL_DOC[it.docid])
                    qtreechilditem.setText(1, '2')
                    qtreechilditem.setText(2, str(it.autoid))
                    qtreechilditem.setText(3, str(it.docid))
                    qtreechilditem.setText(4, str(it.aid))
                else:
                    qtreechilditem.setText(0, it.formatname)
                    qtreechilditem.setText(1, '3')
                    qtreechilditem.setText(2, str(it.autoid))
                    qtreechilditem.setText(3, str(it.docid))
                    qtreechilditem.setText(4, '0')
        self.treewidget_filetree.hideColumn(1)
        self.treewidget_filetree.hideColumn(2)
        self.treewidget_filetree.hideColumn(3)
        self.treewidget_filetree.hideColumn(4)
        self.treewidget_filetree.expandAll()

    # 打开一个新文档
    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def on_treewidget_filetree_itemClicked(self, qitem, p_int):
        try:
            # 判断之前是否有打开过文档且没有保存
            if self.current_content.flat:
                dialog = MessageBox(self, title="提醒", text="文档尚未保存",
                                    informative="是否要保存文档", yes_text="保存",
                                    no_text="放弃保存")
                result = dialog.exec()
                if result == QtWidgets.QMessageBox.Yes:
                    # 调用保存的槽函数
                    self.on_pushButton_accept_clicked()

        except (AttributeError, TypeError):
            pass
        finally:
            if not self.gridLayout_4.isEmpty():
                self.gridLayout_4.removeWidget(self.current_content)
                self.current_content.close()

        self.label_filename.setText(qitem.text(0))
        self.current_docid = qitem.text(3)

        # 点击的是内建文档
        if qitem.text(1) == '2':
            doctype = int(qitem.text(3))
            # 领料单
            if doctype in (-2, -3, -4):
                self.current_content = StuffdrawpaperModule(qitem.text(4), self)
                self.gridLayout_4.addWidget(self.current_content)
            # 请验单
            if doctype in (-15, -16, -17, -18):
                # =============================
                # =============================
                # =============================
                # =============================
                # =============================
                # =============================
                # =============================
                # =============================
                # =============================
                pass

            # 清场合格证（副本）
            elif doctype == -18:
                self.current_content = CleanconfirmityCopyModule(int(qitem.text(4)), self)
                self.gridLayout_4.addWidget(self.current_content)
                #self.current_content = module
            # 清场合格证（正本）
            elif doctype == -17:
                self.current_content = CleanconfirmityOriginalModule(qitem.text(4), qitem.parent().text(2), self)
                self.gridLayout_4.addWidget(self.current_content)
                #self.current_content = module

        # 点击的是自定义文档
        elif qitem.text(1) == '3':
            # 自定义文档在Forms表里的id
            formatid = qitem.text(3)
            document = self.wsmodels.get_form(formatid)
            if document is not None:
                content = document.format
                self.current_content = XMLReadWrite(self)
                self.current_content.openxml(content)
                self.gridLayout_4.addWidget(self.current_content)
                self.current_content.__setattr__('autoid', self.autoid)
        # 点击的是岗位名
        elif qitem.text(1) == '1':
            self.current_content = PostdetailModule(qitem.text(2), self.detail[0].lineid, qitem.text(3), qitem.text(0), self)
            self.gridLayout_4.addWidget(self.current_content)

    @QtCore.pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if int(self.current_docid) > 0:
            res = self.wsmodels.update_form(self.current_docid, self.current_content.get_content())
            if res:
                self.current_content.flat = 0
        else:
            res = self.current_content.save()

    @QtCore.pyqtSlot()
    def on_pushButton_flush_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def on_pushButton_reset_clicked(self):
        pass


GENERAL_DOC = {
    -1: "生产指令",
    -2: "原、辅材料领料单",
    -3: "内包装材料领料单",
    -4: "外包装材料领料单",
    -5: "原、辅材料退库单",
    -6: "内包装材料退库单",
    -7: "外包装材料退库单",
    -8: "批包装指令单",
    -9: "批剩余(残次)标签、包装材料销毁记录",
    -10: "称量配料记录",
    -11: "半成品登记记录",
    -12: "半成品发放记录",
    -13: "成品寄库单",
    -14: "前处理入库单",
    -15: "半成品请验单",
    -16: "成品请验单",
    -17: "中间产品请验单",
    -18: "验证请验单",
    -19: "清场合格证(副本)",
    -20: "清场合格证(正本)",
    -21: "库存零头领取单",
    -22: "尾料销毁记录",
    -23: "产品二维码",
    -24: "小、中包装二维码关联",
    -25: "大、中包装二维码关联",
    -26: "巨、大包装二维码关联",
    -27: "零头登记记录",
    -28: "零头发放记录",
    -29: "退货产品领料单",
}
