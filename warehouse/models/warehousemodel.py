# -*- coding: utf-8 -*-

from db.models import Stuffdrawpaper, Planprescription, Producingplan, \
    Stuffrepository, Productstuff

from lib.utils.saveexcept import SaveExcept

from django.db import transaction

class WarehouseModel(object):

    @staticmethod
    def get_producingplan(*args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            if len(args):
                return Producingplan.objects.filter(**kwargs).values_list(
                    *args, flat=flat)
            else:
                return Producingplan.objects.filter(**kwargs)
        except Exception as e:
            SaveExcept(e, "WarehouseModel-get_producingplan获取生产指令信息时出错", *args,
                       **kwargs)

    @staticmethod
    def get_stuffrepository(flag=0, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            if len(args):
                res = Stuffrepository.objects.filter(**kwargs)
                if flag == 0:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return Stuffrepository.objects.filter(**kwargs)
        except Exception as e:
            SaveExcept(e, "WarehouseModel-get_stuffrepository获取库存信息时出错", *args,
                       **kwargs)

    @staticmethod
    def update_stuffrepository(autoid=None, **kwargs):
        try:
            if autoid is None:
                return Stuffrepository.objects.create(**kwargs)
            else:
                return Stuffrepository.objects.filter(autoid=autoid).update(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新物料库存出错", data=autoid, **kwargs)

    @staticmethod
    def update_productstuff(autoid=None, **kwargs):
        if autoid is None:
            return Productstuff.objects.create(**kwargs)
        else:
            return Productstuff.objects.filter(autoid=autoid).update(
                **kwargs)
        try:
            pass
        except Exception as e:
            SaveExcept(e, "更新产品物料出错", data=autoid, **kwargs)

    @staticmethod
    def update_stuffrepository_amount(*args, **kwargs):
        try:
            if len(args):
                with transaction.atomic():
                    p1 = transaction.savepoint()
                    for item in args:

                        update_stuff = Stuffrepository.objects.filter(
                            autoid=item['srid'])
                        amount = update_stuff.values_list('amount', flat=True)[
                            0]

                        update_stuff.update(amount=amount - item['drawamount'])

                        new_amount = update_stuff.values_list(
                            'amount', flat=True
                        )[0]
                        if new_amount < 0:
                            transaction.savepoint_rollback(p1)
                            return "rollback"
                        WarehouseModel.update_productstuff(**item)
                    sdpid = kwargs['autoid']
                    del kwargs['autoid']
                    Stuffdrawpaper.objects.filter(autoid=sdpid).update(**kwargs)
                    return "accept"
            else:
                return "no changed"

        except Exception as e:
            SaveExcept(e, "更新物料库存数量出错", data=args)
