# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QComboBox


class XmlComboBox(QComboBox):

    def __init__(self, parent=None, xmlelement='QDomElement:None'):
        super().__init__(parent)
        self.element = xmlelement
        self.var_dict = dict()
        self.widget_dict = dict()
        self.setStyleSheet("margin:2 2;")
        width = int(
            self.element.attribute("width")) * 7 + 4 if self.element.attribute(
            "width") else 134
        height = int(
            self.element.attribute("height")) * 24 if self.element.attribute(
            "height") else 24
        self.resize(width, height)
        self.currentTextChanged.connect(self.on_currentTextChanged)
        self.currentIndexChanged.connect(self.on_currentIndexChanged)

    def on_currentTextChanged(self, p_str):
        self.element.setAttribute("value", p_str)

    def on_currentIndexChanged(self, p_str):
        self.element.setAttribute("index", p_str)

    def varToWidget(self, var, widgetOrValue:tuple):
        # widgetOrValue,包括2个值(flag,value)
        # 如果flag = 0,则为value
        # 如果flag = 1,则为widget
        if var not in self.var_dict:
            self.var_dict[var] = widgetOrValue