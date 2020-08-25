# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtXml import QDomDocument, QDomElement

from lib.utils.evalenv import evalenv


class XmlExprBox(QLineEdit):

    def __init__(self, parent=None, xmlelement='QDomElement:None'):
        super().__init__(parent)
        self.element = xmlelement
        self.qdom = QDomDocument()
        self.wid = self.element.attribute("ID")

        self.var_dict = dict()
        self.widget_dict = dict()

        # 后缀
        self.subfix = self.element.firstChildElement("subfix")
        self.subfix_value = self.subfix.firstChild()
        # 公式
        self.vars = self.element.firstChildElement("vars")
        self.vars_value = self.vars.firstChild()
        # 计算结果
        self.expr = self.element.firstChildElement("expr")
        self.expr_value = self.expr.firstChild()
        # 初始化后缀、公式、计算结果
        self.set_subfix()
        self.set_vars()
        self.set_expr()

        self.setEnabled(False)
        self.setStyleSheet("background-color: rgb(85, 255, 255);margin:2 2;")
        width = int(
            self.element.attribute("width")) * 7 + 4 if self.element.attribute(
            "width") else 134
        height = int(
            self.element.attribute("height")) * 24 if self.element.attribute(
            "height") else 24
        self.resize(width, height)

    def set_subfix(self):
        if self.subfix.isNull():
            self.subfix = self.qdom.createElement("subfix")
            self.subfix = self.element.appendChild(self.subfix)
        if self.subfix.firstChild().isNull():
            self.subfix_value = self.qdom.createTextNode("")
            self.subfix_value = self.subfix.appendChild(self.subfix_value)

    def set_vars(self):
        if self.vars.isNull():
            self.vars = self.qdom.createElement("vars")
            self.vars = self.element.appendChild(self.vars)
        if self.vars.firstChild().isNull():
            self.vars_value = self.qdom.createTextNode("")
            self.vars_value = self.subfix.appendChild(self.vars_value)


    def set_expr(self):
        if self.expr.isNull():
            self.expr = self.qdom.createElement("expr")
            self.expr = self.element.appendChild(self.expr)
        if self.expr.firstChild().isNull():
            self.expr_value = self.qdom.createTextNode("")
            self.expr_value = self.subfix.appendChild(self.expr_value)

    def varToWidget(self, var, widgetOrValue:tuple):
        # widgetOrValue,包括2个值(flag,value)
        # 如果flag = 0,则为value
        # 如果flag = 1,则为widget
        if var not in self.var_dict:
            self.var_dict[var] = widgetOrValue

    def ChangedSlot(self, p_str):
        #widget = self.sender()
        #可能会抛出ValueError
        #self.widget_dict[widget] = int(p_str)
        self.flush()

    def flush(self):
        formula = self.vars_value.nodeValue()
        expr = self.expr_value.nodeValue()
        try:
            for key, value in self.var_dict.items():
                kind = value[0]
                wvalue = str(value[1].text() if value[1].text() != '' else None) if kind else str(value[1])
                try:
                    if formula:
                        formula = formula.replace(key, wvalue)
                except Exception as e:
                    pass
                try:
                    if expr:
                        expr = expr.replace(key, wvalue)
                except Exception as e:
                    pass
            expr = str(eval(expr, evalenv(self)))
            self.setText(formula + expr + self.subfix_value.nodeValue())
        except Exception as e:
            pass
