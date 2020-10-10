# -*- coding: utf-8 -*-

from warehouse.models.warehousemodel import WarehouseModel
from stuff.controllers.stuffcontroller import StuffController
from supplyer.controllers.supplyercontroller import SupplyerController

class WarehouseController(object):

    def __init__(self):
        self.SC = StuffController()
        self.SP = SupplyerController()
        self.WM = WarehouseModel()

    def get_stuffdrawpaper(self, *args, **kwargs):
        res = self.SC.get_stuffdrawpaper(*args, **kwargs)
        if len(res):
            ppid_list = list()
            for item in res:
                ppid_list.append(item.ppid)
            value_tuple = ('autoid', 'prodid', 'prodname', 'spec', 'package', 'batchno')
            prod_info_tuple = self.WM.get_producingplan(*value_tuple, autoid__in=set(ppid_list))
            for item in res:
                for it in prod_info_tuple:
                    if item.ppid == it[0]:
                        item.prod = it[1] + ' ' + it[2]
                        item.spec = it[3]
                        item.package = it[4]
                        item.batchno = it[5]
            return res
        else:
            return []

    def get_stuffrepository(self, flag=0, *args, **kwargs):
        res = self.WM.get_stuffrepository(flag, *args, **kwargs)
        supid_list = []
        if len(res):
            for item in res:
                supid_list.append(item['supid'])
            supplyers = self.SP.get_supply(('supid', 'supname'), supid__in=set(supid_list))
            for item in res:
                item['supname'] = ''
                for supplyer in supplyers:
                    if item['supid'] == supplyer[0]:
                        item['supname'] = supplyer[1]
                        break
        return res

    def update_stuffrepository_amount(self, *args, **kwargs):
        return WarehouseModel.update_stuffrepository_amount(*args, **kwargs)

    def get_prodputoutpaper(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_productputoutpaper(display_flag, *args, **kwargs)

    def update_prodputoutpaper(self, autoid, *args, **kwargs):
        return WarehouseModel.update_productputoutpaper(autoid, *args, **kwargs)

    def delete_productputpaper(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_productputoutpaper(autoid, *args, **kwargs)

    def get_prodwithdrawnote(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_prodwithdrawnote(display_flag, *args, **kwargs)

    def update_prodwithdrawnote(self, autoid, *args, **kwargs):
        return WarehouseModel.update_prodwithdrawnote(autoid, *args, **kwargs)

    def delete_prodwithdrawnote(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_prodwithdrawnote(autoid, *args, **kwargs)

    def get_ppopqrcode(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_ppopqrcode(display_flag, *args, **kwargs)

    def update_ppopqrcode(self, autoid, *args, **kwargs):
        return WarehouseModel.update_ppopqrcode(autoid, *args, **kwargs)

    def delete_ppopqrcode(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_ppopqrcode(autoid, *args, **kwargs)

    def get_pwqrcode(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_pwqrcode(display_flag, *args, **kwargs)

    def update_pwqrcode(self, autoid, *args, **kwargs):
        return WarehouseModel.update_pwqrcode(autoid, *args, **kwargs)

    def delete_pwqrcode(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_pwqrcode(autoid, *args, **kwargs)
