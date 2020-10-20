# -*- coding: utf-8 -*-
from workshop.models.workshopmodels import WorkshopModels
from warehouse.controllers.warehousecontroller import WarehouseController
from django.db import transaction, connection


class WorkshopController():

    def get_productputinnote(self, display_flag=False, *args, **kwargs):
        return WorkshopModels.get_productputinnote(display_flag, *args,
                                                   **kwargs)

    def get_prodqrcode(self, display_flag=False, *args, **kwargs):
        return WorkshopModels.get_prodqrcode(display_flag, *args, **kwargs)

    def get_qrcoderep(self, display_flag=False, *args, **kwargs):
        return WorkshopModels.get_qrcoderep(display_flag, *args, **kwargs)

    def update_productputinnote(self, autoid=0, in_warehouse=False,
                                putin_msg=[], *args, **kwargs):
        if not in_warehouse:
            return WorkshopModels.update_productputinnote(autoid, *args,
                                                          **kwargs)
        if autoid == 0:
            return
        with transaction.atomic():
            p1 = transaction.savepoint()
            cursor = connection.cursor()
            # 每个项目对应一条产品库存记录
            # 每个项目分别是一个元组，包括3个元素，
            #   0：入库类型，1：记录对应的autoid,用于入库时补全信息， 2：本项的数量
            for item in putin_msg:
                '''
                cursor.execute(
                    r"call addprodrep(%s, %s, %s, %s, %s)" % (item[i] for i in range(0,4))
                )
                '''
                cursor.execute(
                    "call addprodrep(%s, %s, %s, %s, %s)" % (
                        item[0], item[1], item[2], item[3], item[4])
                )
            return WorkshopModels.update_productputinnote(autoid, *args,
                                                          **kwargs)

    def update_prodqrcode(self, key_dict=None, *args, **kwargs):
        return WorkshopModels.update_prodqrcode(key_dict, *args, **kwargs)

    def delete_prodqrcode(self, key_dict, *args, **kwargs):
        return WorkshopModels.delete_prodqrcode(key_dict, *args, **kwargs)