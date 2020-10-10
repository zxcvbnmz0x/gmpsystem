# -*- coding: utf-8 -*-

from db.models import Client

from lib.utils.saveexcept import SaveExcept


class SaleModel():

    @staticmethod
    def get_client(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Client.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取客户信息时出错", *args, **kwargs)

    @staticmethod
    def update_client(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Client.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Client.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Client.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新客户信息时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_client(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Client.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Client.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Client.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除客户信息时出错", *args, *kwargs)
