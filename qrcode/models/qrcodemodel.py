# -*- coding: utf-8 -*-

from db.models import Qrcoderepository

from lib.utils.saveexcept import SaveExcept

from django.db.utils import IntegrityError


class QrcodeModel():

    @staticmethod
    def get_qrcoderep(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Qrcoderepository.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取二维码库信息时出错", *args, **kwargs)

    @staticmethod
    def update_qrcoderep(key_dict=None, *args, **kwargs):
        if key_dict:
            return Qrcoderepository.objects.filter(*key_dict).update(**kwargs)
        else:
            if len(kwargs):
                return Qrcoderepository.objects.create(**kwargs)
            else:
                insert_list = []
                for item in args:
                    insert_list.append(
                        Qrcoderepository(
                            qrcode=item[0],
                            prodname=item[1],
                            allowno=item[2],
                            companyname=item[3],
                            telno=item[4],
                            createdate=item[5]
                        )

                    )
                try:
                    return Qrcoderepository.objects.bulk_create(insert_list)
                except IntegrityError as e:
                    return 1062
