# -*- coding: utf-8 -*-

from db.models import Client, Salesnotes, Salesgoods,Salesnotesgoods

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

    @staticmethod
    def get_salenotes(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Salesnotes.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取销售订单信息时出错", *args, **kwargs)

    @staticmethod
    def update_salenotes(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Salesnotes.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Salesnotes.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Salesnotes.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新销售订单信息时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_salenotes(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Salesnotes.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Salesnotes.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Salesnotes.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除销售订单信息时出错", *args, *kwargs)

    @staticmethod
    def get_salegoods(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Salesgoods.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取销售货物信息时出错", *args, **kwargs)

    @staticmethod
    def update_salegoods(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Salesgoods.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Salesgoods.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Salesgoods.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新销售货物信息时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_salegoods(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Salesgoods.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Salesgoods.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Salesgoods.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除销售货物信息时出错", *args, *kwargs)

    @staticmethod
    def get_salenotegoods(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Salesnotesgoods.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取待售货物信息时出错", *args, **kwargs)

    @staticmethod
    def update_salenotegoods(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Salesnotesgoods.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Salesnotesgoods.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Salesnotesgoods.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新待售货物信息时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_salenotegoods(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Salesnotesgoods.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Salesnotesgoods.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Salesnotesgoods.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除待售货物信息时出错", *args, *kwargs)
