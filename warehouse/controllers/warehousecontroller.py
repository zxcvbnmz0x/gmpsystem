# -*- coding: utf-8 -*-

from warehouse.models.warehousemodel import WarehouseModel
from stuff.controllers.stuffcontroller import StuffController
from supplyer.controllers.supplyercontroller import SupplyerController

from django.db import transaction

import datetime

import user


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

    def get_stuffrepository(self, display_flag=False, *args, **kwargs):
        return self.WM.get_stuffrepository(display_flag, *args, **kwargs)
        """res = self.WM.get_stuffrepository(flag, *args, **kwargs)
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
        """

    def update_stuffrepository(self, autoid=None, *args, **kwargs):
        return WarehouseModel.update_stuffrepository(autoid, *args, **kwargs)

    def update_stuffrepository_amount(self, *args, **kwargs):
        return WarehouseModel.update_stuffrepository_amount(*args, **kwargs)

    def get_productputoutpaper(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_productputoutpaper(display_flag, *args, **kwargs)

    def update_productputoutpaper(self, autoid=None, *args, **kwargs):
        return WarehouseModel.update_productputoutpaper(autoid, *args, **kwargs)

    def delete_productputoutpaper(self, autoid=None, *args, **kwargs):
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

    def get_stuffcheckin(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_stuffcheckin(display_flag, *args, **kwargs)

    def update_stuffcheckin(self, autoid, *args, **kwargs):
        return WarehouseModel.update_stuffcheckin(autoid, *args, **kwargs)

    def new_stuffcheckin(self, ppid, *args, **kwargs):
        detail = dict()
        key_dict = {'ppid': ppid}
        stuff_query = self.SP.get_purchstuff(
            False, *VALUES_TUPLE_PPLIST, **key_dict
        )
        if not len(stuff_query):
            return
        stuff_list = list(stuff_query)

        with transaction.atomic():
            p1 = transaction.savepoint()
            res = WarehouseModel.update_stuffcheckin(None, *args, **kwargs)

            for item in stuff_list:
                if item['amount']-item['arrivedamount'] <=0:
                    continue
                detail['paperno'] = res.paperno
                detail['papertype'] = 0
                detail['makedate'] = user.now_date
                detail['expireddate'] = user.now_date + datetime.timedelta(
                    days=item['expireddays']
                )
                detail['checkindate'] = user.now_date
                detail['amount'] = item['amount']-item['arrivedamount']
                detail['piamount'] = item['amount']-item['arrivedamount']
                detail['supid'] = kwargs['supid']
                detail['supname'] = kwargs['supname']
                del item['amount']
                del item['arrivedamount']
                del item['expireddays']
                detail.update(item)
                WarehouseModel.update_stuffcheckinlist(None, **detail)


    def delete_stuffcheckin(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_stuffcheckin(autoid, *args, **kwargs)

    def get_stuffcheckinlist(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_stuffcheckinlist(display_flag, *args, **kwargs)

    def update_stuffcheckinlist(self, autoid, *args, **kwargs):
        return WarehouseModel.update_stuffcheckinlist(autoid, *args, **kwargs)

    def delete_stuffcheckinlist(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_stuffcheckinlist(autoid, *args, **kwargs)

    def get_productrepository(self, display_flag=False, *args, **kwargs):
        return WarehouseModel.get_productrepository(display_flag, *args, **kwargs)

    def update_productrepository(self, autoid, *args, **kwargs):
        return WarehouseModel.update_productrepository(autoid, *args, **kwargs)

    def delete_productrepository(self, autoid, *args, **kwargs):
        return WarehouseModel.delete_productrepository(autoid, *args, **kwargs)


VALUES_TUPLE_PPLIST = (
    'stuffid', 'stuffname', 'stufftype', 'spec', 'package', 'unit', 'amount',
    'arrivedamount', 'expireddays'
)