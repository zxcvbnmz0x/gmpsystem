# -*- coding: utf-8 -*-

from db.models import Supplyer
from lib.utils.saveexcept import SaveExcept


class SupplyerModel(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_supply(flag=0, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            if len(args):
                res = Supplyer.objects.filter(**kwargs)
                if flag == 0:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return Supplyer.objects.filter(**kwargs)
        except Exception as e:
            SaveExcept(e, "SupplyerModel-get_supply获取供应商信息时出错", *args,
                       **kwargs)

    def update_stuff_supplyer_item(self, autoid=None, **kwargs):
        detail = kwargs
        if "supid" in detail.keys():
            detail.update(spid_id=SP.objects.get(supid=kwargs['supid']).autoid)
            detail.pop('supid')
            if 'supname' in detail.keys():
                detail.pop('supname')
        try:
            if autoid is None:
                print(detail)
                return Stuffsupplyers.objects.create(**detail)
            else:
                print(detail)
                return Stuffsupplyers.objects.filter(autoid=autoid).update(
                    **detail)
        except Exception as e:
            print(repr(e))

    def delete_stuff_supplyer(self, autoid):
        try:
            return Stuffsupplyers.objects.filter(autoid__in=autoid).delete()
        except Exception as e:
            print(repr(e))