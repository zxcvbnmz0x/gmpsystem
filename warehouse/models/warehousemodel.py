# -*- coding: utf-8 -*-

from db.models import Stuffdrawpaper, Planprescription, Producingplan, \
    Stuffrepository, Productstuff, Productputoutpaper, Ppopqrcode, \
    Productwithdrawnotes, Pwngoods, Pwqrcode, Stuffcheckin, Stuffcheckinlist

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
    def update_stuffrepository(autoid=None, *args, **kwargs):
        try:
            if autoid is None:
                return Stuffrepository.objects.create(**kwargs)
            else:
                return Stuffrepository.objects.filter(autoid=autoid).update(
                    **kwargs)
        except Exception as e:
            SaveExcept(e, "更新物料库存出错", data=autoid, **kwargs)

    @staticmethod
    def update_productstuff(autoid=None, **kwargs):
        try:
            if autoid is None:
                return Productstuff.objects.create(**kwargs)
            else:
                return Productstuff.objects.filter(autoid=autoid).update(
                    **kwargs)
        except Exception as e:
            SaveExcept(e, "更新产品物料出错", data=autoid, **kwargs)

    @staticmethod
    def update_stuffrepository(autoid=None, **kwargs):
        try:
            if autoid:
                if type(autoid) is int:
                    return Productstuff.objects.filter(autoid=autoid).\
                        update(**kwargs)
                else:
                    return Productstuff.objects.filter(autoid__in=autoid).\
                        update(**kwargs)

            else:
                return Stuffrepository.objects.create(**kwargs)

        except Exception as e:
            SaveExcept(e, "更新物料库存时出错", data=autoid, **kwargs)

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

    @staticmethod
    def get_productputoutpaper(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Productputoutpaper.objects.filter(**kwargs)
            if len(args):

                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取产品出库单信息时出错", *args,
                       **kwargs)

    @staticmethod
    def update_productputoutpaper(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Productputoutpaper.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Productputoutpaper.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Productputoutpaper.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新产品出库单时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_productputoutpaper(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Productputoutpaper.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Productputoutpaper.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Productputoutpaper.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除产品出库单时出错", *args, **kwargs)

    @staticmethod
    def get_prodwithdrawnote(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Productwithdrawnotes.objects.filter(**kwargs)
            if len(args):

                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取产品退货单信息时出错", *args,
                       **kwargs)

    @staticmethod
    def update_prodwithdrawnote(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Productwithdrawnotes.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Productwithdrawnotes.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Productwithdrawnotes.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新产品退货单时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_prodwithdrawnote(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Productwithdrawnotes.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Productwithdrawnotes.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Productwithdrawnotes.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除产品退货单时出错", *args, **kwargs)

    @staticmethod
    def get_ppopqrcode(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Ppopqrcode.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取产品出库二维码信息时出错", *args, **kwargs)

    @staticmethod
    def update_ppopqrcode(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Ppopqrcode.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Ppopqrcode.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Ppopqrcode.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新产品出库二维码时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_ppopqrcode(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Ppopqrcode.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Ppopqrcode.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Ppopqrcode.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除产品出库二维码时出错", *args, *kwargs)

    @staticmethod
    def get_pwqrcode(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Pwqrcode.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取产品退货二维码信息时出错", *args, **kwargs)

    @staticmethod
    def update_pwqrcode(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Pwqrcode.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Pwqrcode.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Pwqrcode.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新产品退货二维码时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_pwqrcode(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Pwqrcode.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Pwqrcode.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Pwqrcode.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除产品退货二维码时出错", *args, *kwargs)

    @staticmethod
    def get_stuffcheckin(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Stuffcheckin.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取进货登记信息时出错", *args, **kwargs)

    @staticmethod
    def update_stuffcheckin(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Stuffcheckin.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Stuffcheckin.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Stuffcheckin.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新进货登记时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_stuffcheckin(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Stuffcheckin.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Stuffcheckin.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Stuffcheckin.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除进货登记时出错", *args, *kwargs)

    @staticmethod
    def get_stuffcheckinlist(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Stuffcheckinlist.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取进货登记的物料信息时出错", *args, **kwargs)

    @staticmethod
    def update_stuffcheckinlist(autoid=None, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Stuffcheckinlist.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Stuffcheckinlist.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Stuffcheckinlist.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新进货登记的物料时出错", autoid, *args, **kwargs)

    @staticmethod
    def delete_stuffcheckinlist(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Stuffcheckinlist.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Stuffcheckinlist.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Stuffcheckinlist.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除进货登记的物料时出错", *args, *kwargs)
