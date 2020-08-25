import decimal
from db.models import Productstuff,Workflow, Linepost,Eqrunnotes
from django.db import connection,transaction
import sys,datetime
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication  ,QWidget,QLineEdit, QDialog
from PyQt5.QtGui import   QPainter ,QPixmap, QPen
from PyQt5.QtCore import Qt , QPoint, QFile, QUrl,QTextStream,QIODevice,QByteArray
from PyQt5.QtXmlPatterns import QXmlQuery
from PyQt5.QtXml import QDomDocument,QDomNode,QDomElement
from equipment.controllers.equipmentcontroller import EquipmentController

from django.forms import model_to_dict
import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, \
    QLabel, QPushButton
from PyQt5.QtCore import QDateTime
from lib.sign.signbutton import SignButton
from equipment.modules.eqrunnotedodule import EqrunnoteModule
from stuff.modules.stuffdrawpapermodule import StuffdrawpaperModule
from warehouse.modules.drawstuffmodule import DrawstuffModule
from warehouse.modules.stuffpickingmodule import StuffpickingModule

class Winform(QWidget):
    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)
        self.setWindowTitle("窗体布局管理例子")
        self.resize(400, 100)

        fromlayout = QFormLayout()
        labl1 = QLabel("标签1")
        lineEdit1 = QPushButton()
        labl2 = QLabel("标签2")
        lineEdit2 = QLineEdit()
        labl3 = QLabel("标签3")
        lineEdit3 = QLineEdit()

        fromlayout.addRow(labl1, lineEdit1)
        fromlayout.addRow(labl2, lineEdit2)
        fromlayout.addRow(labl3, lineEdit3)

        self.setLayout(fromlayout)
        lineEdit1.clicked.connect(self.a)
    def a(self):
        s = StuffdrawpaperModule(6781, 0, parent=self)
        res = s.show()
        print(res)
from beeprint import pp
from django.db.models import Aggregate, CharField
from django.db.models.expressions import Func
class Concat(Func):
    """ORM用来分组显示其他字段 相当于group_concat"""
    function = 'CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)
        print(expression)
        print(distinct)
        print(extra)


from PyQt5.QtWidgets import QTreeWidgetItem
from db.models import Productstuff
from lib.utils.inputcode import Inputcode
from labrecord.modules.applycheckmodule import ApplycheckModule
import re
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ApplycheckModule(4)
    #form = ApplycheckModule(36, 6808,0)
    form.show()
    sys.exit(app.exec_())

