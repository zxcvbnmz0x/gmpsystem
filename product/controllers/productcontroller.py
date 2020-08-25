# -*- coding: utf-8 -*-
from product.models.productmodel import ProductModel
from stuff.models.stuffmodel import StuffModel


class ProductController(object):
    def __init__(self):
        pass

    def get_all_medkind(self):
        return ProductModel.get_all_medkind()

    def update_product(self, autoid, **kwargs):
        return ProductModel.update_product(autoid, **kwargs)

    def get_label(self, autoid=0, *args, **kwargs):
        return ProductModel.get_label(autoid, *args, **kwargs)

    def update_productlabel(self, autoid, **kwargs):
        return ProductModel.update_productlabel(autoid, **kwargs)

    def delete_productlabel(self, autoid=None, *args):
        return ProductModel.delete_productlabel(autoid, *args)

    def save_productlabel(self, autoid=None, prodid=None, imagename=None,
                          imagedetail=None, *args,
                          **kwargs):
        return ProductModel.save_productlabel(autoid, prodid, imagename, imagedetail,
                                         *args,
                                         **kwargs)

    def get_producingplan(self, flag=0, *args, **kwargs):
        return ProductModel.get_producingplan(flag, *args, **kwargs)

    def delete_producingplan(self, autoid=None, flat=0, *args):
        return ProductModel.delete_producingplan(autoid, flat, *args)

    def get_product_or_stuff(self, flag=0, autoid=0):
        # flag：产品的类型，0和2为成品，1为前处理
        if flag in (0, 2):
            return ProductModel.get_product(autoid)
        elif flag == 1:
            sm = StuffModel()
            return sm.get_stuff(autoid)

    def update_producingplan_status(self, autoid, *args, **kwargs):
        return ProductModel.update_producingplan_status(autoid, *args, **kwargs)

    def update_producingplan(self, autoid=0, prodtype=0, *args, **kwargs):
        if autoid:
            return ProductModel.update_producingplan(autoid, *args, **kwargs)
        else:
            try:
                return ProductModel.create_producingplan(prodtype, **kwargs)
            except Exception:
                return None
