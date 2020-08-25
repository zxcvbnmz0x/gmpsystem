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