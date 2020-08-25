# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode, QDomAttr


class XmlCheckBox(QCheckBox):

    def __init__(self, parent=None, xmlelement='QDomElement:None'):
        super().__init__(parent)
        self.element = xmlelement
        qdom = QDomDocument()
        self.opt_tag = self.element.firstChildElement()
        # 如果子标签里没有option标签，则新建一个，宽度为8，默认值为0
        if self.opt_tag.isNull():
            self.opt_tag = qdom.createElement("option")
            self.element.appendChild(self.opt_tag)
            self.opt_tag.setAttribute("name", "")
            self.opt_tag.setAttribute("width", "8")
            opt_value = qdom.createTextNode(0)
            self.opt_tag.appendchild(opt_value)

        self.setStyleSheet("margin:2 2;")
        width = int(
            self.element.attribute("width")) * 7 + 4 if self.element.attribute(
            "width") else 134
        height = int(
            self.element.attribute("height")) * 24 if self.element.attribute(
            "height") else 24
        self.resize(width, height)
        self.stateChanged.connect(self.on_stateChanged)

    def on_stateChanged(self, p_int):
        self.opt_tag.firstChild().setNodeValue(str(p_int))
