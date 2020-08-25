# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtXml import QDomElement


# 标题框
class XmlTextEdit(QLabel):

    def __init__(self, parent=None, xmlelement='QDomElement:None'):

        super().__init__(parent)
        self.element = xmlelement

        self.var_dict = dict()
        self.widget_dict = dict()
        self.expr_value = self.element.hasAttribute("Title")
        if self.element.hasAttribute("Title"):
            self.expr_value = self.element.attribute("Title")
        else:
            self.expr_value = self.element.text()

        self.setStyleSheet("border: None;")
        self.setEnabled(False)
        self.setStyleSheet("margin:2 2;")
        if self.element.hasAttribute("width"):
            width = int(self.element.attribute(
                "width")) * 7 + 4 if self.element.attribute("width") else 0
            height = int(self.element.attribute(
                "height")) * 24 if self.element.attribute("height") else 24
        else:
            width = int(
                self.element.attribute("Width")) * 7 if self.element.attribute(
                "Width") else 0
            height = int(self.element.attribute(
                "Height")) * 24 if self.element.attribute("Height") else 24

        self.resize(width, height)

    # 变量和控件的映射，分2种情况，
    # 一：值直接可以使用，如系统变量
    # 二：值指向另一个控件的值，如自定义变量
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
