# -*- coding: utf-8 -*-
from db.models import Producingplan


class Product(object):
    def __init__(self, autoid):
        super().__init__()
        self.__detail = Producingplan.objects.filter(autoid=autoid)

    def getdetail(self):
        return self.__detail

    def setattr(self, key, value):
        setattr(self.__detail, key, value)
        