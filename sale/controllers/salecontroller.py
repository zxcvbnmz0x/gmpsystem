# -*- coding: utf-8 -*-

from sale.models.salemodel import SaleModel


class SaleController():

    def get_client(self, display_flag=False, *args, **kwargs):
        return SaleModel.get_client(display_flag, *args, **kwargs)

    def update_client(self, autoid, *args, **kwargs):
        return SaleModel.update_client(autoid, *args, **kwargs)

    def delete_client(self, autoid, *args, **kwargs):
        return SaleModel.delete_client(autoid, *args, **kwargs)
