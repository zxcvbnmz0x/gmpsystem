# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QPushButton, QDialog
from PyQt5.QtXml import QDomDocument, QDomElement
from PyQt5.QtCore import pyqtSignal
from lib.sign.signmodule import SignModule


class XmlSignBox(QPushButton):
    signed = pyqtSignal()

    def __init__(self, parent=None, xmlelement='QDomElement:None'):
        super().__init__(parent)
        self.element = xmlelement
        self.setObjectName("signbutton")
        self.setStyleSheet(
            "QPushButton#signbutton{background-color: rgb(255, 0, 0);border:none;}")
        width = int(
            self.element.attribute("width")) * 7 + 2 if self.element.attribute(
            "width") else 132
        height = int(
            self.element.attribute("height")) * 22 if self.element.attribute(
            "height") else 22
        self.resize(width, height)
        self.clicked.connect(self.on_Clicked)
        self.uid = self.element.firstChildElement("UserID")
        self.uname = self.element.firstChildElement("UserName")
        self.qdom = QDomDocument()

        if self.uid.isNull():
            self.uid = self.qdom.createElement('UserID')
            self.uid = self.element.appendChild(self.uid)
        if self.uname.isNull():
            self.uname = self.qdom.createElement('UserName')
            self.uname = self.element.appendChild(self.uname)

        self.setText(self.uid.nodeValue() + ' ' + self.uname.nodeValue())

    def on_Clicked(self):
        dialog = SignModule(self)
        dialog.userchanged.connect(self.setusername)
        dialog.exec()

    def setusername(self, p_str):
        self.setText(p_str)
        clerkid, clerkname = p_str.split(' ')
        cid = self.qdom.createTextNode(clerkid)
        cname = self.qdom.createTextNode(clerkname)
        self.uid.appendChild(cid)
        self.uname.appendChild(cname)
        self.signed.emit()
