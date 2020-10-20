# -*- coding: utf-8 -*-
from lib.utils.saveexcept import SaveExcept
from django.db import transaction, connection
from db.models import Productdictionary, Productlabel, Producingplan, Midproddrawnotes, Oddmentdrawnotes
from imageslib.controllers.image import Image
import user


class ProductModel(object):

    @staticmethod
    def get_all_product(medkind=-1):
        try:
            if medkind == -1:
                return Productdictionary.objects.all().values('autoid',
                                                              'prodid',
                                                              'prodname',
                                                              'commonname',
                                                              'medkind', 'spec',
                                                              'package',
                                                              'allowno',
                                                              'storage').order_by(
                    'prodid')
            else:
                return Productdictionary.objects.filter(medkind=medkind).values(
                    'autoid', 'prodid', 'prodname', 'commonname', 'medkind',
                    'spec', 'package', 'allowno', 'storage').order_by('prodid')
        except Exception as e:
            print('repr(e):\t', repr(e))
            return False

    @staticmethod
    def get_productdictionary(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Productdictionary.objects.filter(**kwargs)
            if len(args):

                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取产品字典时出错", *args, *kwargs)

    @staticmethod
    def delete_product(autoid=None, *args):
        if autoid:
            return Productdictionary.objects.filter(autoid=autoid).delete()
        elif args:
            return Productdictionary.objects.filter(autoid__in=args).delete()

    @staticmethod
    def update_product(autoid=None, **kwargs):
        try:
            if autoid:
                return Productdictionary.objects.filter(autoid=autoid).update(
                    **kwargs)
            elif kwargs:
                return Productdictionary.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新产品字典出错", data=autoid, **kwargs)

    @staticmethod
    def get_all_medkind():
        return Productdictionary.objects.values_list('medkind',
                                                     flat=True).distinct()

    @staticmethod
    def get_label(autoid=0, *args, **kwargs):
        if autoid and kwargs:
            kwargs.update(autoid=autoid)
        return Productlabel.objects.filter(**kwargs)

    @staticmethod
    def update_productlabel(autoid, **kwargs):
        return Productlabel.objects.filter(autoid=autoid).update(**kwargs)

    @staticmethod
    def delete_productlabel(autoid, *args):
        try:
            with transaction.atomic():
                image_model = Image()
                image_list = Productlabel.objects.filter(
                    autoid__in=autoid).values_list("imgid", flat=True)
                image_model.delete_image(image_list)
                return Productlabel.objects.filter(autoid__in=autoid).delete()
        except Exception as e:
            SaveExcept(e, "删除产品标签图时出错", autoid=autoid, args=args)

    @staticmethod
    def save_productlabel(autoid=None, prodid=None, image_name=None,
                          imagedetail=None, *args, **kwargs):
        try:
            date = dict()
            if prodid:
                date['prodid'] = prodid
            if image_name:
                date['imagename'] = image_name
            date['modifierid'] = user.user_id
            date['modifiername'] = user.user_name
            date['modifytime'] = user.now_time
            if autoid:
                with transaction.atomic():
                    image_model = Image()
                    item = Productlabel.objects.filter(
                        autoid=autoid).values_list("imgid", flat=True)
                    image_model.save_image(autoid=item[0],
                                           imagedetail=imagedetail)
                    return Productlabel.objects.filter(autoid=autoid).update(
                        **date)
            else:
                with transaction.atomic():
                    image_model = Image()
                    image_id = image_model.save_image(imagedetail=imagedetail)
                    date['imgid'] = image_id.autoid
                    date['flag'] = 0
                    return Productlabel.objects.create(**date)
        except Exception as e:
            SaveExcept(e, "保存产品标签图时出错", autoid=autoid, args=args, kwargs=kwargs)

    @staticmethod
    def get_producingplan(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Producingplan.objects.filter(**kwargs)
            if len(args):

                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "ProductModel-get_producing获取批记录信息时出错", *args,
                       **kwargs)

    @staticmethod
    def get_midproddrawnotes(flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Midproddrawnotes.objects.filter(**kwargs)
            if len(args):

                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取半成品登记/发放时出错", *args, *kwargs)

    @staticmethod
    def get_oddmentdrawnotes(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Oddmentdrawnotes.objects.filter(**kwargs)
            if len(args):

                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取零头登记/发放时出错", *args, *kwargs)

    @staticmethod
    def update_producingplan_status(autoid, *args, **kwargs):
        try:
            if kwargs['status'] == 2:
                with transaction.atomic():
                    cursor = connection.cursor()
                    for aid in autoid:
                        cursor.execute("call startproducingplan(%s)" % (aid))
                    res = Producingplan.objects.filter(
                        autoid__in=autoid).update(**kwargs)
                return res
            else:
                return Producingplan.objects.filter(autoid__in=autoid).update(
                    **kwargs)
        except KeyError:
            pass

    @staticmethod
    def update_producingplan(autoid, *args, **kwargs):
        try:
            if autoid:
                return Producingplan.objects.filter(autoid=autoid).update(
                    **kwargs)
            elif kwargs:
                return Productdictionary.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新生产指令出错", data=autoid, *args, **kwargs)

    @staticmethod
    def update_midproddrawnotes(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Midproddrawnotes.objects.filter(
                        autoid=autoid).update(**kwargs)
                else:
                    return Midproddrawnotes.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Midproddrawnotes.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新半成品登记/发放记录出错", data=autoid, *args, **kwargs)

    @staticmethod
    def update_oddmentdrawnotes(autoid, *args, **kwargs):
        try:
            if autoid:
                if type(autoid) == int:
                    return Oddmentdrawnotes.objects.filter(autoid=autoid).update(**kwargs)
                else:
                    return Oddmentdrawnotes.objects.filter(
                        autoid__in=autoid).update(**kwargs)
            elif kwargs:
                return Oddmentdrawnotes.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, "更新零头登记/发放记录出错", data=autoid, *args, **kwargs)

    @staticmethod
    def create_producingplan(flat, **kwargs):
        try:
            cursor = connection.cursor()
            cursor.execute(
                "select createproducingplan(%s,%s)" % (flat, kwargs['id']))
            aid = cursor.fetchone()
            del kwargs['id']
            # kwargs['id'] = aid
            if aid:
                ProductModel.update_producingplan(aid[0], **kwargs)
                return aid[0]
        except KeyError:
            SaveExcept(KeyError, "缺少产品autoid", data=flat, **kwargs)
        except Exception as e:
            SaveExcept(e, "新建生产记录时出错", data=flat, **kwargs)

    @staticmethod
    def delete_producingplan(autoid=None, flat=0, *args):
        try:
            autoid_list = list(args)
            if autoid is not None:
                autoid_list.append(autoid)
            if flat == 0:
                return Producingplan.objects.filter(
                    autoid__in=autoid_list).delete()
            elif flat == 1:
                cursor = connection.cursor()
                for item in args:
                    with transaction.atomic():
                        cursor.execute("select deletproducingplan(%s)" % item)
                        raw = cursor.fetchone()
                        if raw[0] != 1:
                            return 0
                return 1

            else:
                pass
        except Exception as e:
            SaveExcept(e, "删除生产记录时出错", *args, flat=flat)


    @staticmethod
    def delete_midproddrawnotes(autoid, *args, **kwargs):
        try:
            res = Midproddrawnotes.objects
            if type(autoid) is int:
                return res.filter(autoid=autoid).delete()
            elif type(autoid) is list:
                return res.filter(autoid__in=autoid).delete()
            else:
                return []
        except Exception as e:
            SaveExcept(e, "删除半成品登记记录时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def delete_oddmentdrawnotes(autoid, *args, **kwargs):
        try:
            res = Oddmentdrawnotes.objects
            if type(autoid) is int:
                return res.filter(autoid=autoid).delete()
            elif type(autoid) is list:
                return res.filter(autoid__in=autoid).delete()
            else:
                return []
        except Exception as e:
            SaveExcept(e, "删除零头登记记录时出错", data=autoid, *args, **kwargs)

    @staticmethod
    def get_oddment_invaliddate(date, validday):
        cursor = connection.cursor()
        cursor.execute(
            r"select calcexpireddate('%s',%s)" % (date, validday))
        invaliddate = cursor.fetchone()
        # date 2020-09-09,变成了减法
        return invaliddate