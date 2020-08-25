# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

from supplyer.models.supplyermodel import SupplyerModel

from supplyer.modules.stuffsupplyermodule import StuffSupplyerModule


class StuffSupplyer(StuffSupplyerModule):
    flush_signal = QtCore.pyqtSignal()
    supplyer = SupplyerModel()

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_variable(self, var_name, var_value):
        if var_name not in self.detail:
            setattr(self, var_name, var_value)
        else:
            pass

    def set_stuff_supplyer(self):
        # 有autoid,修改记录
        if self.autoid:
            args = {"autoid": self.autoid}
            res = self.supplyer.get_supply(**args)
            if res:
                self.oridetail["supid"] = res[0].spid.supid
                self.oridetail["sdid"] = res[0].sdid.autoid
                self.oridetail["supname"] = res[0].spid.supname
                self.oridetail["producer"] = res[0].producer
                self.supplyerid.setText(res[0].spid.supid)
                self.supplyername.setText(res[0].spid.supname)
                self.producer.setText(res[0].producer)
        # 无autoid,新建记录
        else:
            pass

    def update_stuff_supplyer_item(self, autoid, **detail):
        return self.supplyer.update_stuff_supplyer_item(autoid, **detail)

    def delete_stuff_supplyer(self, autoid):
        return self.supplyer.delete_stuff_supplyer(autoid)
