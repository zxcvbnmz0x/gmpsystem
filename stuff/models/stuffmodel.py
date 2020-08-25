# -*- coding: utf-8 -*-
import traceback

from lib.utils.saveexcept import SaveExcept

from db.models import Stuffdictionary, Productstuff, Stuffdrawpaper


class StuffModel(object):
    def __init__(self):
        super().__init__()

    def get_all_stuff(self, stufftype=-1):
        try:
            if stufftype == -1:
                return Stuffdictionary.objects.all().values('autoid', 'stuffid',
                                                            'stuffname', 'kind',
                                                            'stufftype', 'spec',
                                                            'package',
                                                            'allowno',
                                                            'storage').order_by(
                    'stuffid')
            else:
                return Stuffdictionary.objects.filter(
                    stufftype=stufftype).values('autoid', 'stuffid',
                                                'stuffname', 'kind',
                                                'stufftype', 'spec', 'package',
                                                'allowno', 'storage').order_by(
                    'stuffid')
        except Exception as e:
            SaveExcept(e, "获取全部物料信息时出错", data=stufftype)

    @staticmethod
    def get_stuff(autoid):
        try:
            return Stuffdictionary.objects.get(autoid=autoid)
        except Exception as e:
            print('repr(e):\t', repr(e))
            return False

    def delete_stuff(self, autoid=None, *args):
        if autoid:
            return Stuffdictionary.objects.filter(autoid=autoid).delete()
        elif args:
            return Stuffdictionary.objects.filter(autoid__in=args).delete()

    @staticmethod
    def update_stuff(autoid=None, **kwargs):
        try:
            if autoid:
                return Stuffdictionary.objects.filter(autoid=autoid).update(
                    **kwargs)
            elif kwargs:
                return Stuffdictionary.objects.create(**kwargs)
        except Exception as e:
            print(repr(e))

    @staticmethod
    def get_prodstuff(flag=0, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            if len(args):
                res = Productstuff.objects.filter(**kwargs).values_list(*args, flat=flat)
                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)

            else:
                return Productstuff.objects.filter(**kwargs)
        except Exception as e:
            SaveExcept(e, "获取产品物料时出错", *args, **kwargs)

    @staticmethod
    def get_Mprodstuff(ppid):
        try:
            sql = "SELECT autoid,kind,unit,stufftype," \
                  "sum(realamount) as realamount,sum(drawamount) as drawamount," \
                  "sum(backamount) as backamount,sum(restamount) as restamount " \
                  "FROM productstuff where ppid =%s group by kind"
            res = Productstuff.objects.raw(sql, [ppid, ])
            return res
        except Exception as e:
            SaveExcept(e, "获取产品物料(部分批次)时出错", data=ppid)

    @staticmethod
    def get_stuffdrawpaper(*args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            if len(args):
                return Stuffdrawpaper.objects.filter(**kwargs).values_list(*args, flat=flat)
            else:
                return Stuffdrawpaper.objects.filter(**kwargs)

        except Exception as e:
            SaveExcept(e, "获取领料单信息时出错", *args, **kwargs)

    @staticmethod
    def update_stuffdrawpaper(autoid=0, *args, **kwargs):
        try:
            if autoid:
                return Stuffdrawpaper.objects.filter(autoid=autoid).update(**kwargs)
            else:
                return Stuffdrawpaper.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新领料单信息时出错", data=autoid , *args, **kwargs)