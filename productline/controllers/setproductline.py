# -*- coding: utf-8 -*-

from productline.modules.selectproductlinemodule import SelectProductLine


class SetProductLine(SelectProductLine):
    def __init__(self, parent=None, pltype=None):
        super().__init__(parent, pltype)
