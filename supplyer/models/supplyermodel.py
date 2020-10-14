# -*- coding: utf-8 -*-

from db.models import Supplyer, Stuffsupplyers, Purchasingplan, Pplist
from lib.utils.saveexcept import SaveExcept


class SupplyerModel(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_supply(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            if len(args):
                res = Supplyer.objects.filter(**kwargs)
                if display_flag:
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
            detail.update(spid_id=SupplyerModel.objects.get(supid=kwargs['supid']).autoid)
            detail.pop('supid')
            if 'supname' in detail.keys():
                detail.pop('supname')
        try:
            if autoid is None:
                return Stuffsupplyers.objects.create(**detail)
            else:
                return Stuffsupplyers.objects.filter(autoid=autoid).update(
                    **detail)
        except Exception as e:
            print(repr(e))

    def delete_stuff_supplyer(self, autoid):
        try:
            return Stuffsupplyers.objects.filter(autoid__in=autoid).delete()
        except Exception as e:
            print(repr(e))


    @staticmethod
    def get_purchasingplan(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Purchasingplan.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取采购单信息时出错", *args, **kwargs)

    @staticmethod
    def update_purchasingplan(autoid=None, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Purchasingplan.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Purchasingplan.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Purchasingplan.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新采购单时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_ppurchasingplan(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Purchasingplan.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Purchasingplan.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Purchasingplan.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除采购单时出错", *args, *kwargs)

    @staticmethod
    def get_purchstuff(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Pplist.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取采购物料信息时出错", *args, **kwargs)

    @staticmethod
    def update_purchstuff(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Pplist.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Pplist.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Pplist.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新采购物料时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_purchstuff(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Pplist.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Pplist.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Pplist.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除采购物料时出错", *args, *kwargs)

    @staticmethod
    def get_stuffsupplyer(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Stuffsupplyers.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取物料供应商关系信息时出错", *args, **kwargs)
