# -*- coding: utf-8 -*-

from db.models import Systemoptions, Syssetting
from lib.utils.saveexcept import SaveExcept

class SystemModel():

    @staticmethod
    def get_systemoption(flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Systemoptions.objects.filter(**kwargs)
            if len(args):

                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取系统参数时出错", *args, *kwargs)

    @staticmethod
    def update_systemoption(otid, *args, **kwargs):
        try:
            if otid:
                if type(otid) == int:
                    return Systemoptions.objects.filter(
                        otid=otid).update(**kwargs)
                else:
                    return Systemoptions.objects.filter(
                        otid__in=otid).update(**kwargs)
            elif kwargs:
                return Systemoptions.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新系统参数出错", data=otid, *args, **kwargs)

    @staticmethod
    def delete_systemoption(otid, *args, **kwargs):
        try:
            res = Systemoptions.objects
            if type(otid) is int:
                return res.filter(autoid=otid).delete()
            elif type(otid) is list:
                return res.filter(otid__in=otid).delete()
            else:
                return []
        except Exception as e:
            SaveExcept(e, "删除系统参数时出错", data=otid, *args, **kwargs)

    @staticmethod
    def get_syssetting(flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Syssetting.objects.filter(**kwargs)
            if len(args):

                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取系统设置时出错", *args, *kwargs)

    @staticmethod
    def update_syssetting(otid, *args, **kwargs):
        try:
            if otid:
                if type(otid) == int:
                    return Syssetting.objects.filter(
                        otid=otid).update(**kwargs)
                else:
                    return Syssetting.objects.filter(
                        otid__in=otid).update(**kwargs)
            elif kwargs:
                return Systemoptions.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新系统设置出错", data=otid, *args, **kwargs)

    @staticmethod
    def delete_Syssetting(otid, *args, **kwargs):
        try:
            res = Syssetting.objects
            if type(otid) is int:
                return res.filter(autoid=otid).delete()
            elif type(otid) is list:
                return res.filter(otid__in=otid).delete()
            else:
                return []
        except Exception as e:
            SaveExcept(e, "删除系统设置时出错", data=otid, *args, **kwargs)
