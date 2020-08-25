import sys
import decimal
import re

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QFile, QRect
from PyQt5.QtXml import QDomDocument

import user as userdetail
from lib.utils.evalenv import evalenv
from db.models import Selfdefinedformat, Forms
from product.controllers.productcontroller import ProductController
from stuff.controllers.stuffcontroller import StuffController
from labrecord.controllers.labrecordscontroller import LabrecordsController

from lib.xmlwidget.xmlcheckbox import XmlCheckBox
from lib.xmlwidget.xmlcombobox import XmlComboBox
from lib.xmlwidget.xmlexprbox import XmlExprBox
from lib.xmlwidget.xmllineedit import XmlLineEdit
from lib.xmlwidget.xmlsignbox import XmlSignBox
from lib.xmlwidget.xmltextedit import XmlTextEdit

from tesui import Ui_Form

# 批记录产品信息类变量
PRODUCT_DICT = {'PBIANHAO': 'prodid', 'PMING': 'prodname', 'PGUIGE': 'spec',
                'PBZGG': 'package', 'PTMING': 'commonname', 'PPIHAO': 'batchno',
                'PSHIJI': 'realamount', 'PJIHUA': 'planamount',
                'PJIXING': 'medkind'
                }
# 批记录物料信息类变量
STUFF_DICT = {'ID': 'stuffid', 'MING': 'stuffname', 'PIHAO': 'batchno',
              'LEIBIE': 'kind', 'GUIGE': 'spec', 'BZGG': 'package',
              'JBDW': 'unit', 'XBZDW': 'spunit', 'ZBZDW': 'mpunit',
              'DBZDW': 'bpunit',
              'JIHUA': 'presamount', 'SHIJI': 'realamount',
              'LINGQU': 'drawamount',
              'SHENGYU': 'restamount', 'TUIKU': 'backamount',
              'SHUIFEN': 'water',
              'HANLIANG': 'content', 'CHANGJIA': 'producer'
              }
STUFF_KIND = {'ZF': (0, 1), 'ZC': 0, 'FC': 1, 'NB': 2, 'WB': 3, 'BC': (2, 3),
              'QC': 4}
# 检验报告类信息变量
# 检品编号，检品名称，批号，半成品取样，成品取样，生产厂家，报告编号，检品数量
LAB_DICT = {'SID': 'chkid', 'SMING': 'chkname', 'JPPIHAO': 'batchno',
            'MQUYANG': 'samplecount', 'PQUYANG': 'samplecount',
            'SPRODUCER': 'producer', 'SBGBH': 'paperno',
            'JPSHULIANG': 'checkamount'
            }

# 对齐方式
alignment = ('L', 'C', 'R')
qtalign = (Qt.AlignLeft, Qt.AlignHCenter, Qt.AlignRight)


class XMLRW(QDialog, Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.dom = QDomDocument()
        # 线框，先把所有线框的信息都保存了，最后再刷新
        self.line_border = list()

        self.current_X = 20
        self.current_Y = 10
        self.form = parent
        # 要查询的记录id
        self.autoid = 0
        # 要查询的内容,0测试，1生产，2检验
        self.type = 0
        self.proddetail = None
        self.stuffdetail = None
        self.mstuffdetail = None
        self.labdetail = None
        self.stuffdetailZF = list()
        self.stuffdetailZC = list()
        self.stuffdetailFC = list()
        self.stuffdetailNB = list()
        self.stuffdetailWB = list()
        self.stuffdetailBC = list()
        self.stuffdetailQC = list()

        self.stuffdetailMZF = list()
        self.stuffdetailMZC = list()
        self.stuffdetailMFC = list()
        self.stuffdetailMNB = list()
        self.stuffdetailMWB = list()
        self.stuffdetailMBC = list()
        self.stuffdetailMQC = list()

    # 中文：14个像素 英文：7个像素，系统中的长度*7 = 像素
    # 中文数*2 = 系统中的长度，中位数*14 = 像素
    # 系统中长度*7 = 像素
    def openxml(self, file):

        # 传入的是地址
        qfile = QFile(file)
        # 找到文件,则设置引擎,否则向xml文件直接添加数据
        if qfile.open(QFile.ReadWrite | QFile.Text):
            self.dom.setContent(QFile)
        else:
            self.dom.setContent(file)
        if self.dom.isNull():
            return False
        # 获得根目录的元素,返回QDomElement    <GMPPaper>
        element = self.dom.documentElement()
        # 获得第一个子元素，返回QDomNode
        n = element.firstChild()
        # 如果没有读到文档结尾，而且没有出现错误
        while not n.isNull():
            # 把当前的QDomNode转为QDomElement
            e = n.toElement()

            if not e.isNull():
                name = e.tagName()
                # 标题框
                if name == "Title":
                    self.titleBox(e)
                # 标题输入框
                elif name == "TextBox":
                    self.inputBox(e)
                # 线框
                elif name == "Box":
                    self.wireframe(e)
                # 检测框
                elif name == "CheckBox":
                    self.checkBox(e)
                # 下拉框
                elif name == "ComboBox":
                    self.comboBox(e)
                # 签名框
                elif name == "Signature":
                    self.signBox(e)
                # 表达式
                elif name == "Expr":
                    self.exprBox(e)
                # 换行
                elif name == "br":
                    self.wrapBox()
            # 空格组成的字符，包括换行
            elif self.dom.isWhitespace():
                pass
            # 纯文本
            elif self.dom.isCharacters():
                pass
            # 获取下一个同级标签
            n = n.nextSibling()

        if qfile.isOpen():
            qfile.close()
        # self.update()
        self.scrollAreaWidgetContents.setLineBorder(self.line_border)
        '''
        try:

        except Exception as e:
            print(repr(e))
            pass
            # raise ValueError
        '''

    # 标题框
    def titleBox(self, element):
        widget = XmlTextEdit(self.scrollAreaWidgetContents, 1, element)
        #widget.setContentsMargins(2, 0, 0, 0)
        self.boxresize(widget)
        # L C R ,左中右对齐
        align = element.attributeNode("align").value()
        widget.setAlignment(Qt.AlignVCenter | qtalign[alignment.index(align)])
        widget.setText(self.set_vars(element.text()))

    # 输入框
    def inputBox(self, element):
        widgetlabel = XmlTextEdit(self.scrollAreaWidgetContents, 1, element)
        widgetlineedit = XmlLineEdit(self.scrollAreaWidgetContents, element)


        widgetlabel.setText(
            self.set_vars(element.AttributeNode("Title").value()))

        self.boxresize(widgetlabel)
        self.boxresize(widgetlineedit)

        wid = element.AttributeNode("ID").value()
        widgetlineedit.setText(self.set_vars(element.text()))
        if wid:
            try:
                setattr(self, wid, decimal.Decimal(widgetlineedit.text()))
            except:
                setattr(self, wid, '')

    # 线框
    def wireframe(self, element):
        linewidth = int(element.attributeNode("width").value()) * 7
        lineheight = int(element.attributeNode("height").value()) * 20
        penwidth = int(element.attributeNode("PenWidth").value())

        qrect = QRect(self.current_X, self.current_Y, linewidth,
                             lineheight)

        self.line_border.append((qrect, penwidth))

    # 检测框
    def checkBox(self, element):
        self.dom.readNextStartElement()
        widget = XmlCheckBox(self.scrollAreaWidgetContents, element)

        self.boxresize(widget)
        widget.setText(self.set_vars(element.AttributeNode("name").value()))
        widget.setChecked(int(element.text()))

    # 下拉框
    def comboBox(self, element):
        index = 0
        widget = XmlComboBox(self.scrollAreaWidgetContents, element)
        self.boxresize(widget)

        # 允许自己填内容，则显示“value”的内容，
        # 否则显示index序号的内容
        if int(element.AttributeNode("style").value()):
            widget.setEditable(
                int(element.AttributeNode("style").value()))
            widget.setCurrentText(
                element.AttributeNode("value").value())
        else:
            index = int(element.AttributeNode("index").value())
        if self.element.hasChildNodes():
            q = self.element.firstChild()
            while not q.isNull():
                b = q.toElement()
                if not b.isNull():
                    self.addItem(self.set_vars(b.text()))
                q = q.nextSibling()
        widget.setCurrentIndex(index)

    # 签名框
    def signBox(self, element):
        widget = XmlSignBox(self.scrollAreaWidgetContents, element)
        self.boxresize(widget)
        widget.setText(element.text())

    # 表达式
    def exprBox(self, element):
        widget = XmlExprBox(self.scrollAreaWidgetContents, element)
        self.boxresize(widget)

        # 后缀
        sibfix = ''
        # 计算过程
        expr = ''
        # 显示的表达式
        va = ''
        vid = element.AttributeNode("ID").value()
        if element.hasChildNodes():
            q = element.firstChild()
            while not q.isNull():
                b = q.toElement()
                if b.tagName() == "subfix":
                    sibfix = b.text()
                elif b.name() == "expr":
                    expr = b.text()
                elif b.name() == "vars":
                    va = b.text()
                q = q.nextSibling()

        # 把文件中的#变量，改为实例中的变量。
        expr = expr.replace('#', 'self.')
        expr = self.set_vars(expr)
        va = self.set_vars(va)
        result = ''
        try:
            result = str(eval(expr, evalenv(self)))
            widget.setText(va + result + sibfix)
        except:
            return "公式格式错误"
        if vid:
            setattr(self, vid, result)

    # 换行框
    def wrapBox(self):
        self.current_X = 20
        self.current_Y += 20

    # 设置控件的位置
    # w:控件的宽度变量名
    # h:控件的高度变量名
    def boxresize(self, widget):
        widget.move(self.current_X, self.current_Y)
        self.current_X += widget.width()

    # 设置表达式
    def set_vars(self, exp):
        items, sys_items = self.get_vars(exp)
        if items:
            for item in set(items):
                try:
                    exp = exp.replace(item, str(getattr(self, item[1:-1])))
                except AttributeError:
                    exp = exp.replace(item, '')
        if sys_items:
            for item in set(sys_items):
                try:
                    # 切片去除头尾的@
                    # 日期类变量
                    if item[1: -1] in (
                    'NIAN', 'YUE', 'RI', 'SHI', 'FEN', 'MIAO'):
                        exp = exp.replace(item,
                                          str(getattr(userdetail, item[1:-1])))
                    # 产品信息类变量
                    elif item[1: -1] in PRODUCT_DICT:
                        if self.proddetail is not None:
                            exp = exp.replace(item, str(
                                self.proddetail[PRODUCT_DICT[item[1: -1]]]))
                        else:
                            try:
                                self.get_sys_vars(0)
                                exp = exp.replace(item, str(
                                    self.proddetail[PRODUCT_DICT[item[1: -1]]]))
                            except IndexError:
                                exp = exp.replace(item, str(''))
                    # 产品物料，分批次
                    elif item[3: -2] in STUFF_DICT or item[3: -3] in STUFF_DICT:
                        # 变量的后缀
                        num = int(re.search(r'\d+', item).group(0)) - 1
                        vals = [x for x in re.split(r'@|\d', item) if x][0]
                        var_list = getattr(self, 'stuffdetail' + item[1: 3])
                        if len(var_list):
                            exp = exp.replace(item, str(
                                getattr(var_list[num], STUFF_DICT[vals[2:]])))
                        else:
                            self.get_sys_vars(1)
                            var_list = getattr(self, 'stuffdetail' + item[1: 3])
                            exp = exp.replace(item, str(
                                getattr(var_list[num], STUFF_DICT[vals[2:]])))
                    # 产品物料，不分批次
                    elif item[4: -2] in STUFF_DICT or item[4: -3] in STUFF_DICT:
                        # 变量的后缀
                        num = int(re.search(r'\d+', item).group(0)) - 1
                        vals = [x for x in re.split(r'@|\d', item) if x][0]
                        var_list = getattr(self, 'stuffdetail' + item[1: 4])
                        if len(var_list):
                            exp = exp.replace(item, str(
                                getattr(var_list[num], STUFF_DICT[vals[3:]])))
                        else:
                            self.get_sys_vars(2)
                            var_list = getattr(self, 'stuffdetail' + item[1: 4])
                            exp = exp.replace(item, str(
                                getattr(var_list[num], STUFF_DICT[vals[3:]])))
                    # 检验报告类信息变量
                    elif item[1: -1] in LAB_DICT:
                        if self.labdetail is not None:
                            exp = exp.replace(item, str(
                                self.labdetail[LAB_DICT[item[1: -1]]]))
                        else:
                            self.get_sys_vars(3)
                            exp = exp.replace(item, str(
                                self.labdetail[LAB_DICT[item[1: -1]]]))
                except:
                    exp = exp.replace(item, str(''))
        return exp

    # 获取系统变量的值
    # kind  获取的数据类型，0生产，1物料，2检验
    def get_sys_vars(self, kind=0):
        if self.autoid != 0:
            try:
                if kind == 0:
                    pm = ProductController()
                    self.proddetail = pm.get_producingplan(autoid=self.autoid)[
                        0]
                elif kind == 1:
                    sm = Stuff()
                    self.stuffdetail = sm.get_prodstuff(self.autoid)
                    for item in self.stuffdetail:
                        stufftype = item.stufftype
                        if stufftype == 0:
                            self.stuffdetailZC.append(item)
                            self.stuffdetailZF.append(item)
                        elif stufftype == 1:
                            self.stuffdetailFC.append(item)
                            self.stuffdetailZF.append(item)
                        elif stufftype == 2:
                            self.stuffdetailNB.append(item)
                            self.stuffdetailBC.append(item)
                        elif stufftype == 3:
                            self.stuffdetailWB.append(item)
                            self.stuffdetailBC.append(item)
                        elif stufftype == 4:
                            self.stuffdetailQC.append(item)
                elif kind == 2:
                    sm = Stuff()
                    self.mstuffdetail = sm.get_Mprodstuff(self.autoid)
                    for item in self.mstuffdetail:
                        stufftype = item.stufftype
                        if stufftype == 0:
                            self.stuffdetailMZC.append(item)
                            self.stuffdetailMZF.append(item)
                        elif stufftype == 1:
                            self.stuffdetailMFC.append(item)
                            self.stuffdetailMZF.append(item)
                        elif stufftype == 2:
                            self.stuffdetailMNB.append(item)
                            self.stuffdetailMBC.append(item)
                        elif stufftype == 3:
                            self.stuffdetailMWB.append(item)
                            self.stuffdetailMBC.append(item)
                        elif stufftype == 4:
                            self.stuffdetailMQC.append(item)
                elif kind == 3:
                    lm = Labrecords()
                    self.labdetail = lm.get_labrecord(1, autoid=self.autoid)[0]
            except:
                # traceback.print_exc()
                pass

    # 获得表达式中的普通变量和系统变量
    # {\w*} 普通变量
    # @\w*@ 系统变量
    def get_vars(self, exp):
        pattern1 = re.compile(r'{\w*}')
        pattern2 = re.compile(r'@\w*@')
        return pattern1.findall(exp), pattern2.findall(exp)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainmenu = XMLRW()

    res = Selfdefinedformat.objects.filter(autoid=2855)
    mainmenu.__setattr__('autoid', 50)
    mainmenu.read(res[0].format)
    mainmenu.show()
    sys.exit(app.exec_())
