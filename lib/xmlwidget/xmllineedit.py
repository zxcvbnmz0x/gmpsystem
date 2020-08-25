# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtXml import QDomDocument, QDomElement


class XmlLineEdit(QLineEdit):
    text_changed = pyqtSignal()

    def __init__(self, parent=None, xmlelement='QDomElement:None'):
        super().__init__(parent)
        self.element = xmlelement
        self.qdom = QDomDocument()

        self.var_dict = dict()
        self.widget_dict = dict()
        self.expr_value = self.element.text()

        self.wid = self.element.attribute("ID")
        self.qtext = self.element.firstChild()
        if self.qtext.isNull():
            self.qtext = self.qdom.createTextNode('')
            self.qtext = self.element.appendChild(self.qtext)
        self.setStyleSheet("margin:2 2;")
        width = int(self.element.attribute(
            "MaxLength")) * 7 + 4 if self.element.attribute(
            "MaxLength") else 134
        height = int(
            self.element.attribute("MaxHeight")) * 24 if self.element.attribute(
            "MaxHeight") else 24
        self.resize(width, height)
        self.textEdited.connect(self.on_textEdited)

    def on_textEdited(self, p_str):
        self.qtext.setNodeValue(p_str)

    def varToWidget(self, var, widgetOrValue:tuple):
        # widgetOrValue,包括2个值(flag,value)
        # 如果flag = 0,则为value
        # 如果flag = 1,则为widget
        if var not in self.var_dict:
            self.var_dict[var] = widgetOrValue

    def ChangedSlot(self, p_str):
        widget = self.sender()
        #可能会抛出ValueError
        self.widget_dict[widget] = int(p_str)
        self.flush()

    def flush(self):
        expr = self.expr_value
        for key, value in self.var_dict.items():
            if expr:
                expr = expr.replace(key, str(self.widget_dict[value[1]]) if value[0] else str(value[1]))
        self.setText(expr)
