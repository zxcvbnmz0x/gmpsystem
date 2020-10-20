# -*- coding: utf-8 -*-

from sale.models.salemodel import SaleModel


class SaleController():

    def get_client(self, display_flag=False, *args, **kwargs):
        return SaleModel.get_client(display_flag, *args, **kwargs)

    def update_client(self, display_flag=False, *args, **kwargs):
        return SaleModel.update_client(display_flag, *args, **kwargs)

    def delete_client(self, display_flag=False, *args, **kwargs):
        return SaleModel.delete_client(display_flag, *args, **kwargs)

    def get_salenotes(self, display_flag=False, *args, **kwargs):
        return SaleModel.get_salenotes(display_flag, *args, **kwargs)

    def update_salenotes(self, autoid, *args, **kwargs):
        return SaleModel.update_salenotes(autoid, *args, **kwargs)

    def delete_salenotes(self, autoid, *args, **kwargs):
        return SaleModel.delete_salenotes(autoid, *args, **kwargs)

    def get_salegoods(self, display_flag=False, *args, **kwargs):
        return SaleModel.get_salegoods(display_flag, *args, **kwargs)

    def update_salegoods(self, autoid, *args, **kwargs):
        return SaleModel.update_salegoods(autoid, *args, **kwargs)

    def delete_salegoods(self, autoid, *args, **kwargs):
        return SaleModel.delete_salegoods(autoid, *args, **kwargs)

    def get_salenotegoods(self, display_flag=False, *args, **kwargs):
        return SaleModel.get_salenotegoods(display_flag, *args, **kwargs)

    def update_salenotegoods(self, autoid, *args, **kwargs):
        return SaleModel.update_salenotegoods(autoid, *args, **kwargs)

    def delete_salenotegoods(self, autoid=None, *args, **kwargs):
        return SaleModel.delete_salenotegoods(autoid, *args, **kwargs)
