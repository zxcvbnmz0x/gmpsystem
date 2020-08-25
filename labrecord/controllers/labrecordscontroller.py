# -*- coding: utf-8 -*-
from labrecord.models.labmodel import LabModel


class LabrecordsController(object):

    def get_labrecord(self, flag=0, *args, **kwargs):
        return LabModel.get_labrecord(flag, *args, **kwargs)

    def get_labitem(self, flag=0, *args, **kwargs):
        return LabModel.get_labitem(flag, *args, **kwargs)
