# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'producing.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(999, 724)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treewidget_filetree = QtWidgets.QTreeWidget(self.groupBox)
        self.treewidget_filetree.setAutoScroll(True)
        self.treewidget_filetree.setProperty("showDropIndicator", True)
        self.treewidget_filetree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treewidget_filetree.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.treewidget_filetree.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.treewidget_filetree.setIndentation(10)
        self.treewidget_filetree.setObjectName("treewidget_filetree")
        self.treewidget_filetree.header().setVisible(False)
        self.gridLayout_2.addWidget(self.treewidget_filetree, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 5, 1)
        self.productmessage = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(11)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.productmessage.sizePolicy().hasHeightForWidth())
        self.productmessage.setSizePolicy(sizePolicy)
        self.productmessage.setObjectName("productmessage")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.productmessage)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_prodname = QtWidgets.QLabel(self.productmessage)
        self.label_prodname.setText("")
        self.label_prodname.setObjectName("label_prodname")
        self.gridLayout_3.addWidget(self.label_prodname, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.productmessage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.productmessage)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.productmessage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.productmessage)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.productmessage)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.productmessage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.productmessage)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 3, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.productmessage)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.productmessage)
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 4, 2, 1, 1)
        self.label_basicamount = QtWidgets.QLabel(self.productmessage)
        self.label_basicamount.setText("")
        self.label_basicamount.setObjectName("label_basicamount")
        self.gridLayout_3.addWidget(self.label_basicamount, 3, 5, 1, 1)
        self.label_temperature = QtWidgets.QLabel(self.productmessage)
        self.label_temperature.setText("")
        self.label_temperature.setObjectName("label_temperature")
        self.gridLayout_3.addWidget(self.label_temperature, 4, 5, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.productmessage)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 4, 0, 1, 1)
        self.label_postname = QtWidgets.QLabel(self.productmessage)
        self.label_postname.setText("")
        self.label_postname.setObjectName("label_postname")
        self.gridLayout_3.addWidget(self.label_postname, 3, 1, 1, 1)
        self.label_endtime = QtWidgets.QLabel(self.productmessage)
        self.label_endtime.setText("")
        self.label_endtime.setObjectName("label_endtime")
        self.gridLayout_3.addWidget(self.label_endtime, 4, 3, 1, 1)
        self.label_medkind = QtWidgets.QLabel(self.productmessage)
        self.label_medkind.setText("")
        self.label_medkind.setObjectName("label_medkind")
        self.gridLayout_3.addWidget(self.label_medkind, 2, 1, 1, 1)
        self.label_batchno = QtWidgets.QLabel(self.productmessage)
        self.label_batchno.setText("")
        self.label_batchno.setObjectName("label_batchno")
        self.gridLayout_3.addWidget(self.label_batchno, 1, 3, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.productmessage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 4, 6, 1, 1)
        self.label_planamount = QtWidgets.QLabel(self.productmessage)
        self.label_planamount.setText("")
        self.label_planamount.setObjectName("label_planamount")
        self.gridLayout_3.addWidget(self.label_planamount, 3, 3, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.productmessage)
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 4, 4, 1, 1)
        self.label_humidity = QtWidgets.QLabel(self.productmessage)
        self.label_humidity.setText("")
        self.label_humidity.setObjectName("label_humidity")
        self.gridLayout_3.addWidget(self.label_humidity, 4, 7, 1, 1)
        self.label_package = QtWidgets.QLabel(self.productmessage)
        self.label_package.setText("")
        self.label_package.setObjectName("label_package")
        self.gridLayout_3.addWidget(self.label_package, 1, 5, 1, 3)
        self.label_starttime = QtWidgets.QLabel(self.productmessage)
        self.label_starttime.setText("")
        self.label_starttime.setObjectName("label_starttime")
        self.gridLayout_3.addWidget(self.label_starttime, 4, 1, 1, 1)
        self.label_spec = QtWidgets.QLabel(self.productmessage)
        self.label_spec.setText("")
        self.label_spec.setObjectName("label_spec")
        self.gridLayout_3.addWidget(self.label_spec, 2, 3, 1, 3)
        self.label_filename = QtWidgets.QLabel(self.productmessage)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_filename.setFont(font)
        self.label_filename.setText("")
        self.label_filename.setAlignment(QtCore.Qt.AlignCenter)
        self.label_filename.setObjectName("label_filename")
        self.gridLayout_3.addWidget(self.label_filename, 0, 0, 1, 8)
        self.gridLayout.addWidget(self.productmessage, 0, 1, 1, 3)
        self.groupbox_filecontent = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        sizePolicy.setHeightForWidth(self.groupbox_filecontent.sizePolicy().hasHeightForWidth())
        self.groupbox_filecontent.setSizePolicy(sizePolicy)
        self.groupbox_filecontent.setObjectName("groupbox_filecontent")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupbox_filecontent)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout.addWidget(self.groupbox_filecontent, 1, 1, 1, 3)
        self.pushButton_accept = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_accept.sizePolicy().hasHeightForWidth())
        self.pushButton_accept.setSizePolicy(sizePolicy)
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.gridLayout.addWidget(self.pushButton_accept, 3, 2, 1, 1)
        self.pushButton_flush = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_flush.sizePolicy().hasHeightForWidth())
        self.pushButton_flush.setSizePolicy(sizePolicy)
        self.pushButton_flush.setObjectName("pushButton_flush")
        self.gridLayout.addWidget(self.pushButton_flush, 3, 3, 1, 1)
        self.pushButton_reset = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_reset.sizePolicy().hasHeightForWidth())
        self.pushButton_reset.setSizePolicy(sizePolicy)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.gridLayout.addWidget(self.pushButton_reset, 4, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 999, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "批生产记录"))
        self.groupBox.setTitle(_translate("MainWindow", "文档目录"))
        self.treewidget_filetree.headerItem().setText(0, _translate("MainWindow", "名称"))
        self.treewidget_filetree.headerItem().setText(1, _translate("MainWindow", "类型"))
        self.treewidget_filetree.headerItem().setText(2, _translate("MainWindow", "id"))
        self.treewidget_filetree.headerItem().setText(3, _translate("MainWindow", "docid"))
        self.treewidget_filetree.headerItem().setText(4, _translate("MainWindow", "aid"))
        self.productmessage.setTitle(_translate("MainWindow", "产品信息"))
        self.label.setText(_translate("MainWindow", "产品名称:"))
        self.label_6.setText(_translate("MainWindow", "岗位名称:"))
        self.label_2.setText(_translate("MainWindow", "包装规格:"))
        self.label_4.setText(_translate("MainWindow", "剂型:"))
        self.label_7.setText(_translate("MainWindow", "计划批量:"))
        self.label_3.setText(_translate("MainWindow", "产品批号:"))
        self.label_8.setText(_translate("MainWindow", "基本计划量:"))
        self.label_5.setText(_translate("MainWindow", "规格:"))
        self.label_10.setText(_translate("MainWindow", "结束时间:"))
        self.label_9.setText(_translate("MainWindow", "开始时间:"))
        self.label_23.setText(_translate("MainWindow", "湿度:"))
        self.label_11.setText(_translate("MainWindow", "温度:"))
        self.groupbox_filecontent.setTitle(_translate("MainWindow", "文档内容"))
        self.pushButton_accept.setText(_translate("MainWindow", "保存"))
        self.pushButton_flush.setText(_translate("MainWindow", "刷新"))
        self.pushButton_reset.setText(_translate("MainWindow", "恢复原始表单"))
